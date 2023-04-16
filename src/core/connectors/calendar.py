import attr
from abc import abstractmethod
from typing import List

from connector import BaseConnector, ConnectorType
from types import DateTime, Email, Integer, Text


@attr.s
class Calendar:
    id = attr.ib(type=Text)
    name = attr.ib(type=Text)
    description = attr.ib(type=Text, default="")

@attr.s
class CalendarEvent:
    calendar_id = attr.ib(type=Text)
    title = attr.ib(type=Text)
    start_time = attr.ib(type=DateTime)
    end_time = attr.ib(type=DateTime)
    is_recurring = attr.ib(type=bool, default=False)
    participants = attr.ib(type=List[Email], default=[])


class BaseCalendarConnector(BaseConnector):
    @property
    def connector_type(self) -> ConnectorType:
        return ConnectorType.Calendar

    @abstractmethod
    def get_events(self, since: DateTime, limit: Integer = 10) -> List[CalendarEvent]:
        raise NotImplementedError()

    @abstractmethod
    def create_event(self, event: CalendarEvent):
        raise NotImplementedError()

    @abstractmethod
    def update_event(self, event: CalendarEvent):
        raise NotImplementedError()

    @abstractmethod
    def delete_event(self, event: CalendarEvent):
        raise NotImplementedError()

    @abstractmethod
    def get_calendars(self) -> List[Calendar]:
        raise NotImplementedError()
