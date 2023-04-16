from typing import List
import attr
from abc import ABC, abstractmethod

from connector import ConnectorType, BaseConnector
from types import DateTime, Email, Integer, Text


@attr.s
class EmailMessage:
    to = attr.ib(type=List[Email])
    cc = attr.ib(type=List[Email], default=[])
    bcc = attr.ib(type=List[Email], default=[])
    subject = attr.ib(type=Text)
    body = attr.ib(type=Text)
    attachments = attr.ib(type=List[Text], default=[])

class BaseEmailConnector(BaseConnector):
    @property
    def connector_type(self) -> ConnectorType:
        return ConnectorType.Mail

    @abstractmethod
    def get_emails(self, since: DateTime, limit: Integer = 10) -> List[EmailMessage]:
        raise NotImplementedError()

    @abstractmethod
    def send_email(self, email: EmailMessage):
        raise NotImplementedError()
