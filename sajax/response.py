from flask import jsonify, session, url_for
import json, os


class Response:
    """Eases sending of JS commands to the DOM

    Builds an internal json array of commands (and their parameters) to be sent as
    a response to an AJAX request. This AJAX request is expected to have been initiated
    by SAjax's javascript-side methods.

    Sajax JS POSTS requests to Python which uses Response, returns Response.get_json
    back to Sajax JS for processing...pretty simple, no?
    """

    project_root = ''
    inc_file_prefix = ''
    inc_file_suffix = ''

    _data = []


    def __init__(self, cls=None):
        self._data = []

        # If we're loading a view and have not yet loaded its static dependencies, asynchronously load them
        if cls.__class__.__name__.find('View') != -1:
            folder = cls.__class__.__name__.replace('View', '').lower()

            # if its not in loaded, it hasn't been loaded
            if folder not in session['sajax']['loaded_dep']:
                # css first, /static/css/obt_folder.css
                filepath = self.root+'/static/css/%s%s%s.css' % (self.inc_file_prefix, folder, self.inc_file_suffix)
                if os.path.isfile(filepath):
                    self._data.append({'action': 'load', 'data': url_for('static', filename='css/%s.css' % folder)})

                # first the js file at /static/js/folder/folder.js if it exists
                if os.path.isfile(self.root+'/static/js/%s/%s.js' % (folder, folder)):
                    self._data.append({'action': 'load', 'data': url_for('static', filename='js/%s/%s.js' % (folder, folder))})

                # then all the rest of the js files in /static/js/folder/
                if os.path.isdir(self.root+'/static/js/'+folder):
                    for file in os.listdir(self.root+'/static/js/'+folder):
                        if (file != folder+'.js'):
                            self._data.append({'action': 'load', 'data': url_for('static', filename='js/%s/%s' % (folder, file))})

                # this folder's js files might have defined an object
                self._data.append({'action': 'js', 'data': "if (typeof %s != 'undefined') window.%s = new %s()" % (folder, folder, folder)})
                # The files will be loaded, mark them as such
                session['sajax']['loaded_dep'].append(folder)

    def __add__(self, other):
        if isinstance(other.data, basestring):
            decoder = json.JSONDecoder()
            self._data += decoder.decode(other.data)['r']
        elif isinstance(other.data, list):
            self._data += other.data

        return self

    def get_json(self):
        return jsonify(r=self._data)

    def assign(self, selector, html):
        self._data.append({ 'action': 'as', 'selector': selector, 'data': html })

    def append(self, selector, html):
        self._data.append({ 'action': 'ap', 'selector': selector, 'data': html })

    def append_template(self, selector, html, template_id):
        self._data.append({ 'action': 'ap_t', 'selector': selector, 'data': html, 'id': template_id })

    def script(self, js):
        self._data.append({ 'action': 'js', 'data': js })

    def remove(self, selector):
        self._data.append({ 'action': 'js', 'data': "$('%s').remove()" % selector })

    def alert(self, text):
        self._data.append({ 'action': 'alert', 'data': text})

    def call(self, path):
        self._data.append({ 'action': 'js', 'data': "sajax.call('%s')" % path})

    def error(self, baseSelector, error):
        self._data.append({ 'action': 'assign', 'selector': baseSelector+' .error', 'data': error })
        self._data.append({ 'action': 'js', 'data': "$('"+baseSelector+" .error').show();" })