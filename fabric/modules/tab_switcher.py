import json

import pyscreenshot as ImageGrab

from fabric.hyprland.service import Hyprland
from fabric.utils import bulk_connect
from fabric.widgets.wayland import WaylandWindow as Window

connection: Hyprland | None = None
visible_workspaces = {}

IMAGE_DIR = "/tmp/fabric_shell"


# Set border for specific window:
# Focus window
# hyprctl dispatch focuswindow address:0x<window_address>


def get_hyprland_connection() -> Hyprland:
    global connection
    if not connection:
        connection = Hyprland()

    return connection


def get_visible_windows():
    pass


class TabSwitcher(Window):
    def __init__(self):
        super().__init__(monitor=1, name="tab-switcher")

        hypr_clients = json.loads(Hyprland.send_command("j/clients").reply)
        active_client = self.get_active_client(hypr_clients)
        print(active_client)

        focused_client = {}
        # focused_address = focused_client["address"]
        focused_address = active_client["address"]

        some = json.loads(
            Hyprland.send_command(
                f"/dispatch focuswindow address:0x{focused_address}"
            ).reply
        )

        print(some)

        # json.loads(
        #     Hyprland.send_command(
        #         f"/dispatch setprop address:0x{focused_address} bordersize 2"
        #     ).reply
        # )

        # bulk_connect(
        #     self.connection,
        #     {
        #         "event::workspacev2": self.update_visible_workspaces,
        #         "event::focusedmonv2": self.update_visible_workspaces,
        #         "event::fullscreen": self.update_visible_workspaces,
        #         "event::activespecialv2": self.update_visible_workspaces,
        #     },
        # )

    def get_active_client(self, clients):
        return [c for c in clients if c["focusHistoryID"] == 0][0]

    # def update_visible_workspaces(self, _, event):
    #     print(event.data)
    #     shot_workspace()
    #
    # def shot_workspace(self):
    #     hyprland_clients = json.loads(Hyprland.send_command("j/clients").reply)
    #
    #     for i, client in enumerate(hyprland_clients):
    #         x = client["at"][0]
    #         y = client["at"][1]
    #         w = client["size"][0]
    #         h = client["size"][1]
    #
    #         x2 = w + x
    #         y2 = h + y
    #
    #         screenshot = ImageGrab.grab(bbox=(x, y, x2, y2))
    #
    #         win_addr = client["address"]
    #
    #         screenshot.save(f"{IMAGE_DIR}/{win_addr}.jpg")


from fabric import Application

if __name__ == "__main__":
    tab_switcher = TabSwitcher()
    app = Application("tab-switcher", tab_switcher)
    app.run()
