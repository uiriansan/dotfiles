from typing import Literal

import gi

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0"})

from gi.repository import Gdk, Gtk

from fabric.utils.helpers import bulk_connect


# https://github.com/rubiin/HyDePanel/blob/f86a593eacc699dbefb110a220a25c8b840723d9/utils/widget_utils.py#L37
def setup_cursor_hover(
    widget, cursor_name: Literal["pointer", "crosshair", "grab"] = "pointer"
):
    display = Gdk.Display.get_default()

    def on_enter_notify_event(widget, _):
        cursor = Gdk.Cursor.new_from_name(display, cursor_name)
        widget.get_window().set_cursor(cursor)

    def on_leave_notify_event(widget, _):
        cursor = Gdk.Cursor.new_from_name(display, "default")
        widget.get_window().set_cursor(cursor)

    bulk_connect(
        widget,
        {
            "enter-notify-event": on_enter_notify_event,
            "leave-notify-event": on_leave_notify_event,
        },
    )

    return widget


def get_widget_geometry(widget: Gtk.Widget) -> tuple[int, ...]:
    pass


def get_widget_screen_position(widget: Gtk.Widget) -> tuple[int, int]:
    toplevel = widget.get_toplevel()
    if not toplevel and toplevel.is_toplevel():
        return 0, 0

    allocation = widget.get_allocation()
    x, y = widget.translate_coordinates(toplevel, allocation.x, allocation.y) or (
        0,
        0,
    )
    return round(x / 2), round(y / 2)


def get_widget_position(widget: Gtk.Widget) -> tuple[int, ...]:
    pass
