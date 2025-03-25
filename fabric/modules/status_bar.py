from gi.repository import Gdk, Gtk

from fabric.system_tray.widgets import SystemTray
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.datetime import DateTime
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow as Window
from widgets import popover
from widgets.icon_button import IconButton
from widgets.popover import PopoverWindow


class StatusBar(Window):
    def __init__(self, monitor, main_monitor_id):
        super().__init__(
            name="status-bar",
            monitor=monitor,
            main_monitor_id=main_monitor_id,
            layer="top",
            anchor="left top right",
            margin="10px 10px -2px 10px",
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        self.system_button = IconButton(icon="arch")
        self.power_button = IconButton(icon="power")

        self.system_tray = (
            SystemTray(name="system-tray", spacing=0, icon_size=16)
            if monitor == main_monitor_id
            else Box()
        )

        self.datetime = DateTime(formatters=["%a %H:%M"], name="datetime")

        self.toolbar = Box()

        popover = PopoverWindow(
            parent=self,
            child=Box(
                children=[Label(label="This is a test!")], style_classes="popover-box"
            ),
            visible=False,
            all_visible=False,
            pointing_to=self.datetime,
            margin="10 0 0 0",
        )

        popover2 = PopoverWindow(
            parent=self,
            child=Box(
                children=[Label(label="This is a test!")], style_classes="popover-box"
            ),
            visible=False,
            all_visible=False,
            pointing_to=self.system_button,
            margin="10 0 0 0",
        )

        popover3 = PopoverWindow(
            parent=self,
            child=Box(
                children=[Label(label="This is a test!")], style_classes="popover-box"
            ),
            visible=False,
            all_visible=False,
            pointing_to=self.power_button,
            margin="10 0 0 0",
        )

        self.datetime.connect(
            "clicked",
            lambda *_: popover.set_visible(not popover.get_visible()),
        )

        self.system_button.connect(
            "clicked",
            lambda *_: popover2.set_visible(not popover2.get_visible()),
        )

        self.power_button.connect(
            "clicked",
            lambda *_: popover3.set_visible(not popover3.get_visible()),
        )

        self.set_events(
            Gdk.EventMask.POINTER_MOTION_MASK
            | Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
        )

        self.connect("event", self.on_gevent)

        # Gdk.Seat.grab(
        #     Gdk.Display.get_default().get_default_seat(),
        #     self,
        #     Gdk.SeatCapabilities.POINTER,
        #     True,
        #     None,
        #     Gdk.EventType.BUTTON_PRESS,
        #     None,
        # )

        self.add_events("button-press")

        self.children = CenterBox(
            name="status-bar-container",
            start_children=Box(
                name="start-container",
                spacing=0,
                orientation="h",
                children=[self.system_button, Gtk.Separator(), self.system_tray],
            ),
            center_children=Box(
                name="center-container",
                spacing=0,
                orientation="h",
                children=[self.datetime],
            ),
            end_children=Box(
                name="end-container",
                spacing=0,
                orientation="h",
                children=[self.toolbar, Gtk.Separator(), self.power_button],
            ),
        )

        self.show_all()

    def on_gevent(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            pass
