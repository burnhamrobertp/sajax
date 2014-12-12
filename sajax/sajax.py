import pkg_resources


def get_js_string():
    """Return the path to sajax.js"""
    return pkg_resources.resource_string(__name__, 'static/js/sajax.js')
