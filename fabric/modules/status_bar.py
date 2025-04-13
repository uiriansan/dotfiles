import gi

from widgets.common_button import CommonButton

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0", "GtkLayerShell": "0.1"})
import time

from gi.repository import Gdk, GLib, Gtk, GtkLayerShell

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow as Window
from utils.widgets import setup_cursor_hover
from widgets.active_window import ActiveWindow
from widgets.datetime import DateTime
from widgets.icon_button import IconButton
from widgets.popover import Popover, PopoverButton
from widgets.system_tray import SystemTray
from widgets.toolbar import Toolbar

############################################################################################
#                                                                                          #
#                                   Use Gtk.Menu()!!                                       #
#                           ...at least for the right click                                #
#                                                                                          #
############################################################################################


class StatusBar(Window):
    def __init__(self, monitor, main_monitor_id):
        super().__init__(
            name="status-bar",
            layer="top",
            monitor=monitor,
            anchor="left top right",
            margin="0px 0px -20px 0px",
            exclusivity="auto",
            # keyboard_mode="on-demand",
            visible=False,
            all_visible=False,
        )

        self._main_monitor_id = main_monitor_id

        self.system_button = CommonButton(
            icon="arch",
            title="Arch Linux",
            l_popover_factory=lambda: Button(child=Label(label="This is a label!!")),
            r_popover_factory=lambda: Button(
                child=Label(label="This is a label on the right click!!")
            ),
        )

        self.active_window = ActiveWindow()

        self.system_tray = (
            SystemTray(name="system-tray", spacing=0, icon_size=16)
            if monitor == main_monitor_id
            else Box()
        )

        self.datetime = DateTime()

        self.toolbar = Toolbar()

        self.children = Box(
            orientation="v",
            children=[
                CenterBox(
                    name="status-bar-container",
                    start_children=Box(
                        name="start-container",
                        spacing=0,
                        orientation="h",
                        children=[
                            self.system_button,
                            # Gtk.Separator(),
                            self.active_window,
                        ],
                    ),
                    center_children=Box(
                        name="center-container",
                        spacing=0,
                        orientation="h",
                        children=[
                            self.datetime,
                        ],
                    ),
                    end_children=Box(
                        name="end-container",
                        spacing=0,
                        orientation="h",
                        children=[
                            self.toolbar,
                            self.system_tray,
                        ],
                    ),
                ),
                CenterBox(
                    name="status-bar-corners",
                    start_children=Box(name="status-bar-corner-left"),
                    end_children=Box(name="status-bar-corner-right"),
                ),
            ],
        )

        self.show_all()

    def open_popover(self, _, event):
        self.datetime_popover.open()

    def toggle(self):
        self.set_visible(not self.get_visible())
