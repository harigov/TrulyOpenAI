from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Type

from configurable import Configurable


class ConnectorType(Enum):
    LLM = 0
    Mail = 1
    Message = 2
    Calendar = 3
    TodoList = 4
    Note = 5
    FileStorage = 6
    AddressBook = 7
    RetailStore = 8
    SocialMedia = 9
    SearchEngine = 10
    InformationSource = 11
    TextToSpeech = 12
    SpeechToText = 13

class BaseConnector(ABC):
    @property
    @abstractmethod
    def id(self):
        """Connector might be instantiated multiple times, so we use id to
        distinguish them."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def connector_type(self) -> ConnectorType:
        raise NotImplementedError()

    @abstractmethod
    def get_configurables(self) -> List[Configurable]:
        raise NotImplementedError()


class ConnectorRegistry:
    """Registry for connectors.

    This class is responsible for registering and retrieving connectors.
    Connectors are usually registered during plugin initialization.
    """

    def __init__(self):
        self._connector_types = {}

    def register(self, connector: Type):
        self._connector_types[connector.name] = connector

    def get(self, name):
        return self._connector_types[name]

    def get_all(self):
        return list(self._connector_types.values())
