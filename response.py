from flask import jsonify, session, url_for
import json, os, pprint
from config import *


class SResponse:
    """An object which eases the work between ajax and python"""
    data = []

    def __init__(self, cls=None):
        self.data = []

        # If we're loading a view and have not yet loaded its static dependencies, asynchronously load them
        if cls.__class__.__name__.find('View') != -1:
            folder = cls.__class__.__name__.replace('View', '').lower()

            # if its not in loaded, it hasn't been loaded
            if folder not in session['sajax']['loaded_dep']:
                # css first, /static/css/obt_folder.css
                if os.path.isfile(ROOT+'/static/css/obt_'+folder+'.css'):
                    self.data.append({'action': 'load', 'data': url_for('static', filename='css/obt_%s.css' % folder)})

                # first the js file at /static/js/folder/folder.js if it exists
                if os.path.isfile(ROOT+'/static/js/%s/%s.js' % (folder, folder)):
                    self.data.append({'action': 'load', 'data': url_for('static', filename='js/%s/%s.js' % (folder, folder))})

                # then all the rest of the js files in /static/js/folder/
                if os.path.isdir(ROOT+'/static/js/'+folder):
                    for file in os.listdir(ROOT+'/static/js/'+folder):
                        if (file != folder+'.js'):
                            self.data.append({'action': 'load', 'data': url_for('static', filename='js/%s/%s' % (folder, file))})

                # this folder's js files might have defined an object
                self.data.append({'action': 'js', 'data': "if (typeof %s != 'undefined') window.%s = new %s()" % (folder, folder, folder)})
                # The files will be loaded, mark them as such
                session['sajax']['loaded_dep'].append(folder)

    def __add__(self, other):
        if isinstance(other.data, basestring):
            decoder = json.JSONDecoder()
            self.data += decoder.decode(other.data)['r']
        elif isinstance(other.data, list):
            self.data += other.data

        return self

    def get_json(self):
        return jsonify(r=self.data)

    def assign(self, selector, html):
        self.data.append({ 'action': 'as', 'selector': selector, 'data': html })

    def append(self, selector, html):
        self.data.append({ 'action': 'ap', 'selector': selector, 'data': html })

    def append_template(self, selector, html, template_id):
        self.data.append({ 'action': 'ap_t', 'selector': selector, 'data': html, 'id': template_id })

    def script(self, js):
        self.data.append({ 'action': 'js', 'data': js })

    def position(self, selector, keyword):
        self.data.append({ 'action': 'js', 'data': "$('%s').data('position', '%s').addClass('positioned'); sajax.position('%s');" % (selector, keyword, selector) })

    def remove(self, selector):
        self.data.append({ 'action': 'js', 'data': "$('%s').remove()" % selector })

    def alert(self, text):
        self.data.append({ 'action': 'alert', 'data': text})

    def call(self, path):
        self.data.append({ 'action': 'js', 'data': "sajax.call('%s')" % path})

    def error(self, baseSelector, error):
        self.data.append({ 'action': 'assign', 'selector': baseSelector+' .error', 'data': error })
        self.data.append({ 'action': 'js', 'data': "$('"+baseSelector+" .error').show();" })