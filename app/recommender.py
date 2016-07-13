import requests


def url_exists(url):
    # function that checks if a url exists
    try:
        r = requests.head(url)
    except:
        return False
    return True


def url_valid(url):
    # Function that checks the validity of the url
    r = requests.head(url)
    return r.status_code == requests.codes.ok


def url_html(url):
    # Function that checks if the url contains html
    r = requests.get(url)
    if "text/html" in r.headers["content-type"]:
        return True
    return False
