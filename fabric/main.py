import gi

from utils.devices import get_all_monitors
from utils.shell import Shell

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

    logger.add("fabric_shell.log", level="WARNING")

    # Set custom `-symbolic.svg` icons' dir
    icon_theme = Gtk.IconTheme.get_default()
    icons_dir = get_relative_path("./assets/icons/")
    icon_theme.append_search_path(icons_dir)

    # from plugins.gepeto.plugin import gepeto
    # print(gepeto("What is your model?"))

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

    shell = Shell("fabric-shell", status_bars, launcher)

    shell.set_stylesheet_from_file(get_relative_path("./styles/global.css"))
    shell.run()
