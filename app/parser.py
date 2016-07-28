import justext
import requests


class ParserError(Exception):
    '''Base class for exceptions in the parser module'''
    pass


class URLRetrievalError(ParserError):
    '''Exception raised for errors in the URL input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
        e    -- the original exception that was raised
    '''

    def __init__(self, expr, msg, e=None):
        self.expr = expr
        self.msg = msg
        self.e = e


class DocumentParsingError(ParserError):
    '''Exception raised for errors in the parsing of the URL.

    Attributes:
        expr -- input expression in which the error occurred
    '''

    def __init__(self, msg):
        self.msg = msg


def get_document(url):
    ''' This function will check if the url is valid and then
    proceed to parse it to produce a clean text (no html) which
    can be used as input to a recommendation engine.

    Arguments:
        url  -- input url that needs to be checked and parsed
    '''
    try:
        r = requests.head(url, allow_redirects = True)
    except requests.exceptions.ConnectionError as e:
        raise URLRetrievalError(url, 'Could not connect', e)
    if r.status_code != requests.codes.ok:
        raise URLRetrievalError(url, 'Invalid response code from remote server: {}'
                                .format(r.status_code))
    if r.headers["content-type"].split(';')[0] not in ["text/html",
                                                       "text/plain"]:
        raise URLRetrievalError(url, 'Document has invalid MIME type: {}'
                                .format(r.headers["content-type"]))
    raw = requests.get(url)
    paragraphs = justext.justext(raw.content, justext.get_stoplist("English"))
    text_only = ''
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            text_only += ' ' + paragraph.text
    if len(text_only) == 0:
        raise DocumentParsingError('Length of document is zero')
    return text_only
