import gi
from utils.widgets import setup_cursor_hover
gi.require_version("Gtk", "3.0")
import calendar
import datetime
from gi.repository import Gdk, Gtk


class Calendar(Gtk.Grid):
    def __init__(self):
        super().__init__(name="calendar")

        self.set_row_spacing(1)
        self.set_column_spacing(1)
        self.set_row_homogeneous(True)
        self.set_column_homogeneous(True)

        # Current displayed date
        self.current_date = datetime.datetime.now()
        self.selected_date = self.current_date

        css_context = self.get_style_context()
        css_context.add_class("padding-10")

        # Header with month/year and navigation
        self.header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.prev_button = Gtk.Button.new_from_icon_name(
            "go-previous-symbolic", Gtk.IconSize.BUTTON
        )
        self.prev_button.set_name("calendar-prev-button")
        self.next_button = Gtk.Button.new_from_icon_name(
            "go-next-symbolic", Gtk.IconSize.BUTTON
        )
        self.next_button.set_name("calendar-next-button")
        self.month_year_label = Gtk.Label()

        self.prev_button.connect("clicked", self._previous_month)
        self.next_button.connect("clicked", self._next_month)

        self.header.pack_start(self.prev_button, False, False, 0)
        self.header.pack_start(self.month_year_label, True, True, 0)
        self.header.pack_start(self.next_button, False, False, 0)

        self.attach(self.header, 0, 0, 7, 1)

        # TODO: Fix arrow button going to the wrong month after clicking on a out-day

        # Day labels (Mon, Tue, etc.)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = Gtk.Label(label=day)
            label.get_style_context().add_class("day-header")
            self.attach(label, i, 1, 1, 1)

        # Create the buttons for days
        self.day_buttons = []
        for row in range(6):
            for col in range(7):
                button = Gtk.Button()
                button.connect("clicked", self._on_day_clicked)
                button.get_style_context().add_class("day-button")
                self.attach(button, col, row + 2, 1, 1)
                setup_cursor_hover(button)
                self.day_buttons.append(button)

        self._update_calendar()

    def _update_calendar(self, selected=False):
        # Get the calendar for the current month
        year, month = self.current_date.year, self.current_date.month

        if selected:
            year, month = self.selected_date.year, self.selected_date.month

        self.month_year_label.set_text(
            self.selected_date.strftime("%B %Y")
            if selected
            else self.current_date.strftime("%B %Y")
        )

        # Get current day for highlighting
        today = datetime.datetime.now()

        # Calculate days from previous and next month
        # Get the first weekday of this month (0 = Monday, 6 = Sunday)
        first_day, days_in_month = calendar.monthrange(year, month)

        # Calculate previous month details
        prev_month = month - 1
        prev_year = year
        if prev_month < 1:
            prev_month = 12
            prev_year -= 1
        _, prev_days_in_month = calendar.monthrange(prev_year, prev_month)

        # Calculate next month details
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1

        # Update day buttons
        day_index = 0

        # Fill in days from previous month
        for i in range(first_day):
            day = prev_days_in_month - first_day + i + 1
            button = self.day_buttons[day_index]
            button.set_label(str(day))
            button.set_sensitive(True)
            button.date = datetime.datetime(prev_year, prev_month, day)

            # Style differently to indicate it's from previous month
            button.get_style_context().remove_class("current-month")
            button.get_style_context().add_class("other-month")
            button.get_style_context().remove_class("today")
            button.get_style_context().remove_class("selected")

            day_index += 1

        # Fill in days from current month
        for day in range(1, days_in_month + 1):
            button = self.day_buttons[day_index]
            button.set_label(str(day))
            button.set_sensitive(True)
            button.date = datetime.datetime(year, month, day)

            # Style as current month
            button.get_style_context().add_class("current-month")
            button.get_style_context().remove_class("other-month")

            # Check if this is today
            if year == today.year and month == today.month and day == today.day:
                button.get_style_context().add_class("today")
            else:
                button.get_style_context().remove_class("today")

            # Check if this is the selected date
            if (
                self.selected_date
                and year == self.selected_date.year
                and month == self.selected_date.month
                and day == self.selected_date.day
            ):
                button.get_style_context().add_class("selected")
            else:
                button.get_style_context().remove_class("selected")

            day_index += 1

        # Fill in days from next month
        next_day = 1
        while day_index < len(self.day_buttons):
            button = self.day_buttons[day_index]
            button.set_label(str(next_day))
            button.set_sensitive(True)
            button.date = datetime.datetime(next_year, next_month, next_day)

            # Style differently to indicate it's from next month
            button.get_style_context().remove_class("current-month")
            button.get_style_context().add_class("other-month")
            button.get_style_context().remove_class("today")
            button.get_style_context().remove_class("selected")

            next_day += 1
            day_index += 1

    def _previous_month(self, button):
        year = self.selected_date.year
        month = self.selected_date.month - 1
        if month < 1:
            month = 12
            year -= 1
        self.selected_date = datetime.datetime(year, month, 1)
        self._update_calendar(True)

    def _next_month(self, button):
        year = self.selected_date.year
        month = self.selected_date.month + 1
        if month > 12:
            month = 1
            year += 1
        self.selected_date = datetime.datetime(year, month, 1)
        self._update_calendar(True)

    def _on_day_clicked(self, button):
        if hasattr(button, "date"):
            self.selected_date = button.date
            self._update_calendar(True)
            # self.emit("day-selected")

    def get_date(self):
        return self.selected_date
