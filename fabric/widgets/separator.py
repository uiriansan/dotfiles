from fabric.widgets.widget import Literal
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Separator(Gtk.Separator):
    def __init__(self, orientation: Literal["h", "v"] = "h", margins: bool = True):
        self._orientation = orientation
        self._gtk_orientation = Gtk.Orientation.HORIZONTAL if self._orientation == "h" else Gtk.Orientation.VERTICAL
        self._margins = margins

        super().__init__(orientation=self._gtk_orientation)

        if self._orientation == "h":
            self.set_size_request(-1, 0)
            self.set_hexpand(True)
            self.set_vexpand(False)
        else:
            self.set_size_request(0, -1)
            self.set_vexpand(True)
            self.set_hexpand(False)

        self._style_context = self.get_style_context()
        self._style_context.add_class("separator")
        if not self._margins:
            self._style_context.add_class("no-margins")
