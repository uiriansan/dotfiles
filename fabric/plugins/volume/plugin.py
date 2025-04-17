from utils.plugins import ToolbarPlugin
from widgets.common_button import CommonButton


class InternetStatus(ToolbarPlugin):
    def __init__(self):
        self._name = "volume"
        self._description = "Show volume button."

        self.shell_context = None

    def initialize(self, shell_context):
        self.shell_context = shell_context

    def register_toolbar_widget(self):
        return CommonButton(
            name="volume-button", icon="volume-max", title="Volume: 100%"
        )
