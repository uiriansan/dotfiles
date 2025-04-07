import gi

from utils.plugins import LauncherOptions, Plugin

from .utils import print_msg

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyPlugin(Plugin):
    def __init__(
        self,
        plugin_name: str,
        plugin_icon: str,
        popover: Gtk.Widget,
        launcher_menu: Gtk.Widget,
        launcher_options: LauncherOptions,
    ):
        super().__init__()

        print_msg("Hello from MyPlugin")
