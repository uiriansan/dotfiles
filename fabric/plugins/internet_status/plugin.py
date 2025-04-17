import gi
from fabric.utils import bulk_connect, get_relative_path
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from utils.plugins import ToolbarPlugin
from widgets.common_button import CommonButton

class InternetStatus(ToolbarPlugin):
    def __init__(self):
        self._name = "internet_status"
        self._description = "Show internet status button."

        self.shell_context = None

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path(get_relative_path("./styles.css"))

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
            # on_click=lambda: self._on_click(button),
        )

        button_style_context = button.get_style_context()
        button_style_context.add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        bulk_connect(
            button,
            {
                "enter-notify-event": self._on_enter_notify_event,
                "leave-notify-event": self._on_leave_notify_event,
            },
        )

        return button

    def _on_enter_notify_event(self, widget, event):
        self._on_click(widget)

    def _on_leave_notify_event(self, widget, event):
        self._unreveal(widget)

    def _unreveal(self, button):
        button.unreveal()
        return False

    def _on_click(self, button):
        button.reveal()
        return False
