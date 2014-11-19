import pkg_resources


def get_javascript_string():
    return pkg_resources.resource_string('sajax', 'static/js/sajax.js')