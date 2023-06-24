import urllib
from pathlib import PurePosixPath
from uuid6 import uuid6


def append_prefix(path: str, prefix: str = None) -> str:
    active_path = PurePosixPath(path)

    if active_path.is_absolute():
        active_path = PurePosixPath(*active_path.parts[1:])

    result_path: PurePosixPath = PurePosixPath(prefix, active_path) if prefix else active_path
    return str(result_path)


def get_parent_path(path: str) -> str:
    return str(PurePosixPath(path).parent)


def create_folder_path(path: str) -> str:
    return str(PurePosixPath(path)) + '/'


def build_object_url(endpoint_url, bucket, path, **params) -> str:
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urllib.parse.urlparse(endpoint_url))
    url_parts[2] = str(PurePosixPath(bucket, path))

    url_parts[4] = urllib.parse.urlencode(params)
    return urllib.parse.urlunparse(url_parts)


def create_uniq_identifier_for_file() -> str:
    return str(uuid6())


def create_path_for_file_forecasted() -> str:
    # /local/files_for_forecasting/<uuid6>.jpg
    filename = 'forecasted_files/' + create_uniq_identifier_for_file() + '.csv'
    return str(PurePosixPath(filename))
