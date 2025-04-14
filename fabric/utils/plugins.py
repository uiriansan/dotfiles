import abc

import gi
from loguru import logger

from config import MAIN_MONITOR_ID
from fabric.utils import get_relative_path

gi.require_versions({"Gtk": "3.0"})
import importlib.util
import os
import sys
from typing import Callable, Dict, List, Tuple

from gi.repository import Gtk


class Plugin(abc.ABC):
    """Base class for all plugins"""

    _name = None
    _description = None

    @property
    def name(self):
        if self._name is None:
            raise NotImplementedError("Subclasses must define _name")
        return self._name

    @property
    def description(self):
        if self._description is None:
            raise NotImplementedError("Subclasses must define _description")
        return self._description

    @abc.abstractmethod
    def initialize(self, shell_context) -> None: ...


class ToolbarPlugin(Plugin):
    """Interface for toolbar plugins"""

    @abc.abstractmethod
    def register_toolbar_widget(self) -> Gtk.Widget: ...


class LauncherPlugin(Plugin):
    """Interface for launcher plugins"""

    @abc.abstractmethod
    def get_commands(self) -> List[str]: ...

    @abc.abstractmethod
    def get_command_call(self, command: str) -> Dict[str, Callable]: ...

    @abc.abstractmethod
    def get_actions(self) -> List[Tuple[str, str, Callable]]: ...


class PluginManager:
    """Load and manages plugins"""

    def __init__(self):
        self.plugins_path = get_relative_path("../plugins")
        self.plugins: Dict[str, Plugin] = {}
        self.toolbar_plugins: Dict[str, ToolbarPlugin] = {}
        self.launcher_plugins: Dict[str, LauncherPlugin] = {}
        self.launcher_commands: Dict[str, str] = {}

    def get_plugins(self):
        if not os.path.exists(self.plugins_path):
            logger.error(
                f"Plugins path could not be resolved. Path: {self.plugins_path}"
            )
            return

        for dir_name in os.listdir(self.plugins_path):
            if dir_name.startswith("_"):
                continue

            plugin_path = os.path.join(self.plugins_path, dir_name)

            if not os.path.isdir(plugin_path):
                continue

            plugin_entry = os.path.join(plugin_path, "plugin.py")
            if not os.path.exists(plugin_entry):
                continue

            try:
                self._load_plugin_from_file(plugin_entry, dir_name)
            except Exception as e:
                logger.warning(f"Error loading plugin `{dir_name}`: {e}")

    def _load_plugin_from_file(self, plugin_entry_path: str, plugin_name: str):
        # Add plugin directory to sys.path temporarily
        plugin_path = os.path.dirname(plugin_entry_path)
        sys.path.insert(0, os.path.dirname(plugin_path))

        try:
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_name}.plugin", plugin_entry_path
            )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Plugin)
                    and attr not in (Plugin, ToolbarPlugin, LauncherPlugin)
                ):
                    plugin_instance = attr()
                    self.plugins[plugin_instance.name] = plugin_instance

                    if isinstance(plugin_instance, ToolbarPlugin):
                        self.toolbar_plugins[plugin_instance.name] = plugin_instance

                    if isinstance(plugin_instance, LauncherPlugin):
                        self.launcher_plugins[plugin_instance.name] = plugin_instance

                        for command in plugin_instance.get_commands():
                            self.launcher_commands[command] = plugin_instance.name

                    logger.info(
                        f"Added plugin `{plugin_instance.name}` from `{plugin_entry_path}`."
                    )
        finally:
            sys.path.pop(0)

    def initialize_plugins(self, shell_context):
        for plugin in self.plugins.values():
            try:
                plugin.initialize(shell_context)
            except Exception as e:
                logger.warning(f"Error initializing plugin `{plugin.name}`: {e}")

    def get_toolbar_widgets(self) -> Dict[str, Gtk.Widget]:
        widgets = {}
        for name, plugin in self.toolbar_plugins.items():
            try:
                widget = plugin.register_toolbar_widget()
                widgets[name] = widget
            except Exception as e:
                logger.warning(
                    f"Failed to register toolbar widget for plugin `{name}`: {e}"
                )

        return widgets

    # TODO: Launcher stuff


class ShellContext:
    """Provides plugins access to the shell components."""

    def __init__(self, status_bars, launcher):
        self._status_bars = status_bars
        self._main_status_bar = self.get_main_status_bar()
        self.launcher = launcher
        self.main_toolbar = self._main_status_bar.toolbar

    def get_launcher(self):
        return self.launcher

    def get_toolbar(self):
        return self.main_toolbar

    def get_main_status_bar(self):
        for bar in self._status_bars:
            if bar.monitor == MAIN_MONITOR_ID:
                return bar
