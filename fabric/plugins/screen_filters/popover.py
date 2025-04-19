from fabric.widgets.box import Box
from widgets.common_button import CommonButton
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from utils.widgets import setup_cursor_hover
from gi.repository import Gtk
from widgets.scale import Scale
from widgets.separator import Separator
from config import DEFAULT_BRIGHTNESS_VALUE, DEFAULT_BLUE_LIGHT_FILTER_VALUE

class ScreenFiltersPopover(Box):
    def __init__(self, filter_service, **kwargs):
        super().__init__(orientation="v", **kwargs)

        self.filter_service = filter_service

        self.blf_label = Label(label=f"{round(self.filter_service.blue_light)}K")
        self.blf_scale = Scale(
            min_value=self.filter_service.min_blue_light,
            max_value=self.filter_service.max_blue_light,
            value=self.filter_service.blue_light,
            step=500.0,
            orientation="h",
        )
        self.blf_scale.set_sensitive(self.filter_service.enabled)

        self.brightness_label = Label(label=f"{round(self.filter_service.brightness * 100)}%")
        self.brightness_scale = Scale(
            min_value=self.filter_service.min_brightness,
            max_value=self.filter_service.max_brightness,
            value=self.filter_service.brightness,
            step=0.05,
            orientation="h"
        )
        self.brightness_scale.set_sensitive(self.filter_service.enabled)

        self.reset_button = CommonButton(icon="refresh", icon_size=14, on_click=self.reset_filters, title="Reset filters")
        self.on_off_switch = Gtk.Switch(active=self.filter_service.enabled)
        self.on_off_switch.set_tooltip_text("Disable filters" if self.filter_service.enabled else "Enable filters")
        setup_cursor_hover(self.on_off_switch)

        # Store the signals to disconnect when the popover is destroyed!
        self.signal_handlers = []
        self.signal_handlers.extend([
            (
                self.filter_service,
                self.filter_service.connect("blue-light-changed", lambda _, value: self.blf_scale.set_value(value))
            ),
            (
                self.filter_service,
                self.filter_service.connect("brightness-changed", lambda _, value: self.brightness_scale.set_value(value))
            ),
            (
                self.blf_scale,
                self.blf_scale.connect("value-changed", self.update_blf_label)
            ),
            (
                self.brightness_scale,
                self.brightness_scale.connect("value-changed", self.update_brightness_label)
            ),
            (
                self.blf_scale,
                self.blf_scale.connect("button-release-event", self.set_blf_value)
            ),
            (
                self.brightness_scale,
                self.brightness_scale.connect("button-release-event", self.set_brightness_value)
            ),
            (
                self.on_off_switch,
                self.on_off_switch.connect("state-set", self.on_off_switch_changed)
            )
        ])
        # Disconnect the signals
        self.connect("destroy", self.on_destroy)

        self.children = [
            CenterBox(
                orientation="h",
                spacing=10,
                style_classes="padding-10",
                start_children=[
                    Label(label="Screen filters", style_classes="title")
                ],
                end_children=[
                    self.reset_button,
                    self.on_off_switch
                ]
            ),
            Separator(orientation="h", margins = False),
            Box(
                spacing=5,
                orientation="v",
                style_classes="padding-10",
                children=[
                    CenterBox(
                        start_children=Label(label="Blue Light"),
                        end_children=self.blf_label
                    ),
                    self.blf_scale
                ]
            ),
            Box(
                spacing=5,
                orientation="v",
                style_classes="padding-10 margin-bottom-10",
                children=[
                    CenterBox(
                        start_children=Label(label="Brightness"),
                        end_children=self.brightness_label
                    ),
                    self.brightness_scale
                ]
            ),
        ]

    def reset_filters(self):
        if self.filter_service.brightness == DEFAULT_BRIGHTNESS_VALUE and self.filter_service.blue_light == DEFAULT_BLUE_LIGHT_FILTER_VALUE:
            return
        self.filter_service.brightness = DEFAULT_BRIGHTNESS_VALUE
        self.filter_service.blue_light = DEFAULT_BLUE_LIGHT_FILTER_VALUE
        if self.filter_service.enabled:
            self.filter_service.shader_on()

    def on_off_switch_changed(self, switch, state):
        self.filter_service.enabled = state
        if state:
            self.filter_service.shader_on()
        else:
            self.filter_service.shader_off()

        self.brightness_scale.set_sensitive(state)
        self.blf_scale.set_sensitive(state)
        switch.set_tooltip_text("Disable filters" if state else "Enable filters")

    def update_blf_label(self, scale):
        self.blf_label.set_label(f"{round(scale.get_value())}K")

    def update_brightness_label(self, scale):
        self.brightness_label.set_label(f"{round(scale.get_value() * 100)}%")

    def set_blf_value(self, scale, _):
        value = scale.get_value()
        self.filter_service.blue_light = value
        self.filter_service.shader_on()

    def set_brightness_value(self, scale, _):
        value = scale.get_value()
        self.filter_service.brightness = value
        self.filter_service.shader_on()

    def on_destroy(self, widget):
        for obj, handler_id in self.signal_handlers:
            if obj and hasattr(obj, 'handler_disconnect'):
                obj.handler_disconnect(handler_id)
        self.signal_handlers = []
