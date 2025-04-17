from fabric.widgets.box import Box
from utils.plugins import ToolbarPlugin
from widgets.common_button import CommonButton
from fabric.widgets.scale import Scale
from gi.repository import Gtk

class Brghtness(ToolbarPlugin):
    def __init__(self):
        self._name = "brightness"
        self._description = "Show brightness button."

        self.shell_context = None
        self.value = 5000

    def initialize(self, shell_context):
        self.shell_context = shell_context

    def get_popover_content(self):
        scale = Gtk.Scale.new_with_range(orientation=Gtk.Orientation.HORIZONTAL, min=2000, max=10000, step=500)
        scale.set_value(self.value)

        return Box(
            orientation="v",
            children=[
                scale
            ]
        )

    def register_toolbar_widget(self):
        return CommonButton(
            name="brightness-button", icon="brightness", title="Brightness", l_popover_factory=self.get_popover_content
        )
