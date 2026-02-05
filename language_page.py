import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import os

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
		self.lang_combo.set_active(0)
		self.lang_combo.connect("changed", self.on_lang_changed)
		self.append(self.lang_combo)
		
		self.sub_lang_combo = Gtk.ComboBoxText()
		self.sub_lang_combo.set_active(0)
		self.append(self.sub_lang_combo)

		self.tz_combo = Gtk.ComboBoxText()
		self.tz_combo.set_active(0)
		self.tz_combo.connect("changed", self.on_timezone_changed)
		self.append(self.tz_combo)
		
		self.sub_tz_combo = Gtk.ComboBoxText()
		self.sub_tz_combo.set_active(0)
		self.append(self.sub_tz_combo)


		self.next_button = Gtk.Button(label="Next")
		self.next_button.add_css_class("suggested-action")
		self.next_button.connect("clicked", self.on_next_clicked)
		self.append(self.next_button)

		self.get_languages()
		self.get_regions()

	def get_regions(self):
		SKIP_DIRS = {"posix", "right"}

		for d in os.listdir("/usr/share/zoneinfo"):
			path = os.path.join("/usr/share/zoneinfo", d)
			if os.path.isdir(path) and d not in SKIP_DIRS:
				self.tz_combo.append_text(d)

	def on_timezone_changed(self, timezone_combo):
		region = timezone_combo.get_active_text()
		base = os.path.join("/usr/share/zoneinfo", region)

		for root, _, files in os.walk(base):
			for f in files:
				full = os.path.join(root, f)
				city = full.replace(base + "/", "")
				self.sub_tz_combo.append_text(city)

	def get_languages(self):
		filename = "locales.txt"
		top_langs = [
			"ar_SA", "bg_BG", "cs_CZ", "da_DK", "de_DE", "el_GR", "en_GB",
			"en_US", "es_ES", "fi_FI", "fr_FR", "he_IL", "hi_IN", "hu_HU",
			"it_IT", "ja_JP", "ko_KR", "nl_NL", "no_NO", "pl_PL", "pt_BR",
			"pt_PT", "ro_RO", "ru_RU", "sk_SK", "sv_SE", "tr_TR", "uk_UA",
			"zh_CN",
			"zh_TW",
		]

		langs = []
		readable_langs = []

		with open(filename, "r", encoding="utf-8") as f:
			for line in f:
				line = line.strip().lstrip("#")
				if line == "":
					continue

				lang_code = line.split(".")[0].split()[0].split("@")[0]
				langs.append(lang_code)

		seen = set()
		for lang in langs:
			if lang not in seen:
				readable_langs.append(lang)
				seen.add(lang)

		final_langs = []

		for lang in top_langs:
			if lang in readable_langs:
				final_langs.append(lang)
				readable_langs.remove(lang)

		final_langs.append("-------------------------------------------------")
		final_langs.append("                 OTHER LANGUAGES                 ")
		final_langs.append("-------------------------------------------------")
		final_langs.extend(sorted(readable_langs))


		for i in final_langs:
			self.lang_combo.append_text(i)

	def on_lang_changed(self, lang_combo):
		getlang = lang_combo.get_active_text()
		
		if getlang == "-------------------------------------------------" or getlang == "                 OTHER LANGUAGES                 ":
			self.sub_lang_combo.remove_all()
			return

		filename = "locales.txt"
		selected_langs = []

		with open(filename, "r", encoding="utf-8") as f:
			for line in f:
				line = line.strip().lstrip("#")
				if line == "":
					continue

				if line.startswith(getlang) and "UTF-8" in line:
					selected_langs.append(line)

		self.sub_lang_combo.remove_all()
		for lang in selected_langs:
			self.sub_lang_combo.append_text(lang)

		if selected_langs:
			self.sub_lang_combo.set_active(0)


	def on_next_clicked(self, button):
		import installer
		installer.language = self.sub_lang_combo.get_active_text()
		installer.timezone = self.tz_combo.get_active_text() + "/" + self.sub_tz_combo.get_active_text()
		print(installer.language)
		print(installer.timezone)
