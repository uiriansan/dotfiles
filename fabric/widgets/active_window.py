import json
import re

from config import window_pattern_list, workspace_pattern_list
from fabric.hyprland.service import HyprlandEvent
from fabric.utils import bulk_connect
from fabric.widgets.button import Button
from utils.widgets import setup_cursor_hover
from utils.services import get_hyprland_connection

class ActiveWindow(Button):
    def __init__(self, **kwargs):
        super().__init__(name="active-window", **kwargs)

        setup_cursor_hover(self)

        self.connection = get_hyprland_connection()
        bulk_connect(
            self.connection,
            {
                "event::activewindow": self.on_active_window,
                "event::closewindow": self.on_active_window,
                "event::workspacev2": self.on_active_window,
                "event::focusedmonv2": self.on_active_window,
                "event::createworkspacev2": self.on_active_window,
                "event::destroyworkspacev2": self.on_active_window,
                "event::urgent": self.on_active_window,
            },
        )

        self.set_tooltip_text("Active window")

        self.get_window_data()

    def on_active_window(self, _, event: HyprlandEvent):
        return self.get_window_data()

    def get_window_data(self):
        win_data: dict = json.loads(
            self.connection.send_command("j/activewindow").reply.decode()
        )

        workspace_name_ref: dict = json.loads(
            self.connection.send_command("j/activeworkspace").reply.decode()
        )

        workspace_name = win_data.get("workspace", workspace_name_ref)["name"]

        win_class = win_data.get("class")
        win_title = win_data.get("title")
        win_initial_title = win_data.get("initialTitle")

        return self.set_label(
            f"{workspace_pattern_list.get(workspace_name, workspace_name.zfill(2))}   "
            + self.match_window_pattern(win_class, win_title, win_initial_title)
        )

    def match_window_pattern(
        self,
        win_class: str | None,
        win_title: str | None,
        win_initial_title: str | None,
    ) -> str:
        for pattern, result in window_pattern_list.items():

            match = None
            if (
                (match := re.match(pattern, f"class:{win_class}"))
                or (match := re.match(pattern, f"ititle:{win_initial_title}"))
                or (match := re.match(pattern, f"title:{win_title}"))
            ):
                final_title = result

                # TODO: Check if `result` includes "$" before loop the entire fucking group array

                if match:
                    for i in range(1, len(match.groups()) + 1):
                        group = match.group(i) or ""
                        final_title = final_title.replace(f"${i}", group)

                return final_title.strip()

        return ((win_title[:40] + "...") if len(win_title) > 40 else win_title) if win_title is not None else "Desktop"
