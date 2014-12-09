import pkg_resources


def get_js_path():
    """Return the path to sajax.js"""
    return pkg_resources.resource_string(__name__, 'static/js/sajax.js')


def get_js_string():
    """Return the string contents of sajax.js"""
    pass