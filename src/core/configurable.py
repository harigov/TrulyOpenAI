from typing import List
import attr

@attr.s
class Configurable:
    name = attr.ib()
    type = attr.ib()
    default = attr.ib()
    value = attr.ib(default=None)
    required = attr.ib(default=False)

class ConfigurationManager:
    def __init__(self):
        self.configurables = []

    def add_configurable(self, configurable: Configurable):
        self.configurables.append(configurable)

    def get_configurable(self, name: str) -> Configurable:
        for configurable in self.configurables:
            if configurable.name == name:
                return configurable

    def get_configurables(self) -> List[Configurable]:
        return self.configurables

    def get_configurable_value(self, name: str):
        configurable = self.get_configurable(name)
        return configurable.value

    def set_configurable_value(self, name: str, value):
        configurable = self.get_configurable(name)
        configurable.value = value

    def get_configurable_default(self, name: str):
        configurable = self.get_configurable(name)
        return configurable.default

    def set_configurable_default(self, name: str, default):
        configurable = self.get_configurable(name)
        configurable.default = default

    def get_configurable_type(self, name: str):
        configurable = self.get_configurable(name)
        return configurable.type

    def set_configurable_type(self, name: str, type):
        configurable = self.get_configurable(name)
        configurable.type = type

    def get_configurable_name(self, name: str):
        configurable = self.get_configurable(name)
        return configurable.name

    def set_configurable_name(self, name: str):
        configurable = self.get_configurable(name)
        configurable.name = name