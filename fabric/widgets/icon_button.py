from fabric.widgets.button import Button
from fabric.widgets.image import Image
from utils.widgets import setup_cursor_hover


class IconButton(Button):
    def __init__(self, icon: str, icon_size=18, **kwargs):
        super().__init__(
            style_classes="icon-button",
            **kwargs,
        )
        self.icon = icon
        self.icon_size = icon_size

        setup_cursor_hover(self)
        self.set_icon(icon)

    def set_icon(self, icon, size=18):
        self.set_image(
            image=Image(
                icon_size=size, style_classes="icon", icon_name=f"{icon}-symbolic"
            )
        )
