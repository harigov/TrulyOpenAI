from typing import List
import attr
from abc import abstractmethod

from connector import BaseConnector, ConnectorType
from types import Text, Integer


@attr.s
class Note:
    id = attr.ib(type=str)
    title = attr.ib(type=str)
    content = attr.ib(type=str)


class BaseNoteConnector(BaseConnector):
    @property
    def connector_type(self) -> ConnectorType:
        return ConnectorType.Note

    @abstractmethod
    def get_notes(self, path: Text, limit: Integer = 10) -> List[Note]:
        raise NotImplementedError()

    @abstractmethod
    def create_note(self, note: Note):
        raise NotImplementedError()

    @abstractmethod
    def update_note(self, note: Note):
        raise NotImplementedError()

    @abstractmethod
    def delete_note(self, note: Note):
        raise NotImplementedError()
