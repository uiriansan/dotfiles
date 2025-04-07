import gi
from setproctitle import setproctitle

from config import MAIN_MONITOR_ID
from fabric.utils.helpers import get_relative_path

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0"})
from gi.repository import Gdk, Gtk
from loguru import logger

from fabric.core.application import Application
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow as Window
from utils.devices import get_all_monitors
from utils.widgets import setup_cursor_hover
from widgets.active_window import ActiveWindow
from widgets.datetime import DateTime
from widgets.icon_button import IconButton
from widgets.popover import PopoverWindow
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

        self._opened_popover = None

        self.system_button = IconButton(icon="arch", title="Arch Linux")
        self.active_window = ActiveWindow()

        self.system_tray = (
            SystemTray(name="system-tray", spacing=0, icon_size=16)
            if monitor == main_monitor_id
            else Box()
        )

        self.datetime = DateTime()

        self.toolbar = Toolbar()

        # self.system_button.connect(
        #     "clicked",
        #     lambda *_: popover2.present(),
        # )
        #
        # self.power_button.connect(
        #     "clicked",
        #     lambda *_: popover3.present(),
        # )

        # self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        # This will be the event handler for mouse presses
        # self.connect("button-press-event", self.on_gevent)

        # Gdk.Seat.grab(
        #     Gdk.Display.get_default().get_default_seat(),
        #     self,
        #     Gdk.SeatCapabilities.POINTER,
        #     True,
        #     None,
        #     Gdk.EventType.BUTTON_PRESS,
        #     None,
        # )

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
                            # Gtk.Separator(),
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

    def toggle(self):
        self.set_visible(not self.get_visible())

    #
    # def get_pointing_to(self, widget: Gtk.Widget) -> Gdk.Rectangle:
    #     # if not ((toplevel := widget.get_toplevel()) and toplevel.is_toplevel()):
    #     #     return 0, 0
    #
    #     return widget.get_allocation()
    #     # x, y = widget.translate_coordinates(toplevel, allocation.x, allocation.y) or (
    #     #     0,
    #     #     0,
    #     # )
    #     # return round(x / 2), round(y / 2)
    #
    # def close_opened_popover(self):
    #     if self._opened_popover:
    #         return self._opened_popover.close()
    #
    # def on_gevent(self, widget, event):
    #     print(event.type)
    #     if event.type == Gdk.EventType.BUTTON_PRESS:
    #         pass
    #         # self.close_opened_popover()
