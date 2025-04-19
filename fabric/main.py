import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from loguru import logger
from setproctitle import setproctitle
from config import SHELL_NAME
from fabric.utils import get_relative_path
from modules.shell import Shell

if __name__ == "__main__":
    setproctitle(SHELL_NAME)

    logger.configure(
        handlers=[
            {
                "sink": sys.stderr,
                "format": "<level>{level}</level> -> <bold>{message}</bold>",
            }
        ],
        extra={"reqid": "-", "ip": "-", "user": "-"},
    )
    logger.add(
        f"{SHELL_NAME}.log",
        level="WARNING",
        format="<level>{level}</level>::<green>{time:DD-MM-YYYY | HH:mm:ss}</green> -> {message}",
    )

    # Set custom `-symbolic.svg` icons' dir
    icon_theme = Gtk.IconTheme.get_default()
    icons_dir = get_relative_path("./data/icons/")
    icon_theme.append_search_path(icons_dir)

    shell = Shell(SHELL_NAME)
    shell.run()
