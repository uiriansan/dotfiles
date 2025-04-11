import socket

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from utils.widgets import setup_cursor_hover
from widgets.common_button import CommonButton
from widgets.icon_button import IconButton


class Tool(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Toolbar(Box):
    def __init__(self, **kwargs):
        super().__init__(spacing=5, **kwargs)

        self.children = [
            IconButton(icon="vinyl", title="Media player"),
            setup_cursor_hover(
                Button(
                    child=Box(
                        orientation="h",
                        spacing=2,
                        children=[
                            Image(
                                icon_name="color-picker-symbolic",
                                icon_size=14,
                            ),
                            Label(label=" #FF0000"),
                        ],
                    ),
                )
            ),
            IconButton(icon="magnifier", title="Magnifier"),
            IconButton(icon="screenshot", title="Screenshot"),
            IconButton(icon="recorder", title="Record screen"),
            IconButton(icon="system-monitor", title="System monitor"),
            IconButton(icon="brightness", title="Blue light filter"),
            IconButton(icon="volume-max", title=f"Volume: 100%"),
            CommonButton(
                icon="ethernet",
                title=f"Ethernet | IPv4 {socket.gethostbyname(socket.gethostname())}",
                l_popover_factory=lambda: Label(label="Lorem ipsum dolor sit amet"),
            ),
        ]

        self.show_all()
