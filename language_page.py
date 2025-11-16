import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

class LanguagePage(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_margin_top(50)
        self.set_margin_bottom(50)
        self.set_margin_start(50)
        self.set_margin_end(50)

        title = Gtk.Label(label="Select language and localization")
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.CENTER)
        self.append(title)

        self.lang_combo = Gtk.ComboBoxText()
        self.lang_combo.append_text("English")
        self.lang_combo.set_active(0)
        self.append(self.lang_combo)

        self.tz_combo = Gtk.ComboBoxText()
        self.tz_combo.append_text("Europe/London")
        self.tz_combo.append_text("America/New_York")
        self.tz_combo.set_active(0)
        self.append(self.tz_combo)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.add_css_class("suggested-action")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.append(self.next_button)

    def on_next_clicked(self, button):
        lang = self.lang_combo.get_active_text()
        tz = self.tz_combo.get_active_text()
        print(f"Selected language: {lang}, selected timezone: {tz}")
