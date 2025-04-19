import os
from fabric.core.service import Service, Property, Signal
from config import DEFAULT_BRIGHTNESS_VALUE, DEFAULT_BLUE_LIGHT_FILTER_VALUE, HYPRSHADE_SHADER_PATH
from fabric.utils import exec_shell_command_async

class FilterService(Service):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = FilterService(
                DEFAULT_BRIGHTNESS_VALUE,
                0.5, 1.0,
                DEFAULT_BLUE_LIGHT_FILTER_VALUE,
                2000.0, 25000.0
            )
        return cls._instance

    @Signal
    def brightness_changed(self, value: float) -> None: ...
    @Signal
    def blue_light_changed(self, value: float) -> None: ...

    @Property(float, flags="read-write")
    def brightness(self) -> float:
        return self._brightness

    @brightness.setter
    def brightness(self, value: float):
        if value >= self.min_brightness and value <= self.max_brightness:
            self._brightness = value
            self.brightness_changed(value)

    @Property(float, flags="read-write")
    def blue_light(self) -> float:
        return self._blue_light

    @blue_light.setter
    def blue_light(self, value: int):
        if value >= self.min_blue_light and value <= self.max_blue_light:
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
        self.min_brightness = min_brightness or 0.5
        self.max_brightness = max_brightness or 1.0
        self._blue_light = blue_light or DEFAULT_BLUE_LIGHT_FILTER_VALUE
        self.min_blue_light = min_blue_light or 2000.0
        self.max_blue_light = max_blue_light or 25000.0
        self.enabled = True

    def shader_on(self):
        shader_path = os.path.expanduser(HYPRSHADE_SHADER_PATH)
        temperature = self.blue_light
        brightness = self.brightness
        command = f"hyprshade on {shader_path} --var temperature={temperature} --var brightness={brightness}"
        exec_shell_command_async(
            command, lambda *_: None
        )

    def shader_off(self):
        command = "hyprshade off"
        exec_shell_command_async(
            command, lambda *_: None
        )
