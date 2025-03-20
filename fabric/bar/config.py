from logging import NullHandler
import psutil
import json
from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.eventbox import EventBox
from fabric.widgets.datetime import DateTime
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.button import Button
from fabric.system_tray.widgets import SystemTray
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.hyprland.service import HyprlandEvent, Hyprland
from fabric.hyprland.widgets import Workspaces, WorkspaceButton, get_hyprland_connection
from fabric.utils import (
    FormattedString,
    bulk_replace,
    invoke_repeater,
    get_relative_path,
    truncate,
)
from fabric.utils.helpers import bulk_connect
from typing import Literal
from gi.repository import Gdk

AUDIO_WIDGET = True

if AUDIO_WIDGET is True:
    try:
        from fabric.audio.service import Audio
    except Exception as e:
        print(e)
        AUDIO_WIDGET = False


class VolumeWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio = Audio()

        self.progress_bar = CircularProgressBar(
            name="volume-progress-bar", pie=True, size=24
        )

        self.event_box = EventBox(
            events="scroll",
            child=Overlay(
                child=self.progress_bar,
                overlays=Label(
                    label="",
                    style="margin: 0px 6px 0px 0px; font-size: 12px",  # to center the icon glyph
                ),
            ),
        )

        self.audio.connect("notify::speaker", self.on_speaker_changed)
        self.event_box.connect("scroll-event", self.on_scroll)
        self.add(self.event_box)

    def on_scroll(self, _, event):
        match event.direction:
            case 0:
                self.audio.speaker.volume += 8
            case 1:
                self.audio.speaker.volume -= 8
        return

    def on_speaker_changed(self, *_):
        if not self.audio.speaker:
            return
        self.progress_bar.value = self.audio.speaker.volume / 100
        self.audio.speaker.bind(
            "volume", "value", self.progress_bar, lambda _, v: v / 100
        )
        return

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

class ActiveWindow(Button):
    def __init__(
        self,
        formatter: FormattedString = FormattedString(
            "{'Desktop' if not initial_title else truncate(initial_title, 42)}",
            truncate=truncate,
        ),
        # TODO: hint super's kwargs
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.connection = get_hyprland_connection()
        self.formatter = formatter

        setup_cursor_hover(self)

        bulk_connect(
            self.connection,
            {
                "event::activewindow": self.on_activewindow,
                "event::closewindow": self.on_closewindow,
                "event::workspacev2": self.on_activewindow,
                "event::windowmove": self.on_activewindow,
                "event::focusedmon": self.on_activewindow,
                "event::createworkspacev2": self.on_activewindow,
                "event::destroyworkspacev2": self.on_activewindow,
                "event::urgent": self.on_activewindow,
            },
        )

        # all aboard...
        if self.connection.ready:
            self.on_ready(None)
        else:
            self.connection.connect("event::ready", self.on_ready)

    def on_ready(self, _):
        return self.do_initialize()

    def on_closewindow(self, _, event: HyprlandEvent):
        if len(event.data) < 1:
            return
        return self.do_initialize()

    def on_activewindow(self, _, event: HyprlandEvent):
        if len(event.data) < 2:
            return

        win_data: dict = json.loads(
            self.connection.send_command("j/activewindow").reply.decode()
        )
        
        win_title = win_data.get("title", "unknown")
        initial_title = win_data.get("initialTitle", "NoInitialTitle")
        workspace: dict = win_data.get("workspace")

        print(workspace)

        # FIXME: Not properly updating when switching to an empty workspace
        try:
            return self.set_label(
                # self.formatter.format(win_title=event.data[0], initial_title=event.data[1])
                workspace.get("name").replace("special:", "") + " " + initial_title
            )
        except Exception as e:
            # "j/activeworkspace"?????????
            return self.set_label("Whatever")

    def do_initialize(self):
        win_data: dict = json.loads(
            self.connection.send_command("j/activewindow").reply.decode()
        )

        win_title = win_data.get("title", "unknown")
        initial_title = win_data.get("initialTitle", "NoInitialTitle")
        workspace = win_data.get("workspace")

        return self.set_label(
            initial_title
            # self.formatter.format(win_title=win_title, initial_title=initial_title)
        )


class StatusBar(Window):
    def __init__(
        self,
        monitor,
        main_monitor_id,
    ):
        super().__init__(
            name="bar",
            monitor=monitor,
            main_monitor_id=main_monitor_id,
            layer="top",
            anchor="left top right",
            margin="10px 20px -2px 20px",
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        self.workspaces = Workspaces(
            name="workspaces",
            spacing=4,
            buttons_factory=lambda ws_id: WorkspaceButton(id=ws_id, label=None),
        )
        self.active_window = ActiveWindow(name="hyprland-window", tooltip_text="Active window")
        self.date_time = DateTime(name="date-time")
        self.system_tray = SystemTray(name="system-tray", spacing=4) if monitor == main_monitor_id else Box()

        self.ram_progress_bar = CircularProgressBar(
            name="ram-progress-bar", pie=True, size=24
        )
        self.cpu_progress_bar = CircularProgressBar(
            name="cpu-progress-bar", pie=True, size=24
        )
        self.progress_bars_overlay = Overlay(
            child=self.ram_progress_bar,
            overlays=[
                self.cpu_progress_bar,
                Label("", style="margin: 0px 6px 0px 0px; font-size: 12px"),
            ],
        )

        self.status_container = Box(
            name="widgets-container",
            spacing=4,
            orientation="h",
            children=self.progress_bars_overlay,
        )
        self.status_container.add(VolumeWidget()) if AUDIO_WIDGET is True else None

        self.children = CenterBox(
            name="bar-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=self.workspaces,
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=self.active_window,
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[
                    self.status_container,
                    self.system_tray,
                    self.date_time,
                ],
            ),
        )

        invoke_repeater(1000, self.update_progress_bars)

        self.show_all()

    def update_progress_bars(self):
        self.ram_progress_bar.value = psutil.virtual_memory().percent / 100
        self.cpu_progress_bar.value = psutil.cpu_percent() / 100
        return True


if __name__ == "__main__":
    # Where to display the system tray:
    main_monitor_id = 1

    monitors = json.loads(Hyprland.send_command("j/monitors").reply)

    app: Application
    for monitor in monitors:
        # print("Adding bar for ", monitor["id"], monitor["name"])
        bar = StatusBar(monitor["id"], main_monitor_id)
        app = Application("bar", bar)
    
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    app.run()

