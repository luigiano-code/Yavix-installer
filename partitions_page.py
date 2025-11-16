import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import subprocess

class PartitionsPage(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_margin_top(50)
        self.set_margin_bottom(50)
        self.set_margin_start(50)
        self.set_margin_end(50)

        title = Gtk.Label(label="Creating partitions")
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.CENTER)
        self.append(title)

        self.open_gparted = Gtk.Button(label = "Open Gparted")
        self.open_gparted.connect("clicked", self.on_gparted_clicked)
        self.append(self.open_gparted)

        self.erase_disk = Gtk.Button(label="Erase disk and install Lightix")
        self.erase_disk.connect("clicked", self.on_erase_clicked)
        self.append(self.erase_disk)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.add_css_class("suggested-action")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.append(self.next_button)

    def on_erase_clicked(self, button):
        print("die")

    def on_next_clicked(self, button):
        print("next")

    def on_gparted_clicked(self, button):
        subprocess.Popen(["gparted"])
