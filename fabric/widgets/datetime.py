import time

from gi.repository import GLib

from fabric.core.service import Property
from fabric.utils.helpers import invoke_repeater
from fabric.widgets.button import Button
from utils.styling import int_to_ordinal
from utils.widgets import setup_cursor_hover


class DateTime(Button):
    @Property(int, "read-write")
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value: int):
        self._interval = value
        if self._repeater_id:
            GLib.source_remove(self._repeater_id)
        self._repeater_id = invoke_repeater(self._interval, self.update_time)
        self.update_time()
        return

    def __init__(self, interval: int = 1000, **kwargs):
        super().__init__(name="datetime", **kwargs)

        self._interval: int = interval
        self._repeater_id: int | None = None

        self.interval = interval

        setup_cursor_hover(self)

        self.update_time()

    def update_time(self):
        day = time.strftime("%d")
        ordinal_day = int_to_ordinal(int(day))

        self.set_tooltip_text(time.strftime(f"%B %d, %Y - %H:%M:%S"))
        self.set_label(time.strftime(f"%a %d ❘ %H:%M"))
        return True
