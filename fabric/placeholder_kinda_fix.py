import gi

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0"})
from gi.repository import Gdk, GObject, Gtk, Pango


class PersistentPlaceholderEntry(Gtk.Entry):
    """A Gtk.Entry that keeps its placeholder visible when focused but empty."""

    def __init__(self, placeholder_text=""):
        super().__init__()

        # Set properties
        self.placeholder_text = placeholder_text
        self.actual_text = ""
        self.is_placeholder_visible = True

        # Set initial placeholder
        self.set_text(self.placeholder_text)

        # Apply placeholder styling
        self._apply_placeholder_style(True)

        # Connect signals
        self.connect("focus-in-event", self._on_focus_in)
        self.connect("focus-out-event", self._on_focus_out)
        self.connect("changed", self._on_changed)
        self.connect("key-press-event", self._on_key_press)

    def _apply_placeholder_style(self, is_placeholder):
        """Apply the placeholder or normal style to the entry"""
        context = self.get_style_context()
        if is_placeholder:
            self.set_text(self.placeholder_text)
            if not context.has_class("placeholder-active"):
                context.add_class("placeholder-active")
        else:
            if context.has_class("placeholder-active"):
                context.remove_class("placeholder-active")

    def _on_focus_in(self, widget, event):
        """Handle focus-in event"""
        # Move cursor to start of entry when showing placeholder
        if self.is_placeholder_visible:
            GObject.idle_add(self.set_position, 0)
        return False

    def _on_focus_out(self, widget, event):
        """Handle focus-out event"""
        # If the entry is empty, show placeholder
        if not self.actual_text:
            self.is_placeholder_visible = True
            self._apply_placeholder_style(True)
        return False

    def _on_changed(self, widget):
        """Handle text changes"""
        current_text = super().get_text()

        # Prevent recursive calls and infinite loops
        if hasattr(self, "_changing") and self._changing:
            return

        self._changing = True

        # Handle the change of text
        if current_text == "" and not self.is_placeholder_visible:
            # If text was deleted and placeholder is not showing, display placeholder
            self.is_placeholder_visible = True
            self._apply_placeholder_style(True)
            GObject.idle_add(self.set_position, 0)
        elif current_text != self.placeholder_text:
            # Text was entered, hide placeholder
            if self.is_placeholder_visible:
                self.is_placeholder_visible = False
                self._apply_placeholder_style(False)
                self.set_text(current_text)
            self.actual_text = current_text

        self._changing = False

    def _on_key_press(self, widget, event):
        """Handle key presses"""
        # If placeholder is visible and user starts typing,
        # clear placeholder and show normal text
        if self.is_placeholder_visible:
            # Check if the key is a printable character or spaces
            keyval = event.keyval
            if (
                (keyval >= 32 and keyval <= 126)  # ASCII printable
                or (keyval >= 0x00A0 and keyval <= 0x10FFFF)  # Unicode characters
                or keyval == Gdk.KEY_space
            ):
                self.is_placeholder_visible = False
                self._apply_placeholder_style(False)
                self.set_text("")
                return False  # Allow the character to be inserted

            # Handle special keys like delete, backspace when placeholder is visible
            if keyval in (Gdk.KEY_BackSpace, Gdk.KEY_Delete):
                return True  # Stop propagation to prevent deleting the placeholder

        return False  # Let other keys pass through

    def get_text(self):
        """Override get_text to return actual text, not placeholder"""
        return "" if self.is_placeholder_visible else super().get_text()

    def set_text(self, text):
        """Override set_text to handle placeholder properly"""
        if text == "" or text is None:
            self.actual_text = ""
            if self.is_focused():
                self.is_placeholder_visible = True
                super().set_text(self.placeholder_text)
                self._apply_placeholder_style(True)
            else:
                self.is_placeholder_visible = True
                super().set_text(self.placeholder_text)
                self._apply_placeholder_style(True)
        else:
            self.actual_text = text
            self.is_placeholder_visible = False
            super().set_text(text)
            self._apply_placeholder_style(False)

    def set_placeholder_text(self, text):
        """Set a new placeholder text"""
        self.placeholder_text = text
        if self.is_placeholder_visible:
            super().set_text(text)


# Demo application to showcase the persistent placeholder entry
class PlaceholderDemo(Gtk.Window):
    def __init__(self):
        super().__init__(title="Persistent Placeholder Demo")
        self.set_default_size(400, 200)
        self.set_border_width(20)

        # Load CSS
        self.load_css()

        # Create a grid layout
        grid = Gtk.Grid()
        grid.set_row_spacing(15)
        grid.set_column_spacing(10)
        self.add(grid)

        # Add a regular entry for comparison
        regular_label = Gtk.Label(label="Regular Entry:")
        regular_label.set_halign(Gtk.Align.START)
        grid.attach(regular_label, 0, 0, 1, 1)

        regular_entry = Gtk.Entry()
        regular_entry.set_placeholder_text("This placeholder disappears on focus")
        grid.attach(regular_entry, 1, 0, 1, 1)

        # Add our custom entry
        custom_label = Gtk.Label(label="Custom Entry:")
        custom_label.set_halign(Gtk.Align.START)
        grid.attach(custom_label, 0, 1, 1, 1)

        self.custom_entry = PersistentPlaceholderEntry(
            "This placeholder stays visible on focus"
        )
        grid.attach(self.custom_entry, 1, 1, 1, 1)

        # Add a button to get the text
        button = Gtk.Button(label="Get Entry Text")
        button.connect("clicked", self.on_button_clicked)
        grid.attach(button, 1, 2, 1, 1)

        # Add a label to show the text
        self.result_label = Gtk.Label(label="")
        self.result_label.set_halign(Gtk.Align.START)
        grid.attach(self.result_label, 1, 3, 1, 1)

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css = """
        .placeholder-active {
            color: gray;
            font-style: italic;
        }
        """
        css_provider.load_from_data(css.encode())

        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_button_clicked(self, button):
        text = self.custom_entry.get_text()
        if text:
            self.result_label.set_text(f"You entered: '{text}'")
        else:
            self.result_label.set_text("Entry is empty")


if __name__ == "__main__":
    win = PlaceholderDemo()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
