import gi

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0"})
from gi.repository import Gdk, Gtk

from fabric.widgets.box import Box


class Calendar(Box):
    def __init__(self, **kwargs):
        super().__init__(name="calendar", **kwargs)

        self.cal = Gtk.Calendar()

        self.add(self.cal)
