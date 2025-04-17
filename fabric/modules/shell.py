from loguru import logger
import gi
gi.require_versions({"Gtk": "3.0"})
from gi.repository import Gtk
from fabric.core.application import Application
from fabric.utils import get_relative_path
from config import MAIN_MONITOR_ID
from modules.launcher import Launcher
from modules.status_bar import StatusBar
from utils.devices import get_all_monitors
from utils.plugins import PluginManager, ShellContext
from typing import List

class Shell(Application):
    def __init__(
        self,
        name: str,
        *windows: Gtk.Window,
    ):
        launcher = Launcher()
        logger.debug("[Shell] Added `launcher`.")

        status_bars: List[StatusBar] = []

        monitors = get_all_monitors()
        for monitor in monitors:
            status_bar = StatusBar(monitor["id"], MAIN_MONITOR_ID)
            status_bars.append(status_bar)

            logger.debug(
                f"[Shell] Added `status-bar` for monitor {monitor['id']} ({monitor['name']})."
            )

        super().__init__(name, *status_bars, launcher, *windows)

        self.status_bars = status_bars
        self.launcher = launcher
        self.context = ShellContext(self.status_bars, self.launcher)

        self.plugin_manager = PluginManager()

        self.plugin_manager.get_plugins()
        self.plugin_manager.initialize_plugins(self.context)

        self.set_stylesheet_from_file(get_relative_path("../styles/global.css"))

        # Create a reference of the plugins for each status bar. Not the best idea, but make plugins a lot easier to work with.
        # TODO: REALLY GOTTA FIX THIS
        for bar in self.status_bars:
            self._load_toolbar_widgets(bar)

        self._connect_launcher()

    def _load_toolbar_widgets(self, bar):
        widgets = self.plugin_manager.get_toolbar_widgets()
        toolbar = bar.toolbar

        for _, widget in widgets.items():
            toolbar.add_widget(widget)

    def _connect_launcher(self):
        self.launcher._connect()

    def toggle_launcher(self):
        self.launcher.toggle()

    def toggle_launcher_with_command(self, command: str):
        self.launcher.toggle()
        self.launcher.launch(command)
