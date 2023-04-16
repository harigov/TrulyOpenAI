from abc import ABC, abstractmethod
import importlib
import os
from typing import List

from configurable import Configurable

class BasePlugIn(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def enabled(self):
        raise NotImplementedError()

    @enabled.setter
    def enabled(self, value):
        raise NotImplementedError()

    @abstractmethod
    def get_configurables(self) -> List[Configurable]:
        raise NotImplementedError()

    @abstractmethod
    def init(self):
        raise NotImplementedError()

class PlugInRegistry:
    def __init__(self):
        self._plugins = []

    def load_plugins(self, path: str):
        for entry in os.scandir(path):
            if entry.is_file() and entry.name.endswith(".py"):
                module_name = entry.name[:-3]  # remove .py extension
                module_path = entry.path
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name in dir(module):
                    obj = getattr(module, name)
                    if isinstance(obj, type) and issubclass(obj, BasePlugIn):
                        plugin_instance = obj()
                        self.register_plugin(plugin_instance)
            elif entry.is_dir() and entry.name != "__pycache__":
                package_name = entry.name
                package_path = entry.path
                spec = importlib.util.spec_from_file_location(package_name, os.path.join(package_path, "__init__.py"))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name in dir(module):
                    obj = getattr(module, name)
                    if isinstance(obj, type) and issubclass(obj, BasePlugIn):
                        plugin_instance = obj()
                        self.register_plugin(plugin_instance)

    def register_plugin(self, plugin: BasePlugIn):
        self._plugins.append(plugin)

    def get_plugins(self) -> List[BasePlugIn]:
        return self._plugins

    def get_plugin_by_name(self, name: str) -> BasePlugIn:
        for plugin in self._plugins:
            if plugin.name == name:
                return plugin
        return None

    def enable_plugin(self, name: str):
        plugin = self.get_plugin_by_name(name)
        if plugin:
            plugin.enabled = True

    def disable_plugin(self, name: str):
        plugin = self.get_plugin_by_name(name)
        if plugin:
            plugin.enabled = False

    def init(self):
        for plugin in self._plugins:
            plugin.init()
