import gi
import sys
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

class WelcomePage(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_margin_top(50)
        self.set_margin_bottom(50)
        self.set_margin_start(50)
        self.set_margin_end(50)

        welcome_label = Gtk.Label(label="Welcome to Lightix Installer!")
        welcome_label.set_wrap(True)
        welcome_label.set_wrap_mode(Gtk.WrapMode.WORD)
        welcome_label.set_halign(Gtk.Align.CENTER)
        welcome_label.add_css_class("title-1")
        self.append(welcome_label)

        subtitle = Gtk.Label(label="Click to start installation.")
        subtitle.set_halign(Gtk.Align.CENTER)
        subtitle.add_css_class("dim-label")
        self.append(subtitle)

        self.start_button = Gtk.Button(label="Start installation")
        self.start_button.set_halign(Gtk.Align.CENTER)
        self.start_button.add_css_class("suggested-action")
        self.start_button.connect("clicked", self.on_start_clicked)
        self.append(self.start_button)

    def on_start_clicked(self, button):
        print("instalation starts")

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("")
        self.set_default_size(600, 400)
        self.set_resizable(False)

        welcome_page = WelcomePage()
        self.set_child(welcome_page)

class InstallerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.luigiano-code.Lightix-installer", flags=0)

    def do_activate(self):
        win = MainWindow(self)
        win.present()

