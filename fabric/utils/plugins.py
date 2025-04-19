import abc

import gi
from loguru import logger

from config import MAIN_MONITOR_ID, toolbar_plugin_order
from fabric.utils import get_relative_path

from modules.status_bar import StatusBar

gi.require_versions({"Gtk": "3.0"})
import importlib.util
import os
import sys
from typing import Callable, Dict, List, Tuple

from gi.repository import Gtk

class ShellContext:
    """Provides plugins access to shell's components."""

    def __init__(self, status_bars, launcher):
        self._status_bars = status_bars
        self._main_status_bar: StatusBar = self._get_main_status_bar()
        self.launcher = launcher
        self.main_toolbar = self._main_status_bar.toolbar

    def get_launcher(self):
        return self.launcher

    def get_toolbar(self):
        return self.main_toolbar

    def _get_main_status_bar(self) -> StatusBar:
        for bar in self._status_bars:
            if bar.get_monitor() == MAIN_MONITOR_ID:
                return bar

        return self._status_bars[0]

class Plugin(abc.ABC):
    """Base class for all plugins"""

    _name: str | None = None
    _description: str | None = None

    @property
    def name(self):
        if self._name is None:
            raise NotImplementedError("Plugins must define _name")
        return self._name

    @property
    def description(self):
        if self._description is None:
            raise NotImplementedError("Plugins must define _description")
        return self._description

    @abc.abstractmethod
    def initialize(self, shell_context: ShellContext) -> None: ...

    # TODO: Make these part of ShellContext
    # ShellContext.NotificationManager.notify(notification: Widget)
    # ShellContext.Calendar.add_event(event: Event)
    # ShellContext.JobManager.create_job(job: Job)

class ToolbarPlugin(Plugin):
    """
        Interface for toolbar plugins.
        Toolbar plugins can add interactive Gtk.Widgets to the toolbar (i.e., status bar far right)
    """

    @abc.abstractmethod
    def register_toolbar_widget(self) -> Gtk.Widget: ...

class LauncherPlugin(Plugin):
    """
        Interface for launcher plugins.
        Launcher plugins can register commands and add widgets and actions to them.
    """

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
                f"[Shell] Plugins path could not be resolved. Path: {self.plugins_path}"
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

            icons_path = os.path.join(plugin_path, "icons")
            if os.path.exists(icons_path) and os.path.isdir(icons_path):
                self._append_icons_path(icons_path)

            try:
                self._load_plugin_from_file(plugin_entry, dir_name)
            except Exception as e:
                logger.warning(f"[Shell] Error loading plugin `{dir_name}`: {e}")

    def _append_icons_path(self, icons_path):
        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.append_search_path(icons_path)

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
        finally:
            sys.path.pop(0)

    def initialize_plugins(self, shell_context: ShellContext):
        loaded_plugins = []
        for name, plugin in self.plugins.items():
            try:
                plugin.initialize(shell_context)
                loaded_plugins.append(name)
            except Exception as e:
                logger.warning(f"[Shell] Error initializing plugin `{plugin.name}`: {e}")

        logger.debug(f"[Shell] Loaded {len(loaded_plugins)} plugins: ({', '.join(loaded_plugins)})")

    def get_toolbar_widgets(self) -> Dict[str, Gtk.Widget]:
        # Sort toolbar widgets to follow the order defined in config.py
        if toolbar_plugin_order and len(toolbar_plugin_order) > 0:
            complete_order = [
                key for key in toolbar_plugin_order if key in self.toolbar_plugins
            ] + list(set(self.toolbar_plugins) - set(toolbar_plugin_order))
            plugins_in_order = {
                key: self.toolbar_plugins[key] for key in complete_order
            }
        else:
            plugins_in_order = self.toolbar_plugins

        widgets = {}
        for name, plugin in plugins_in_order.items():
            try:
                widget = plugin.register_toolbar_widget()
                widgets[name] = widget
            except Exception as e:
                logger.warning(
                    f"[Shell] Failed to register toolbar widget for plugin `{name}`: {e}"
                )

        return widgets
