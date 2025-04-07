import json

import gi

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0"})
from gi.repository import Gdk, Gtk

from fabric.hyprland.service import Hyprland


def get_all_monitors():
    return json.loads(Hyprland.send_command("j/monitors").reply)


def get_monitor_geometry(monitor_id: int) -> Gdk.Rectangle | None:
    screen = Gdk.Display.get_default().get_default_screen()
    return screen.get_monitor_geometry(monitor_id) or None


def get_monitor_geometry_from_widget(widget: Gtk.Widget) -> Gdk.Rectangle | None:
    window = widget.get_window()
    screen = Gdk.Display.get_default().get_default_screen()

    if window:
        monitor_id = screen.get_monitor_at_window(window)
        return screen.get_monitor_geometry(monitor_id)

    return None
