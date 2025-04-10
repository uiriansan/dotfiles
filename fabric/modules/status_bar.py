import gi

gi.require_versions({"Gtk": "3.0", "Gdk": "3.0", "GtkLayerShell": "0.1"})
import time

from gi.repository import Gdk, GLib, Gtk, GtkLayerShell

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow as Window
from utils.widgets import setup_cursor_hover
from widgets.active_window import ActiveWindow
from widgets.datetime import DateTime
from widgets.icon_button import IconButton
from widgets.popover import PopoverWindow
from widgets.system_tray import SystemTray
from widgets.toolbar import Toolbar

############################################################################################
#                                                                                          #
#                                   Use Gtk.Menu()!!                                       #
#                           ...at least for the right click                                #
#                                                                                          #
############################################################################################


class StatusBar(Window):
    def __init__(self, monitor, main_monitor_id):
        super().__init__(
            name="status-bar",
            layer="top",
            monitor=monitor,
            anchor="left top right",
            margin="0px 0px -20px 0px",
            exclusivity="auto",
            # keyboard_mode="on-demand",
            visible=False,
            all_visible=False,
        )

        self._main_monitor_id = main_monitor_id

        self._opened_popover = None

        self.system_button = IconButton(icon="arch", title="Arch Linux")
        self.layout = setup_cursor_hover(
            Button(
                child=Box(
                    orientation="h",
                    spacing=5,
                    children=[
                        Image(
                            icon_name="layout-dwindle-symbolic",
                            icon_size=12,
                        ),
                        Label(label="Dwindle", style="font-weight: bold;"),
                    ],
                ),
            )
        )
        self.active_window = ActiveWindow()

        self.system_tray = (
            SystemTray(name="system-tray", spacing=0, icon_size=16)
            if monitor == main_monitor_id
            else Box()
        )

        self.datetime = DateTime()
        self.datetime.connect("button-press-event", self.on_widget_button_press)

        # Create popup window
        self.popup_window = None
        self.popup_visible = False

        self.toolbar = Toolbar()

        # self.system_button.connect(
        #     "clicked",
        #     lambda *_: popover2.present(),
        # )
        #
        # self.power_button.connect(
        #     "clicked",
        #     lambda *_: popover3.present(),
        # )

        # self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        # This will be the event handler for mouse presses
        # self.connect("button-press-event", self.on_gevent)

        # Gdk.Seat.grab(
        #     Gdk.Display.get_default().get_default_seat(),
        #     self,
        #     Gdk.SeatCapabilities.POINTER,
        #     True,
        #     None,
        #     Gdk.EventType.BUTTON_PRESS,
        #     None,
        # )

        self.children = Box(
            orientation="v",
            children=[
                CenterBox(
                    name="status-bar-container",
                    start_children=Box(
                        name="start-container",
                        spacing=0,
                        orientation="h",
                        children=[
                            self.system_button,
                            # self.layout,
                            # Gtk.Separator(),
                            self.active_window,
                        ],
                    ),
                    center_children=Box(
                        name="center-container",
                        spacing=0,
                        orientation="h",
                        children=[
                            self.datetime,
                        ],
                    ),
                    end_children=Box(
                        name="end-container",
                        spacing=0,
                        orientation="h",
                        children=[
                            self.toolbar,
                            self.system_tray,
                        ],
                    ),
                ),
                CenterBox(
                    name="status-bar-corners",
                    start_children=Box(name="status-bar-corner-left"),
                    end_children=Box(name="status-bar-corner-right"),
                ),
            ],
        )

        self.show_all()

    def toggle(self):
        self.set_visible(not self.get_visible())

    #
    # def get_pointing_to(self, widget: Gtk.Widget) -> Gdk.Rectangle:
    #     # if not ((toplevel := widget.get_toplevel()) and toplevel.is_toplevel()):
    #     #     return 0, 0
    #
    #     return widget.get_allocation()
    #     # x, y = widget.translate_coordinates(toplevel, allocation.x, allocation.y) or (
    #     #     0,
    #     #     0,
    #     # )
    #     # return round(x / 2), round(y / 2)
    #
    # def close_opened_popover(self):
    #     if self._opened_popover:
    #         return self._opened_popover.close()
    #
    # def on_gevent(self, widget, event):
    #     print(event.type)
    #     if event.type == Gdk.EventType.BUTTON_PRESS:
    #         pass
    #         # self.close_opened_popover()

    def on_widget_button_press(self, widget, event):
        # Check if it's a right-click (button 3)
        if event.button == 1:
            if self.popup_window and self.popup_visible:
                self.hide_popup()
            else:
                self.show_popup_at(event.x_root, event.y_root)
            return True
        return False

    def show_popup_at(self, x, y):
        # Create popup window if it doesn't exist
        if not self.popup_window:
            self.popup_window = Gtk.Window(type=Gtk.WindowType.POPUP, name="popup")
            GtkLayerShell.init_for_window(self.popup_window)
            GtkLayerShell.set_layer(self.popup_window, GtkLayerShell.Layer.OVERLAY)
            GtkLayerShell.set_keyboard_interactivity(self.popup_window, True)

            # Make the popup transparent to input except for its widgets
            self.popup_window.set_app_paintable(True)
            screen = self.popup_window.get_screen()
            visual = screen.get_rgba_visual()
            if visual and screen.is_composited():
                self.popup_window.set_visual(visual)

            # Add content to popup
            self.popup_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.popup_content.set_margin_start(0)
            self.popup_content.set_margin_end(0)
            self.popup_content.set_margin_top(0)
            self.popup_content.set_margin_bottom(0)

            # Add menu items
            item1 = Gtk.Button(label="Option 1")
            item2 = Gtk.Button(label="Option 2")
            item3 = Gtk.Button(label="Option 3")

            self.popup_content.pack_start(item1, False, False, 5)
            self.popup_content.pack_start(item2, False, False, 5)
            self.popup_content.pack_start(item3, False, False, 5)

            self.popup_window.add(self.popup_content)

            # Add CSS styling
            css_provider = Gtk.CssProvider()
            css = b"""
            window {
                background-color: black;
                background: black;
                border-radius: 5px;
                border: 1px solid rgba(255, 255, 255, 0.9);
            }
            #popup {
                background-color: red;
            }
            button {
                background-color: black;
                background: black;
                color: green;
                border-radius: 3px;
                padding: 8px;
            }
            button:hover {
                background-color: rgba(70, 70, 70, 0.9);
            }
            """
            css_provider.load_from_data(css)
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )

            # Connect events
            self.popup_window.connect("button-press-event", self.on_popup_clicked)

            # Connect signal to detect when popup loses focus
            self.popup_window.connect("focus-out-event", self.on_popup_focus_out)

        # Position the popup
        GtkLayerShell.set_anchor(self.popup_window, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self.popup_window, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_margin(self.popup_window, GtkLayerShell.Edge.LEFT, x)
        GtkLayerShell.set_margin(self.popup_window, GtkLayerShell.Edge.TOP, y)

        # Create an invisible, full-screen layer shell window below our popup
        # This window will capture clicks outside our popup
        self.backdrop = Gtk.Window()
        GtkLayerShell.init_for_window(self.backdrop)
        GtkLayerShell.set_layer(self.backdrop, GtkLayerShell.Layer.OVERLAY)
        self.backdrop.set_app_paintable(True)
        self.backdrop.connect("button-press-event", self.on_backdrop_clicked)

        # Make backdrop invisible but clickable
        self.backdrop.set_opacity(0.01)
        self.backdrop.set_size_request(1, 1)  # Minimal size
        GtkLayerShell.set_anchor(self.backdrop, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self.backdrop, GtkLayerShell.Edge.RIGHT, True)
        GtkLayerShell.set_anchor(self.backdrop, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self.backdrop, GtkLayerShell.Edge.BOTTOM, True)

        # Show our windows
        self.backdrop.show_all()
        self.popup_window.show_all()
        self.popup_visible = True

    def on_popup_clicked(self, widget, event):
        # Let clicks inside the popup through
        return False

    def on_backdrop_clicked(self, widget, event):
        # When clicking outside the popup, hide it
        self.hide_popup()
        return True

    def on_popup_focus_out(self, widget, event):
        # This helps with keyboard focus issues
        print("focus-out")
        GLib.timeout_add(100, self.hide_popup)
        return False

    def hide_popup(self):
        if self.popup_window and self.popup_visible:
            self.popup_window.hide()
            if hasattr(self, "backdrop") and self.backdrop:
                self.backdrop.hide()
                self.backdrop.destroy()
                self.backdrop = None
            self.popup_visible = False
        return False
