import gi
import sys
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import os

class InternetPage(Gtk.Box):
	def __init__(self):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.set_margin_top(50)
		self.set_margin_bottom(50)
		self.set_margin_start(50)
		self.set_margin_end(50)

		self.internet_label = Gtk.Label(label="No Internet connection")
		self.internet_label.set_wrap(True)
		self.internet_label.set_wrap_mode(Gtk.WrapMode.WORD)
		self.internet_label.set_halign(Gtk.Align.CENTER)
		self.internet_label.add_css_class("title-1")
		self.append(self.internet_label)

		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		svg_path = os.path.join(BASE_DIR, "images", "no_connection.svg")

		self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
		
		icon_size = 512

		self.no_connection_button = Gtk.Button()
		self.no_connection_icon = Gtk.Image.new_from_file(svg_path)
		self.no_connection_icon.set_pixel_size(icon_size)
		self.no_connection_button.set_child(self.no_connection_icon)

		self.no_connection_button.set_hexpand(True)

		self.vbox1.append(self.no_connection_button)
		self.append(self.vbox1)


