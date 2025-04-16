from gi.repository import GLib

from utils.plugins import ToolbarPlugin
from widgets.common_button import CommonButton


class InternetStatus(ToolbarPlugin):
    def __init__(self):
        self._name = "Internet Status"
        self._description = "Show internet status button."

        self.shell_context = None

    def initialize(self, shell_context):
        self.shell_context = shell_context

    def register_toolbar_widget(self):
        # TODO: When loading the plugin, make sure it actually returns a Widget

        button = CommonButton(
            name="internet-status-button",
            icon="ethernet-off",
            title="Ethernet | IPv4: 192.168.0.1",
            label="No internet",
            revealed=False,
            on_click=lambda: self._on_click(button),
        )

        return button

    def _unreveal(self, button):
        button.unreveal()
        return False

    def _on_click(self, button):
        button.reveal()
        GLib.timeout_add(3000, lambda: self._unreveal(button))
        return False
