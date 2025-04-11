import gi

from fabric.widgets.wayland import WaylandWindow

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0", "GtkLayerShell": "0.1"})
from gi.repository import Gdk, GLib, Gtk, GtkLayerShell

from fabric.hyprland.service import Hyprland
from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow


class Popover(WaylandWindow):
    def __init__(self, content: Gtk.Widget, point_to: Gtk.Widget, **kwargs):
        super().__init__(
            name="popover-overlay",
            style_classes="popover-overlay",
            title="fabric-shell-popover-overlay",
            anchor="left top right bottom",
            margin="-50px 0px 0px 0px",
            exclusivity="auto",
            layer="overlay",
            type="top-level",
            visible=False,
            all_visible=False,
            style="background-color: rgba(0,0,0,.6);",
            **kwargs,
        )

        self._content = content
        self._point_to = point_to

        self._content_window = None
        self._visible = False

        # destroy popover if it stays hidden for 5 seconds
        self._destroy_timeout = None

        # Shut up, Gtk!
        self.add(Box())

    def open(self):
        if not self._content_window:
            self.create_popover()
        else:
            if self._destroy_timeout is not None:
                GLib.source_remove(self._destroy_timeout)
                self._destroy_timeout = None

            self.show_all()
            self._content_window.show_all()
            self._visible = True

    def create_popover(self):
        allocation = self._point_to.get_allocation()
        x = allocation.x
        y = allocation.y

        self._content_window = WaylandWindow(
            type="popup",
            layer="overlay",
            name="popover-window",
            anchor="left top",
            visible=False,
            all_visible=False,
            margin=[y, 0, 0, x],
        )

        GtkLayerShell.set_keyboard_interactivity(self._content_window, True)

        self._content_window.set_keep_above(True)

        self._content_window.add(
            Box(style_classes="popover-content", children=self._content)
        )

        self._content_window.connect("focus-out-event", self.on_popover_focus_out)
        self.connect("button-press-event", self.on_overlay_clicked)

        self.show_all()
        self._content_window.show_all()
        self._visible = True

    def on_overlay_clicked(self, widget, event):
        self.hide_popover()
        return True

    def on_popover_focus_out(self, widget, event):
        # This helps with keyboard focus issues
        GLib.timeout_add(100, self.hide_popover)
        self.hide_popover()
        return False

    def hide_popover(self):
        if self._content_window and self._visible:
            self._content_window.hide()
            self.hide()

        self._visible = False

        if not self._destroy_timeout:
            self._destroy_timeout = GLib.timeout_add(1000 * 5, self.destroy_popover)

        return False

    def destroy_popover(self):
        self._destroy_timeout = None
        self._visible = None

        self._content_window.hide()
        self._content_window.destroy()
        self._content_window = None

        self.hide()

        return False
