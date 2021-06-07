import io
import typing
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type


class FileSystem(ABC):
    @classmethod
    def get_filesystem(cls, schema: str) -> 'FileSystem':
        for sub in FileSystem.__subclasses__():  # type: Type[FileSystem]
            if sub.services(schema):
                return sub()
        raise ValueError(f'No filesystem registered for "{schema}"')

    @classmethod
    @abstractmethod
    def services(cls, schema: str) -> bool:
        pass

    @abstractmethod
    def open(self, filename) -> typing.BinaryIO:
        pass


class LocalFileSystem(FileSystem):
    @classmethod
    def services(cls, schema: str) -> bool:
        return not schema

    def open(self, filename) -> typing.BinaryIO:
        path = str(Path(filename).expanduser())
        return open(path, 'rb')


class S3FileSystem(FileSystem):
    @classmethod
    def services(cls, schema: str) -> bool:
        return schema == 's3'

    def open(self, filename) -> typing.BinaryIO:
        try:
            import s3fs
        except ImportError:
            raise ImportError("s3fs required for s3 files")
        return s3fs.S3FileSystem().open(filename, mode='rb')


class HTTPFileSystem(FileSystem):
    @classmethod
    def services(cls, schema: str) -> bool:
        return schema in ('http', 'https')

    def open(self, filename) -> typing.BinaryIO:
        try:
            import requests
        except ImportError:
            raise ImportError("requests required for s3 files")
        # TODO: stream contents from the response obj with stream=True
        response = requests.get(filename)
        response.raise_for_status()
        return io.BytesIO(response.content)
