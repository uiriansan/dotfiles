import gi

from fabric.widgets.button import Button
from fabric.widgets.image import Image

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from loguru import logger

from utils.widgets import setup_cursor_hover


class StatusBarButton(Button):
    def __init__(
        self,
        icon: str | None = None,
        content: Gtk.Widget | None = None,
        primary_popover: Gtk.Widget | None = None,
        secondary_popover: Gtk.Widget | None = None,
        **kwargs,
    ):
        super().__init__(
            style_classes="icon-button status-bar-button",
            **kwargs,
        )

        if not content and not icon:
            logger.error(f"`status-bar-button` must contain either an icon or a widget")

        setup_cursor_hover(self)

        if content:
            self._content = content
            self.set_content()
        elif icon:
            self._icon = icon
            self._icon_size = 14
            self.set_icon()

    def set_icon(self, icon: str | None = None):
        ico = icon or self._icon
        self.set_image(
            image=Image(
                icon_size=self._icon_size,
                style_classes="icon",
                icon_name=f"{ico}-symbolic",
            )
        )

    def set_content(self, content: Gtk.Widget | None = None):
        self.add(content)
