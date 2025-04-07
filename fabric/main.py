import gi

from utils.devices import get_all_monitors

gi.require_version("Gtk", "3.0")
from multiprocessing import Process

from gi.repository import Gtk
from loguru import logger
from setproctitle import setproctitle

from config import MAIN_MONITOR_ID
from fabric import Application
from fabric.utils import get_relative_path
from modules.launcher import Launcher
from modules.status_bar import StatusBar

if __name__ == "__main__":
    setproctitle("fabric-shell")

    logger.add("fabric_shell.log")

    # Set custom `-symbolic.svg` icons' dir
    icon_theme = Gtk.IconTheme.get_default()
    icons_dir = get_relative_path("./assets/icons/")
    icon_theme.append_search_path(icons_dir)

    launcher = Launcher()
    status_bars = []

    monitors = get_all_monitors()
    for monitor in monitors:
        status_bar = StatusBar(monitor["id"], MAIN_MONITOR_ID)
        status_bars.append(status_bar)

        logger.info(
            f"Added `status-bar` for monitor {monitor['id']} ({monitor['name']})."
        )

    logger.info(f"Added `launcher`.")

    app = Application("shell", *status_bars, launcher)

    app.set_stylesheet_from_file(get_relative_path("./styles/global.css"))
    app.run()
