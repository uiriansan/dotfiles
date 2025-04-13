import importlib.util
import inspect

plugin_class = None

for 
import os

from fabric.utils import get_relative_path
from modules.launcher import Launcher

type LauncherOptions = {}
type StatusBarActions = {}
type LauncherActions = {}


class Plugin:
    def __init__(self):
        super().__init__()


class LauncherContext:
    """Singleton that handles the Launcher's context and shared resources for plugins."""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        pass


# Launcher:
#   - Plugin register commands
#       command -> regex matching
#       command_type -> list | interactive
#       command_actions = action[] -> keybindings
#       command_factory -> callable


def load_plugins() -> [StatusBarActions | None, LauncherActions | None]:
    plugins_path = "../plugins"
    launcher_actions = []
    toolbar_buttons = []

    for plugin_dir in os.listdir(get_relative_path(plugins_path)):
        # Skip plugins starting with "_"
        if plugin_dir.startswith("_"):
            continue

        plugin_path = os.path.join(plugins_path, plugin_dir)

        if os.path.isdir(plugin_path):
            entry_file_path = os.path.join(plugin_path, "plugin.py")

            if os.path.exists(entry_file_path):
                spec = importlib.util.spec_from_file_location("plugin", entry_file_path)
                module = importlib.util.module_from_spec(spec)
                # spec.loader.exec_module(module)

                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Plugin) and obj is not Plugin:
                        plugin = obj
                        break

                # if hasattr(module, "get_launcher_actions"):
                #     launcher_actions.extend(module.get_launcher_actions())
                #     toolbar_actions.extend(module.get_toolbar_actions())

    return launcher_actions, toolbar_buttons


def execute_launcher_action(action: callable, context: LauncherContext):
    pass
