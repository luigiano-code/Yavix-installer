#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
import sys

from welcome_page import WelcomePage
from language_page import LanguagePage
from disks_page import DisksPage
from partitions_page import PartitionsPage

partitions_flags = {}
partitions_mount_points = {}
partitions_format = {}

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Lightix Installer")
        self.set_default_size(600, 400)
        self.set_resizable(False)

        self.stack = Gtk.Stack()
        self.set_child(self.stack)

        self.welcome_page = WelcomePage()
        self.language_page = LanguagePage()
        self.disks_page = DisksPage()
        self.partitions_page = PartitionsPage()

        self.stack.add_named(self.welcome_page, "welcome")
        self.stack.add_named(self.language_page, "language")
        self.stack.add_named(self.partitions_page, "partitions")
        self.stack.add_named(self.disks_page, "disks")

        self.welcome_page.start_button.connect("clicked", self.show_language_page)
        self.language_page.next_button.connect("clicked", self.show_partitions_page)
        self.partitions_page.next_button.connect("clicked", self.show_disks_page)
        self.stack.set_visible_child_name("welcome")

    def show_partitions_page(self, button):
        self.stack.set_visible_child_name("partitions")

    def show_language_page(self, button):
        self.stack.set_visible_child_name("language")

    def show_disks_page(self, button):
        self.stack.set_visible_child_name("disks")

class InstallerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.luigiano-code.Lightix-installer")

    def do_activate(self):
        win = MainWindow(self)
        win.present()

if __name__ == "__main__":
    app = InstallerApp()
    app.run(sys.argv)
