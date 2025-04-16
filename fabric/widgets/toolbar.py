import socket

import gi
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from utils import widgets
from utils.widgets import setup_cursor_hover
from widgets.common_button import CommonButton
from widgets.icon_button import IconButton

gi.require_versions({"Gtk": "3.0"})
from gi.repository import Gtk


class Tool(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Toolbar(Box):
    def __init__(self, **kwargs):
        super().__init__(spacing=5, **kwargs)

        self.children = []

        self.show_all()

    def add_widget(self, widget: Gtk.Widget):
        self.add(widget)
