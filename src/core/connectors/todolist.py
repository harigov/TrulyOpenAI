from typing import List
import attr
from abc import abstractmethod

from connector import BaseConnector, ConnectorType
from types import Text, Integer


@attr.s
class TodoList:
    id = attr.ib(type=str)
    name = attr.ib(type=str)
    description = attr.ib(type=str)

@attr.s
class TodoItem:
    id = attr.ib(type=str)
    list_id = attr.ib(type=str)
    title = attr.ib(type=str)
    description = attr.ib(type=str)
    due_date = attr.ib(type=str)
    completed = attr.ib(type=bool)


class BaseTodoListConnector(BaseConnector):
    @property
    def connector_type(self) -> ConnectorType:
        return ConnectorType.TodoList

    @abstractmethod
    def get_todo_lists(self) -> List[TodoList]:
        raise NotImplementedError()

    @abstractmethod
    def create_todo_list(self, todo_list: TodoList):
        raise NotImplementedError()

    @abstractmethod
    def update_todo_list(self, todo_list: TodoList):
        raise NotImplementedError()

    @abstractmethod
    def delete_todo_list(self, todo_list: TodoList):
        raise NotImplementedError()

    @abstractmethod
    def get_todo_items(self, todo_list: TodoList) -> List[TodoItem]:
        raise NotImplementedError()

    @abstractmethod
    def create_todo_item(self, todo_item: TodoItem):
        raise NotImplementedError()

    @abstractmethod
    def update_todo_item(self, todo_item: TodoItem):
        raise NotImplementedError()

    @abstractmethod
    def delete_todo_item(self, todo_item: TodoItem):
        raise NotImplementedError()

    @abstractmethod
    def complete_todo_item(self, todo_item: TodoItem):
        raise NotImplementedError()

    @abstractmethod
    def uncomplete_todo_item(self, todo_item: TodoItem):
        raise NotImplementedError()