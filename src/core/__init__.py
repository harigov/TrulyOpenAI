from configurable import Configurable, ConfigurationManager
from plugin import BasePlugIn, PlugInRegistry

def init():
    plugin_registry = PlugInRegistry()
    plugin_registry.load_plugins("src/plugins")
    config_mgr = ConfigurationManager("config.json")
    config_mgr.init_plugins()
    config_mgr.init_connectors()
