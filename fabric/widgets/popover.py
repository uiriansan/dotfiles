# https://github.com/rubiin/HyDePanel/blob/master/shared/pop_over.py

import contextlib
import json

import gi

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0", "GtkLayerShell": "0.1"})
from gi.repository import Gdk, Gtk, GtkLayerShell

from fabric.hyprland.service import Hyprland
from fabric.widgets.overlay import Overlay
from fabric.widgets.wayland import WaylandWindow
from utils.devices import get_monitor_geometry_from_widget
from utils.widgets import get_widget_geometry, get_widget_screen_position


class PopoverWindow(WaylandWindow):
    def __init__(
        self,
        parent: WaylandWindow,
        content: Gtk.Widget,
        pointing_to: Gtk.Widget | None = None,
        margin: tuple[int, ...] | str = "0 0 0 0",
        **kwargs,
    ):
        super().__init__(
            name="popover",
            style_classes="popover",
            anchor="left top right bottom",
            margin=(0, 0, 0, 0),
            type="popup",
            layer="overlay",
            exclusivity="auto",
            **kwargs,
        )

        self.fullscreen()

        self._parent = parent
        self._content = content
        self._pointing_widget = pointing_to
        self._base_margin = self.extract_margin(margin)
        # self.margin = self._base_margin.values()

        # self.display = Gdk.Display.get_default()

        # self.connect("notify::visible", self.toggle)

        # self.ov = Gtk.Overlay()
        # self.ov.add(self._content)

        # self.ov.add_overlay(self._parent)
        # self.ov.add_overlay(self._content)
        # self.ov.set_overlay_pass_through(self._content, True)

        # self.add(self.ov)
        # self.add(self._content)

        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        # This will be the event handler for mouse presses
        # self.connect("button-press-event", self.on_gevent)

    def on_gevent(self, _, event):
        print(event.type)
        if event.type == Gdk.EventType.BUTTON_PRESS:
            print("iosd")
            # self.close()
            # self.destroy()
