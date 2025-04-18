import os
from fabric.core.service import Service, Property, Signal
from fabric.utils import exec_shell_command_async
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from utils.plugins import ToolbarPlugin
from utils.widgets import setup_cursor_hover
from widgets.common_button import CommonButton
from gi.repository import Gtk
from widgets.scale import Scale
from config import DEFAULT_BRIGHTNESS_VALUE, DEFAULT_BLUE_LIGHT_FILTER_VALUE, HYPRSHADE_SHADER_PATH
from widgets.separator import Separator

class FilterService(Service):
    @Signal
    def brightness_changed(self, value: float) -> None: ...
    @Signal
    def blue_light_changed(self, value: float) -> None: ...

    @Property(float, flags="read-write")
    def brightness(self) -> float:
        return self._brightness

    @brightness.setter
    def brightness(self, value: float):
        if value >= self._min_brightness and value <= self._max_brightness:
            self._brightness = value
            self.brightness_changed(value)

    @Property(float, flags="read-write")
    def blue_light(self) -> float:
        return self._blue_light

    @blue_light.setter
    def blue_light(self, value: int):
        if value >= self._min_blue_light and value <= self._max_blue_light:
            self._blue_light = value
            self.blue_light_changed(value)

    def __init__(
        self, brightness: float | None = None,
        min_brightness: float | None = None,
        max_brightness: float | None = None,
        blue_light: float | None = None,
        min_blue_light: float | None = None,
        max_blue_light: float | None = None,
    ):
        super().__init__()
        self._brightness = brightness or DEFAULT_BRIGHTNESS_VALUE
        self._min_brightness = min_brightness or 0.5
        self._max_brightness = max_brightness or 1.0
        self._blue_light = blue_light or DEFAULT_BLUE_LIGHT_FILTER_VALUE
        self._min_blue_light = min_blue_light or 2000.0
        self._max_blue_light = max_blue_light or 25000.0

class ScreenFilters(ToolbarPlugin):
    def __init__(self):
        self._name = "screen_filters"
        self._description = "Show screen filters button."

        self.shell_context = None

        self._filters_enabled = True
        self._min_brightness = 0.5
        self._max_brightness = 1.0
        self._min_blf = 2000.0
        self._max_blf = 25000.0
        self._filter_service = FilterService(
            DEFAULT_BRIGHTNESS_VALUE,
            self._min_brightness,
            self._max_brightness,
            DEFAULT_BLUE_LIGHT_FILTER_VALUE,
            self._min_blf,
            self._max_blf
        )

    def initialize(self, shell_context):
        self.shell_context = shell_context
        self.set_shader()

    def set_shader(self):
        shader_path = os.path.expanduser(HYPRSHADE_SHADER_PATH)
        temperature = self._filter_service.blue_light
        brightness = self._filter_service.brightness
        command = f"hyprshade on {shader_path} --var temperature={temperature} --var brightness={brightness}"
        exec_shell_command_async(
            command, lambda *_: None
        )

    def disable_shader(self):
        command = "hyprshade off"
        exec_shell_command_async(
            command, lambda *_: None
        )

    def set_blf_value(self, value: int):
        self._filter_service.blue_light = value
        self.set_shader()

    def set_brightness_value(self, value: float):
        self._filter_service.brightness = value
        self.set_shader()

    def reset_filters(self):
        if self._filter_service.brightness == DEFAULT_BRIGHTNESS_VALUE and self._filter_service.blue_light == DEFAULT_BLUE_LIGHT_FILTER_VALUE:
            return
        self._filter_service.brightness = DEFAULT_BRIGHTNESS_VALUE
        self._filter_service.blue_light = DEFAULT_BLUE_LIGHT_FILTER_VALUE

    def on_off_switch_changed(self, switch, state, brightness_scale, blf_scale):
        self._filters_enabled = state
        if state:
            self.set_shader()
        else:
            self.disable_shader()

        brightness_scale.set_sensitive(state)
        blf_scale.set_sensitive(state)
        switch.set_tooltip_text("Disable filters" if state else "Enable filters")

    def update_blf_label(self, scale, label):
        label.set_label(f"{round(scale.get_value())}K")

    def update_brightness_label(self, scale, label):
        label.set_label(f"{round(scale.get_value() * 100)}%")

    def get_popover_content(self):
        blf_label = Label(label=f"{round(self._filter_service.blue_light)}K")
        self._filter_service.connect("blue-light-changed", lambda _, value: blf_scale.set_value(value))

        blf_scale = Scale(
            min_value=self._min_blf,
            max_value=self._max_blf,
            value=self._filter_service.blue_light,
            step=500.0,
            orientation="h",
        )
        blf_scale.connect("button-release-event", lambda scale, _: self.set_blf_value(scale.get_value()))
        blf_scale.connect("value-changed", lambda scale: self.update_blf_label(scale, blf_label))
        blf_scale.set_sensitive(self._filters_enabled)

        brightness_label = Label(label=f"{round(self._filter_service.brightness * 100)}%")
        self._filter_service.connect("brightness-changed", lambda _, value: brightness_scale.set_value(value))

        brightness_scale = Scale(
            min_value=self._min_brightness,
            max_value=self._max_brightness,
            value=self._filter_service.brightness,
            step=0.05,
            orientation="h"
        )
        brightness_scale.set_sensitive(self._filters_enabled)
        brightness_scale.connect("value-changed", lambda scale: self.update_brightness_label(scale, brightness_label))
        brightness_scale.connect("button-release-event", lambda scale, _: self.set_brightness_value(scale.get_value()))

        reset_button = CommonButton(icon="refresh", icon_size=14, on_click=self.reset_filters, title="Reset filters")
        on_off_switch = Gtk.Switch(active=self._filters_enabled)
        on_off_switch.set_tooltip_text("Disable filters" if self._filters_enabled else "Enable filters")
        setup_cursor_hover(on_off_switch)
        on_off_switch.connect("state-set", lambda switch, state:self.on_off_switch_changed(switch, state, brightness_scale, blf_scale))

        return Box(
            orientation="v",
            children=[
                CenterBox(
                    orientation="h",
                    spacing=10,
                    style_classes="padding-10",
                    start_children=[
                        Label(label="Screen filters", style_classes="title")
                    ],
                    end_children=[
                        reset_button,
                        on_off_switch
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
                            end_children=blf_label
                        ),
                        blf_scale
                    ]
                ),
                Box(
                    spacing=5,
                    orientation="v",
                    style_classes="padding-10 margin-bottom-10",
                    children=[
                        CenterBox(
                            start_children=Label(label="Brightness"),
                            end_children=brightness_label
                        ),
                        brightness_scale
                    ]
                ),
            ]
        )

    def register_toolbar_widget(self):
        return CommonButton(
            name="screen-filters-button", icon="brightness", title="Screen filters", l_popover_factory=self.get_popover_content
        )
