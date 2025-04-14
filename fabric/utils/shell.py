import gi

from fabric.core.application import Application
from modules.launcher import Launcher
from modules.status_bar import StatusBar
from utils.plugins import PluginManager, ShellContext

gi.require_versions({"Gtk": "3.0"})
from typing import List

from gi.repository import Gtk


class Shell(Application):
    def __init__(
        self,
        name: str,
        status_bars: List[StatusBar],
        launcher: Launcher,
        *windows: Gtk.Window,
    ):
        super().__init__(name, *status_bars, launcher, *windows)

        self.status_bars = status_bars
        self.launcher = launcher
        self.context = ShellContext(self.status_bars, self.launcher)

        self.plugin_manager = PluginManager()
        self.plugin_manager.get_plugins()
        self.plugin_manager.initialize_plugins(self.context)

        self._load_toolbar_widgets()
        self._connect_launcher()

    def _load_toolbar_widgets(self):
        widgets = self.plugin_manager.get_toolbar_widgets()

        # FIX: Add the widget to both bars
        # Gtk-WARNING **: 17:55:57.693: Attempting to add a widget with type widgets+common_button+CommonButton to a container of type widgets+toolbar+Toolbar, but the widget is already inside a container of type widgets+toolbar+Toolbar, please remove the widget from its existing container first.
        for _, widget in widgets.items():
            for bar in self.status_bars:
                toolbar = bar.toolbar
                toolbar.add_widget(widget)

    def _connect_launcher(self):
        self.launcher._connect()
