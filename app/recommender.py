import requests


class RecommenderError(Exception):
    '''Base class for exceptions in the recommender module'''
    pass


class URLRetrievalError(RecommenderError):
    '''Exception raised for errors in the URL input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    '''

    def __init__(self, expr, msg, e=None):
        self.expr = expr
        self.msg = msg
        self.e = e


def get_document(url):
    # can we get the page?
    # Is it HTML?
    # How long is it? Too long, too short (invalid length) or no data?
    try:
        r = requests.head(url)
    except requests.exceptions.ConnectionError as e:
        raise URLRetrievalError(url, 'Could not connect', e)
    if r.status_code != requests.codes.ok:
        raise URLRetrievalError(url, 'Invalid response code\
                                      from remote server')
    if r.headers["content-type"].split(';')[0] not in ["text/html", "text/plain"]:
        raise URLRetrievalError(url, 'Document has invalid MIME type: {}'.format(r.headers["content-type"]))
    return url
