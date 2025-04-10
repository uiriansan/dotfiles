import gi

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0", "GtkLayerShell": "0.1"})
from gi.repository import Gdk, Gtk, GtkLayerShell

from fabric.hyprland.service import Hyprland
from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow


class Popover(WaylandWindow):
    def __init__(self, monitor, **kwargs):
        super().__init__(
            name="layer-shell-overlay",
            style_classes="layer-shell-overlay",
            monitor=monitor,
            title="brightness-overlay",
            pass_through=False,
            anchor="left top right bottom",
            margin="-50px 0px 0px 0px",
            exclusivity="auto",
            layer="overlay",
            type="top-level",
            visible=False,
            all_visible=False,
            style="background-color: rgba(0,0,0,.8);",
            **kwargs,
        )

        self.set_events(
            Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK
        )
        self.connect("event", self.test)

        self.children = Box(style_classes="body-box")

        self.show_all()

    def test(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            print(f"Clicked at {event.x}x{event.y}")
