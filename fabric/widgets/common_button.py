from typing import Callable

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from utils.widgets import setup_cursor_hover
from widgets.popover import Popover


class CommonButton(Button):
    """A common button to be used with the Status Bar"""

    @property
    def l_popover(self):
        """Lazy create the popover if accessed."""
        if not self._l_popover and self._l_popover_factory:
            self._l_popover = Popover(self._l_popover_factory, self)
        return self._l_popover

    @property
    def r_popover(self):
        """Lazy create the popover if accessed."""
        if not self._r_popover and self._r_popover_factory:
            self._r_popover = Popover(self._r_popover_factory, self)
        return self._r_popover

    def __init__(
        self,
        label: str | None = None,
        icon: str | None = None,
        icon_size=14,
        title: str | None = None,
        l_popover_factory: Callable | None = None,
        r_popover_factory: Callable | None = None,
        on_click: Callable | None = None,
        **kwargs,
    ):
        """
        Initialize the common button.

        Args:
            label: Button label
            icon: Button icon
            icon_size: Button icon size
            title: Text to be rendered as a tooltip
            l_popover_factory: Function that returns the content for the popover that will open with left click
            r_popover_factory: Function that returns the content for the popover that will open with right click
            **kwargs: Additional arguments for Button
        """
        super().__init__(
            style_classes="common-button",
            **kwargs,
        )

        self._icon = icon
        self._icon_size = icon_size
        self._label = label
        self._l_popover_factory = l_popover_factory
        self._r_popover_factory = r_popover_factory
        self._on_click = on_click

        self._icon_widget = None
        self._label_widget = None
        self._l_popover = None
        self._r_popover = None

        self._content_box = Box(
            orientation="h",
            spacing=5,
        )

        if self._icon is not None:
            self.set_icon(self._icon)

        if self._label is not None:
            self.set_label(self._label)

        if title is not None:
            self.set_tooltip_text(title)

        if (
            self._on_click is not None
            or self._l_popover_factory is not None
            or self._r_popover_factory is not None
        ):
            self.connect("button-press-event", self._on_button_press)

        setup_cursor_hover(self)
        self.add(self._content_box)
        self.show_all()

    def _on_button_press(self, widget, event):
        # Left click
        if event.button == 1:
            if self._on_click is not None:
                return self._on_click()
            elif self._l_popover_factory is not None:
                if not self._l_popover:
                    self._l_popover = Popover(self._l_popover_factory, self)
                self._l_popover.open()

        # Right click
        if event.button == 3 and self._r_popover_factory is not None:
            if not self._r_popover:
                self._r_popover = Popover(self._r_popover_factory, self)
            self._r_popover.open()

        return True

    def set_label(self, label: str | None):
        if not label:
            return False

        if not self._label_widget:
            self._label_widget = Label(
                label=label,
                style_classes="common-button-label",
            )
            self._content_box.add(self._label_widget)
        else:
            self._label_widget.set_label(label)

        return True

    def set_icon(self, icon: str | None = "", size: int | None = None):
        if size is not None:
            self._icon_size = size

        if not self._icon_widget:
            self._icon_widget = Image(
                icon_size=self._icon_size,
                style_classes="common-button-icon",
                icon_name=f"{icon}-symbolic",
            )
            self._content_box.add(self._icon_widget)
        else:
            self._icon_widget.set_from_icon_name(icon, self._icon_size)

        return True
