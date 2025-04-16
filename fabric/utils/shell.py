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
        for bar in self.status_bars:
            widgets = self.plugin_manager.get_toolbar_widgets()
            toolbar = bar.toolbar

            for _, widget in widgets.items():
                toolbar.add_widget(widget)

    def _connect_launcher(self):
        self.launcher._connect()
