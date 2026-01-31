#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import sys
import threading

from welcome_page import WelcomePage
from language_page import LanguagePage
from disks_page import DisksPage
from partitions_page import PartitionsPage
from setting_page import SettingPage
from installation_page import InstallationPage

partitions_flags = {}
partitions_mount_points = {}
partitions_format = {}

settings_username = None
settings_password = None
settings_pcname = None


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Yavix Installer")
        self.set_default_size(600, 400)
        self.set_resizable(False)

        self.stack = Gtk.Stack()
        self.set_child(self.stack)

        self.welcome_page = WelcomePage()
        self.language_page = LanguagePage()
        self.disks_page = DisksPage()
        self.partitions_page = PartitionsPage()
        self.setting_page = SettingPage()
        self.installation_page = InstallationPage()

        self.stack.add_named(self.welcome_page, "welcome")
        self.stack.add_named(self.language_page, "language")
        self.stack.add_named(self.partitions_page, "partitions")
        self.stack.add_named(self.disks_page, "disks")
        self.stack.add_named(self.setting_page, "setting")
        self.stack.add_named(self.installation_page, "installation")

        self.welcome_page.start_button.connect("clicked", self.show_language_page)
        self.language_page.next_button.connect("clicked", self.show_partitions_page)
        self.partitions_page.next_button.connect("clicked", self.show_disks_page)
        self.disks_page.next_button.connect("clicked", self.show_setting_page)
        self.setting_page.next_button.connect("clicked", self.show_installation_page)
        self.stack.set_visible_child_name("welcome")

    def show_partitions_page(self, button):
        self.stack.set_visible_child_name("partitions")

    def show_language_page(self, button):
        self.stack.set_visible_child_name("language")

    def show_disks_page(self, button):
        self.stack.set_visible_child_name("disks")

    def show_setting_page(self, button):
        self.stack.set_visible_child_name("setting")

    def install_done(self):
        InstallationPage().append(InstallationPage().next_button)

    def install_thread(self):
        InstallationPage().install_system()
        GLib.idle_add(self.install_done)

    def show_installation_page(self, button):
        self.stack.set_visible_child_name("installation")
        t = threading.Thread(target=self.install_thread)
        t.daemon = True
        t.start()
     

class InstallerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.luigiano-code.Yavix-installer")

    def do_activate(self):
        win = MainWindow(self)
        win.present()

if __name__ == "__main__":
    app = InstallerApp()
    app.run(sys.argv)