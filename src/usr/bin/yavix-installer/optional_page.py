import gi
import sys
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import os

class OptionalPage(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_margin_top(50)
        self.set_margin_bottom(50)
        self.set_margin_start(50)
        self.set_margin_end(50)

        self.welcome_label = Gtk.Label(label="Install optional apps?")
        self.welcome_label.set_wrap(True)
        self.welcome_label.set_wrap_mode(Gtk.WrapMode.WORD)
        self.welcome_label.set_halign(Gtk.Align.CENTER)
        self.welcome_label.add_css_class("title-1")
        self.append(self.welcome_label)

        self.apps_label = Gtk.Label(label="\n* LocalSend\n* GearLevel")
        self.apps_label.set_wrap(True)
        self.apps_label.set_wrap_mode(Gtk.WrapMode.WORD)
        self.apps_label.set_halign(Gtk.Align.CENTER)
        self.apps_label.add_css_class("title-2")
        self.append(self.apps_label)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        
        icon_size = 128

        self.yes_button = Gtk.Button(label="Yes")
        self.yes_button.option = "Yes"
        self.yes_button.connect("clicked", self.on_button_clicked)

        self.no_button = Gtk.Button(label="No")
        self.no_button.option = "No"        
        self.no_button.connect("clicked", self.on_button_clicked)

        self.yes_button.set_hexpand(True)
        self.no_button.set_hexpand(True)

        self.vbox1.append(self.yes_button)
        self.vbox1.append(self.no_button)
        self.append(self.vbox1)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.set_halign(Gtk.Align.CENTER)
        self.next_button.add_css_class("suggested-action")
        self.next_button.set_size_request(200, 50)
        self.next_button.set_visible(False)
        self.append(self.next_button)

    def on_button_clicked(self, button):
        import installer

        installer.optional_apps = button.option
        self.next_button.set_visible(True)  
            

