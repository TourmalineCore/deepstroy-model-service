import urllib


def build_url(host, path, **params) -> str:
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urllib.parse.urlparse(host))
    url_parts[2] = path

    url_parts[4] = urllib.parse.urlencode(params)
    return urllib.parse.urlunparse(url_parts)
