from fabric.widgets.box import Box
from fabric.widgets.label import Label
from utils.plugins import LauncherPlugin, ToolbarPlugin
from widgets.common_button import CommonButton


class MyPlugin(ToolbarPlugin):
    def __init__(self):
        self._name = "example_plugin"
        self._description = (
            "Add a button to the toolbar that toggles the launcher on click."
        )

        self.shell_context = None

        self.popover_content = Box(
            orientation="v",
            children=[
                Label(label="This is a label inside a popover."),
                Label(label="Now try left clicking the button!"),
            ],
        )

    def initialize(self, shell_context):
        # This function is only called once
        self.shell_context = shell_context

    def get_button_popover(self):
        return self.popover_content

    def register_toolbar_widget(self):
        # This function is called for each status bar and must return a Gtk.Widget()
        button = CommonButton(
            name="example-plugin-button",
            icon="arch",
            title="Right click me!",
            label="Launcher opened!",
            revealed=False,  # initialize button with the label hidden
            # Do not use lambda to retrive `*_popover_factory`s! It creates a weak reference that can cause a seg fault.
            r_popover_factory=self.get_button_popover,
            on_click=lambda: self._on_click(button),
        )

        return button

    def _on_click(self, button):
        launcher = self.shell_context.get_launcher()
        launcher.toggle()

        if launcher.get_visible():
            button.add_style_class("pressed")
            button.reveal()
        else:
            button.remove_style_class("pressed")
            button.unreveal()

        return False
