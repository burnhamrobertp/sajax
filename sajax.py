import pkg_resources
import pprint


class Sajax:
    """Register Python routes or methods with Sajax.js

    Given a set of python routes or FlaskViews, register these routes so that they can be
    easily called using dynamically built, route-specific javascript methods.
    """

    def get_js_path(self):
        """Return the path to sajax.js"""
        return pkg_resources.resource_string(__name__, 'static/js/sajax.js')


    def get_js_string(self):
        """Return the string contents of sajax.js"""
        pass


    def register_view(self, view):
        """Register a FlaskView


        """
        pprint.pprint(view)