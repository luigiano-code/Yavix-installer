import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib


class SettingPage(Gtk.Box):
    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.main_window = main_window 
        self.set_margin_top(50)
        self.set_margin_bottom(50)
        self.set_margin_start(50)
        self.set_margin_end(50)

        self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.labelUsername = Gtk.Label(label="Enter your name:")
        self.labelUsername.set_halign(Gtk.Align.START)
        self.vbox1.append(self.labelUsername)

        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Set your name here")
        self.vbox1.append(self.username_entry)

        self.labelPCName = Gtk.Label(label="Your computer`s name")
        self.labelPCName.set_halign(Gtk.Align.START)
        self.vbox2.append(self.labelPCName)

        self.PCName_entry = Gtk.Entry()
        self.PCName_entry.set_placeholder_text("computer`s name here")
        self.vbox2.append(self.PCName_entry)

        self.labelPassword = Gtk.Label(label="Enter your password:")
        self.labelPassword.set_halign(Gtk.Align.START)
        self.vbox3.append(self.labelPassword)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("password here")
        self.vbox3.append(self.password_entry)

        self.confirm_entry = Gtk.Entry()
        self.confirm_entry.set_placeholder_text("confirm password")
        self.vbox3.append(self.confirm_entry)

        self.append(self.vbox1)
        self.append(self.vbox2)
        self.append(self.vbox3)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.add_css_class("suggested-action")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.append(self.next_button)

    def on_next_clicked(self, button):
        import installer

        installer.settings_password = self.password_entry.get_text()
        installer.settings_pcname = self.PCName_entry.get_text()
        installer.settings_username = self.username_entry.get_text()

        if installer.settings_password == self.confirm_entry.get_text():
            self.main_window.show_browser_page()
