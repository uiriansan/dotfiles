from fabric.widgets.widget import Literal
import gi
gi.require_versions({"Gtk": "3.0"})
from gi.repository import Gtk
from utils.widgets import setup_cursor_hover
from fabric.core.service import Property

class Scale(Gtk.Scale):
    @Property(float, "read-write", install=False)
    def value(self) -> float:
        return self.get_value()

    @value.setter
    def value(self, value: float):
        return self.set_value(value)

    @Property(float, "read-write", default_value=0.0)
    def min_value(self) -> float:
        return self._min_value

    @min_value.setter
    def min_value(self, value: float):
        self._min_value = value
        return self.set_range(self._min_value, self._max_value)

    @Property(float, "read-write", default_value=1.0)
    def max_value(self) -> float:
        return self._max_value

    @max_value.setter
    def max_value(self, value: float):
        self._max_value = value
        return self.set_range(self._min_value, self._max_value)

    def __init__(self,
        min_value: float = 0.0,
        max_value: float = 1.0,
        value: float = 0.5,
        step: float = 0.1,
        orientation: Literal["h", "v"] | None = None,
        value_pos: Literal["hide", "top", "bottom", "left", "right"] = "hide",
        digits: int = 0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self._min_value = min_value
        self._max_value = max_value
        self._value = value
        self._step = step
        self._orientation = orientation or "h"
        self._value_pos = value_pos or "hide"
        self._digits = digits

        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.set_orientation(Gtk.Orientation.HORIZONTAL if self._orientation == "h" else Gtk.Orientation.VERTICAL)
        self.set_value(self._value)
        self.set_digits(self._digits)

        self.set_draw_value(not self._value_pos == "hide")
        self.set_value_pos(
            Gtk.PositionType.LEFT if self._value_pos == "left"
            else Gtk.PositionType.RIGHT if self._value_pos == "right"
            else Gtk.PositionType.TOP if self._value_pos == "top"
            else Gtk.PositionType.BOTTOM
        )

        self._style_context = self.get_style_context()
        setup_cursor_hover(self)

        self.connect("value-changed", self._on_value_changed)
        self.connect("button-press-event", self._on_button_press)
        self.connect("button-release-event", self._on_button_release)

        # Flag to prevent infinite recursion in value changes
        self._updating = False

    def _on_value_changed(self, scale):
        if self._updating:
            return

        current_value = scale.get_value()
        stepped_value = round(current_value / self._step) * self._step

        if stepped_value != current_value:
            self._updating = True
            scale.set_value(stepped_value)
            self._updating = False

    def _on_button_press(self, widget, event):
        if event.button == 1:
            self._style_context.add_class("pressed")

    def _on_button_release(self, widget, event):
        if event.button == 1:
            self._style_context.remove_class("pressed")
