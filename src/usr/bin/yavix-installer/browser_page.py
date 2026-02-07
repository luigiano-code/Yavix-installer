import gi
import sys
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import os

class BrowserPage(Gtk.Box):
	def __init__(self):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.set_margin_top(50)
		self.set_margin_bottom(50)
		self.set_margin_start(50)
		self.set_margin_end(50)

		self.welcome_label = Gtk.Label(label="Select your browser")
		self.welcome_label.set_wrap(True)
		self.welcome_label.set_wrap_mode(Gtk.WrapMode.WORD)
		self.welcome_label.set_halign(Gtk.Align.CENTER)
		self.welcome_label.add_css_class("title-1")
		self.append(self.welcome_label)

		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		svg_path = os.path.join(BASE_DIR, "images", "firefox.svg")

		self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
		
		icon_size = 128

		self.firefox_button = Gtk.Button()
		self.firefox_button.browser = "firefox"
		self.firefox_icon = Gtk.Image.new_from_file(svg_path)
		self.firefox_icon.set_pixel_size(icon_size)
		self.firefox_button.set_child(self.firefox_icon)
		self.firefox_button.connect("clicked", self.on_browser_clicked)

		svg_path = os.path.join(BASE_DIR, "images", "zen.svg")

		self.zen_button = Gtk.Button()
		self.zen_button.browser = "zen"		
		self.zen_icon = Gtk.Image.new_from_file(svg_path)
		self.zen_icon.set_pixel_size(icon_size)
		self.zen_button.set_child(self.zen_icon)
		self.zen_button.connect("clicked", self.on_browser_clicked)

		svg_path = os.path.join(BASE_DIR, "images", "brave.svg")

		self.brave_button = Gtk.Button()
		self.brave_button.browser = "brave"
		self.brave_icon = Gtk.Image.new_from_file(svg_path)
		self.brave_icon.set_pixel_size(icon_size)
		self.brave_button.set_child(self.brave_icon)
		self.brave_button.connect("clicked", self.on_browser_clicked)

		self.firefox_button.set_hexpand(True)
		self.zen_button.set_hexpand(True)
		self.brave_button.set_hexpand(True)

		self.vbox1.append(self.firefox_button)
		self.vbox1.append(self.zen_button)
		self.vbox1.append(self.brave_button)
		self.append(self.vbox1)

		self.next_button = Gtk.Button(label="Next")
		self.next_button.set_halign(Gtk.Align.CENTER)
		self.next_button.add_css_class("suggested-action")
		self.next_button.set_size_request(200, 50)
		self.next_button.set_visible(False)
		self.append(self.next_button)

	def on_browser_clicked(self, button):
		import installer

		installer.browser = button.browser
		self.next_button.set_visible(True)

		print(installer.browser)	
			

