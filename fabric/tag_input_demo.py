import gi

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0"})
from gi.repository import Gdk, GObject, Gtk, Pango


class IntegratedTagEntry(Gtk.Entry):
    """A custom Gtk.Entry that handles tags inline with text and supports navigation."""

    def __init__(self, available_tags=None):
        super().__init__()

        # List of available tags
        self.available_tags = available_tags or [
            "python",
            "gtk",
            "programming",
            "ui",
            "linux",
        ]

        # Tag state
        self.tags = []  # List of (start_pos, end_pos, tag_text) tuples
        self.current_tag_candidates = []  # For auto-completion
        self.is_navigating_tags = False

        # Connect signals
        self.connect("key-press-event", self.on_key_press)
        self.connect("changed", self.on_text_changed)
        self.connect("focus-out-event", self.on_focus_out)

        # Set up custom text layout
        self.create_tags()

        # For rendering
        self.connect("draw", self.on_draw)

    def create_tags(self):
        """Create Pango attributes for tag styling"""
        self.tag_attrs = Pango.AttrList()

    def update_tag_rendering(self):
        """Update the visual rendering of tags"""
        self.tag_attrs = Pango.AttrList()

        # Apply styling to each tag
        for start_pos, end_pos, tag_text in self.tags:
            # Background color
            bg_attr = Pango.attr_background_new(52, 152, 219)  # #3498db (blue)
            bg_attr.start_index = start_pos
            bg_attr.end_index = end_pos
            self.tag_attrs.insert(bg_attr)

            # Foreground color
            fg_attr = Pango.attr_foreground_new(255, 255, 255)  # white
            fg_attr.start_index = start_pos
            fg_attr.end_index = end_pos
            self.tag_attrs.insert(fg_attr)

            # Border radius is not directly supported in Pango,
            # so we approximate with a slight padding
            pad_attr = Pango.attr_rise_new(600)  # Slight padding
            pad_attr.start_index = start_pos
            pad_attr.end_index = end_pos
            self.tag_attrs.insert(pad_attr)

            # Weight
            weight_attr = Pango.attr_weight_new(Pango.Weight.BOLD)
            weight_attr.start_index = start_pos
            weight_attr.end_index = end_pos
            self.tag_attrs.insert(weight_attr)

        # Apply attributes to the entry
        self.set_attributes(self.tag_attrs)

    def on_draw(self, widget, cr):
        """Custom drawing for better tag appearance"""
        # Let the default drawing happen
        retval = Gtk.Entry.do_draw(widget, cr)

        # Add custom drawing here if needed for better tag styling
        # (For advanced styling beyond what Pango can do)

        return retval

    def on_text_changed(self, entry):
        """Handle text changes"""
        # Get the current text and cursor position
        text = self.get_text()
        position = self.get_position()

        # Check if we're in the middle of typing a potential tag
        word_start = position
        while word_start > 0 and text[word_start - 1].isalnum():
            word_start -= 1

        current_word = text[word_start:position]

        # Update tag positions if text was inserted or deleted
        self.update_tag_positions()

        # Check for tag candidates based on current word
        if current_word:
            self.current_tag_candidates = [
                tag
                for tag in self.available_tags
                if tag.startswith(current_word) and tag != current_word
            ]
        else:
            self.current_tag_candidates = []

        # Check if the current word exactly matches a tag
        if current_word in self.available_tags:
            # Highlight the potential tag
            self.get_style_context().add_class("tag-match")
        else:
            self.get_style_context().remove_class("tag-match")

        # Update the visual rendering of tags
        self.update_tag_rendering()

    def update_tag_positions(self):
        """Update tag positions after text changes"""
        text = self.get_text()
        position = self.get_position()
        updated_tags = []

        # Adjust tag positions based on current text
        for start_pos, end_pos, tag_text in self.tags:
            # Check if the tag is still intact in the text
            if start_pos < len(text) and end_pos <= len(text):
                if text[start_pos:end_pos] == tag_text:
                    updated_tags.append((start_pos, end_pos, tag_text))

        self.tags = updated_tags

    def on_key_press(self, entry, event):
        """Handle key presses"""
        keyval = event.keyval
        text = self.get_text()
        position = self.get_position()

        # Handle Enter key - create tag
        if keyval == Gdk.KEY_Return or keyval == Gdk.KEY_KP_Enter:
            # Get the word at cursor
            word_start = position
            while word_start > 0 and text[word_start - 1].isalnum():
                word_start -= 1

            word_end = position
            while word_end < len(text) and text[word_end].isalnum():
                word_end += 1

            current_word = text[word_start:word_end]

            if current_word and current_word in self.available_tags:
                # Create a new tag
                self.create_tag_at_position(word_start, word_end, current_word)
                return True  # Stop event propagation

        # Handle Backspace - delete tag if at tag boundary
        elif keyval == Gdk.KEY_BackSpace:
            # Check if cursor is just after a tag
            for i, (start_pos, end_pos, tag_text) in enumerate(self.tags):
                if position == end_pos:
                    # Delete the tag
                    new_text = text[:start_pos] + text[end_pos:]
                    self.set_text(new_text)
                    self.set_position(start_pos)
                    return True  # Stop event propagation

        # Handle Left/Right arrow keys for navigation
        elif keyval == Gdk.KEY_Left:
            # Check if we need to jump to the start of a tag
            for start_pos, end_pos, tag_text in self.tags:
                if position == end_pos:
                    self.set_position(start_pos)
                    return True

        elif keyval == Gdk.KEY_Right:
            # Check if we need to jump to the end of a tag
            for start_pos, end_pos, tag_text in self.tags:
                if position == start_pos:
                    self.set_position(end_pos)
                    return True

        return False  # Continue event propagation

    def on_focus_out(self, widget, event):
        """Handle focus out - finalize any pending tags"""
        text = self.get_text()
        position = self.get_position()

        # Check if there's a potential tag at cursor
        word_start = position
        while word_start > 0 and text[word_start - 1].isalnum():
            word_start -= 1

        word_end = position
        while word_end < len(text) and text[word_end].isalnum():
            word_end += 1

        current_word = text[word_start:word_end]

        if current_word and current_word in self.available_tags:
            # Create a tag from the current word
            self.create_tag_at_position(word_start, word_end, current_word)

        return False

    def create_tag_at_position(self, start_pos, end_pos, tag_text):
        """Create a tag at the specified position"""
        text = self.get_text()

        # Add the tag to our list of tags
        self.tags.append((start_pos, end_pos, tag_text))

        # Sort tags by start position
        self.tags.sort(key=lambda x: x[0])

        # Update the visual rendering
        self.update_tag_rendering()

        # Move cursor to end of tag
        self.set_position(end_pos)

    def get_tags_list(self):
        """Return list of tag texts"""
        return [tag_text for _, _, tag_text in self.tags]


class TagInputDemo(Gtk.Window):
    def __init__(self):
        super().__init__(title="Integrated Tag Input Demo")
        self.set_default_size(500, 150)
        self.set_border_width(20)

        # Load CSS
        self.load_css()

        # Create a vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Add instruction label
        instructions = Gtk.Label()
        instructions.set_markup(
            "<b>Available Tags:</b> python, gtk, programming, ui, linux\n"
            "<i>Type a tag name and press Enter to create a tag. "
            "Use arrow keys to navigate between tags.</i>"
        )
        instructions.set_halign(Gtk.Align.START)
        vbox.pack_start(instructions, False, False, 0)

        # Create tag entry
        self.tag_entry = IntegratedTagEntry()
        vbox.pack_start(self.tag_entry, False, False, 10)

        # Add a button to get tags
        button = Gtk.Button(label="Get Tags")
        button.connect("clicked", self.on_get_tags_clicked)
        vbox.pack_start(button, False, False, 0)

        # Add a results label
        self.result_label = Gtk.Label()
        self.result_label.set_halign(Gtk.Align.START)
        vbox.pack_start(self.result_label, False, False, 10)

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css = """
        .tag-match {
            background-color: #e8f4fc;
        }
        """
        css_provider.load_from_data(css.encode())

        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_get_tags_clicked(self, button):
        tags = self.tag_entry.get_tags_list()
        if tags:
            self.result_label.set_text(f"Selected tags: {', '.join(tags)}")
        else:
            self.result_label.set_text("No tags selected")


if __name__ == "__main__":
    win = TagInputDemo()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
