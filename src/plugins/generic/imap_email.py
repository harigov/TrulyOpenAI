from typing import List
from core.configurable import Configurable
from core.connector import ConnectorType
from core.connectors.email import BaseEmailConnector, EmailMessage
from core.types import DateTime, Email, Integer, Text


class IMAPEmailConnector(BaseEmailConnector):
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @property
    def id(self):
        return f"{self.host}:{self.port}"

    @property
    def name(self):
        return "IMAP Email"

    def get_configurables(self) -> List[Configurable]:
        return [
            Configurable(
                name="host",
                type=Text,
                value=self.host,
                description="IMAP server host"
            ),
            Configurable(
                name="port",
                type=Integer,
                value=self.port,
                description="IMAP server port"
            ),
            Configurable(
                name="username",
                type=Text,
                value=self.username,
                description="IMAP server username"
            ),
            Configurable(
                name="password",
                type=Password,
                value=self.password,
                description="IMAP server password"
            )
        ]

    def get_emails(self, since: DateTime, limit: Integer = 10) -> List[EmailMessage]:
        raise NotImplementedError()

    def send_email(self, email: EmailMessage):
        raise NotImplementedError()
