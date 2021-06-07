import binascii
import io
from contextlib import contextmanager
from gzip import GzipFile
from typing import BinaryIO, TextIO
from urllib.parse import urlparse

from openpy.filesystem import FileSystem


@contextmanager
def read(file_name: str) -> TextIO:
    """
    just open a file for reading (as text)
    Example:
    >>> with read('README.md') as f:
    >>>     contents = f.read()
    """
    parsed = urlparse(file_name)

    fs = FileSystem.get_filesystem(parsed.scheme)

    with fs.open(file_name) as source:
        with _compression_wrapper(file_name, source) as uncompressed:
            text = io.TextIOWrapper(uncompressed, encoding='utf-8')
            try:
                yield text
            finally:
                pass


def _compression_wrapper(file_name: str, f: BinaryIO):
    if file_name.endswith('.gz') or file_name.endswith('.gzip'):
        return GzipFile(fileobj=f)

    has_header = binascii.hexlify(f.read(2)) == b'1f8b'
    f.seek(0)
    if has_header:
        return GzipFile(fileobj=f)
    return f
