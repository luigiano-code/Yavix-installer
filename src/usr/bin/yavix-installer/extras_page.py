import gi
import sys
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

class ExtrasPage(Gtk.Box):
	def __init__(self):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.set_margin_top(50)
		self.set_margin_bottom(50)
		self.set_margin_start(50)
		self.set_margin_end(50)

		self.welcome_label = Gtk.Label(label="Optional Enhancements")
		self.welcome_label.set_wrap(True)
		self.welcome_label.set_wrap_mode(Gtk.WrapMode.WORD)
		self.welcome_label.set_halign(Gtk.Align.CENTER)
		self.welcome_label.add_css_class("title-1")
		self.append(self.welcome_label)

		self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

		self.checkbox_gamemode = Gtk.CheckButton(label="Enable GameMode")
		self.vbox1.append(self.checkbox_gamemode)

		self.checkbox_gamescope = Gtk.CheckButton(label="Enable GameScope")
		self.vbox1.append(self.checkbox_gamescope)

		self.checkbox_wine = Gtk.CheckButton(label="Install wine")
		self.vbox1.append(self.checkbox_wine)
	
		self.checkbox_linuxzen = Gtk.CheckButton(label="Install Linux-zen")
		self.vbox2.append(self.checkbox_linuxzen)
		
		self.checkbox_steam = Gtk.CheckButton(label="Install steam")
		self.vbox2.append(self.checkbox_steam)

		self.append(self.vbox1)
		self.append(self.vbox2)

		self.next_button = Gtk.Button(label="Next")
		self.next_button.set_halign(Gtk.Align.CENTER)
		self.next_button.add_css_class("suggested-action")
		self.next_button.connect("clicked", self.on_start_clicked)
		self.next_button.set_size_request(200, 50)
		self.append(self.next_button)

	def on_start_clicked(self, button):
		import setup

		setup.extras = []
		if self.checkbox_gamemode.get_active():
			setup.extras.append("gamemode")

		if self.checkbox_gamescope.get_active():
			setup.extras.append("gamescope")

		if self.checkbox_wine.get_active():
			setup.extras.append("wine")

		if self.checkbox_linuxzen.get_active():
			setup.extras.append("linux-zen")

		if self.checkbox_steam.get_active():
			setup.extras.append("steam")

							

