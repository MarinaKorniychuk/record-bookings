import httplib2

def make_custom_http():
    """Returns a customized httplib2.Http instance to make requests to Google API."""
    return httplib2.Http(timeout=5)
