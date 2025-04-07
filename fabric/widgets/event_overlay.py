import gi

from fabric.widgets.wayland import WaylandWindow as Window

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EventOverlay(Window):
    def __init__(self, content: Gtk.Widget, content_pos: tuple[int, int], **kwargs):
        super().__init__(self, style_classes="event-overlay", **kwargs)

        self._content = content
        self.children = content
