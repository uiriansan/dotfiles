import json

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from loguru import logger

from fabric import Application
from fabric.hyprland.service import Hyprland
from fabric.utils import get_relative_path
from modules.status_bar import StatusBar

MAIN_MONITOR_ID = 0

if __name__ == "__main__":
    icon_theme = Gtk.IconTheme.get_default()

    icons_dir = get_relative_path("./assets/icons/")
    icon_theme.append_search_path(icons_dir)

    monitors = json.loads(Hyprland.send_command("j/monitors").reply)

    app = None
    for monitor in monitors:
        status_bar = StatusBar(monitor["id"], MAIN_MONITOR_ID)
        app = Application("status-bar", status_bar)

        logger.info(
            f"Added `status-bar` for monitor {monitor['id']} ({monitor['name']})."
        )

    if app:
        app.set_stylesheet_from_file(get_relative_path("./styles/global.css"))
        app.run()
