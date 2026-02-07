import gi
import sys
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import os

class OfficePage(Gtk.Box):
	def __init__(self):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.set_margin_top(50)
		self.set_margin_bottom(50)
		self.set_margin_start(50)
		self.set_margin_end(50)

		self.welcome_label = Gtk.Label(label="Select your office")
		self.welcome_label.set_wrap(True)
		self.welcome_label.set_wrap_mode(Gtk.WrapMode.WORD)
		self.welcome_label.set_halign(Gtk.Align.CENTER)
		self.welcome_label.add_css_class("title-1")
		self.append(self.welcome_label)

		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		svg_path = os.path.join(BASE_DIR, "images", "libreoffice.svg")

		self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
		
		icon_size = 128

		self.libreoffice_button = Gtk.Button()
		self.libreoffice_button.office = "libreoffice"
		self.libreoffice_icon = Gtk.Image.new_from_file(svg_path)
		self.libreoffice_icon.set_pixel_size(icon_size)
		self.libreoffice_button.set_child(self.libreoffice_icon)
		self.libreoffice_button.connect("clicked", self.on_office_clicked)

		svg_path = os.path.join(BASE_DIR, "images", "onlyoffice.svg")

		self.onlyoffice_button = Gtk.Button()
		self.onlyoffice_button.office = "onlyoffice"		
		self.onlyoffice_icon = Gtk.Image.new_from_file(svg_path)
		self.onlyoffice_icon.set_pixel_size(icon_size)
		self.onlyoffice_button.set_child(self.onlyoffice_icon)
		self.onlyoffice_button.connect("clicked", self.on_office_clicked)

		self.libreoffice_button.set_hexpand(True)
		self.onlyoffice_button.set_hexpand(True)

		self.vbox1.append(self.libreoffice_button)
		self.vbox1.append(self.onlyoffice_button)
		self.append(self.vbox1)

		self.next_button = Gtk.Button(label="Next")
		self.next_button.set_halign(Gtk.Align.CENTER)
		self.next_button.add_css_class("suggested-action")
		self.next_button.set_size_request(200, 50)
		self.next_button.set_visible(False)
		self.append(self.next_button)

	def on_office_clicked(self, button):
		import setup

		setup.office = button.office
		self.next_button.set_visible(True)	
			

