from typing import Callable
from gi.repository import GLib
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from loguru import logger
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
        revealed: bool = True,
        **kwargs,
    ):
        """
        Initialize the common button.

        :param label: Button label
        :type label: str
        :param icon: Button icon
        :type icon: str
        :param icon_size: Button icon size
        :type icon_size: int
        :param title: Text to be rendered as a tooltip
        :type title: str
        :param l_popover_factory: Function that returns the content for the popover that will open with left click
        :type l_popover_factory: Callable[Gtk.Widget]
        :param r_popover_factory: Function that returns the content for the popover that will open with right click
        :type r_popover_factory: Callable[Gtk.Widget]
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

        # Make sure *_popover_factory is not a lambda expression
        # Lambda creates a weak reference that will end up being destroyed by the garbage collector along with the popover window.
        if l_popover_factory is not None:
            if (callable(l_popover_factory) and l_popover_factory.__name__ == '<lambda>'):
                logger.warning(f"`popover_factory` cannot be a lambda expression. Skipping popover for button `{self.get_name()}`")
                self._l_popover_factory = None
        if r_popover_factory is not None:
            if (callable(r_popover_factory) and r_popover_factory.__name__ == '<lambda>'):
                logger.warning(f"`popover_factory` cannot be a lambda expression. Skipping popover for button `{self.get_name()}`")
                self._r_popover_factory = None

        self._on_click = on_click
        self._revealed = revealed

        self._label_revealer_clear_delay = None

        self._icon_widget = None
        self._label_widget = None
        self._l_popover = None
        self._r_popover = None

        self._content_box = Box(
            orientation="h",
            spacing=5 if self._revealed else 0,
        )

        self._revealer = Revealer(
            transition_type="slide-right",
            transition_duration=200,
            child_revealed=self._revealed,
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
                    self._l_popover.connect("popover-closed", lambda _: self.remove_style_class("pressed"))
                self._l_popover.open()
                self.add_style_class("pressed")

        # Right click
        if event.button == 3 and self._r_popover_factory is not None:
            if not self._r_popover:
                self._r_popover = Popover(self._r_popover_factory, self)
                self._r_popover.connect("popover-closed", lambda _: self.remove_style_class("pressed"))
            self._r_popover.open()
            self.add_style_class("pressed")

        return True

    def set_label(self, label: str | None):
        if not label:
            return

        if not self._label_widget:
            self._label_widget = Label(
                label=label,
                style_classes="common-button-label",
            )
            self._revealer.add(self._label_widget)
            self._content_box.pack_end(self._revealer, False, False, 0)
        else:
            self._label_widget.set_label(label)

    def set_label_and_reveal(self, label: str | None, reveal_duration: int = 1000 * 5):
        self.set_label(label)
        self.reveal()

        if self._label_revealer_clear_delay is not None:
            GLib.source_remove(self._label_revealer_clear_delay)
            self._label_revealer_clear_delay = None

        self._label_revealer_clear_delay = GLib.timeout_add(
            reveal_duration, self._unreveal_and_clear_delay
        )

    def set_icon(self, icon: str | None = "", size: int | None = None):
        if size is not None:
            self._icon_size = size

        if not self._icon_widget:
            self._icon_widget = Image(
                icon_size=self._icon_size,
                style_classes="common-button-icon",
                icon_name=f"{icon}-symbolic",
            )
            self._content_box.pack_start(self._icon_widget, False, False, 0)
        else:
            self._icon_widget.set_from_icon_name(icon, self._icon_size)

        return True

    def reveal(self):
        self._content_box.set_spacing(5)
        return self._revealer.reveal()

    def unreveal(self):
        self._content_box.set_spacing(0)
        return self._revealer.unreveal()

    def _unreveal_and_clear_delay(self):
        if self._label_revealer_clear_delay is not None:
            GLib.source_remove(self._label_revealer_clear_delay)
            self._label_revealer_clear_delay = None

        self.unreveal()
