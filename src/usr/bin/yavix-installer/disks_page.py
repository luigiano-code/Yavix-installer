import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import subprocess


class DisksPage(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.partition_widgets = {}

        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled.set_min_content_height(200)

        self.partitions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.scrolled.set_child(self.partitions_box)

        label = Gtk.Label(label="Select Disk:")
        label.set_halign(Gtk.Align.START)
        self.append(label)

        self.disk_combo = Gtk.ComboBoxText()
        for d in self.list_disks():
            self.disk_combo.append_text(d)
        self.disk_combo.set_active(0)
        self.vbox1.append(self.disk_combo)

        self.refresh_button = Gtk.Button(label="Refresh")
        self.refresh_button.connect("clicked", self.on_refresh_clicked)
        self.vbox1.append(self.refresh_button)

        self.append(self.vbox1)
        self.append(self.scrolled)

        self.disk_combo.connect("changed", self.on_disk_changed)
        self.on_disk_changed(self.disk_combo)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.next_button.add_css_class("suggested-action")
        self.append(self.next_button)

    def on_refresh_clicked(self, button):
        disk = self.disk_combo.get_active_text()
        if disk:
            self.show_partitions(disk)


    def show_partitions(self, disk):
        child = self.partitions_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.partitions_box.remove(child)
            child = next_child

        self.partition_widgets.clear()

        if not disk:
            return

        partitions = self.list_partitions(disk)

        if not partitions:
            self.partitions_box.append(Gtk.Label(label="No partitions found"))
            return

        for p in partitions:
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            row.set_margin_bottom(10)

            title = Gtk.Label(label=p)
            title.set_halign(Gtk.Align.START)

            options = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

            mount_combo = Gtk.ComboBoxText()

            mount_combo.append_text("/")
            mount_combo.append_text("/boot")
            mount_combo.append_text("/home")
            mount_combo.append_text("Custom")
            mount_combo.set_active(0)

            mount_entry = Gtk.Entry()
            mount_entry.set_placeholder_text("/ mount point")
            mount_entry.set_visible(False)


            mount_combo.connect(
                "changed",
                lambda combo, entry=mount_entry: entry.set_visible(
                    combo.get_active_text() == "Custom"
                )
            )

            flags_combo = Gtk.ComboBoxText()
            for f in ["No flag", "boot", "boot & esp", "swap"]:
                flags_combo.append_text(f)
            flags_combo.set_active(0)

            format_check = Gtk.CheckButton(label="Format")

            formats = Gtk.ComboBoxText()
            for fs in ["ext4", "ext3", "ext2", "btrfs", "exfat", "fat32"]:
                formats.append_text(fs)
            formats.set_active(0)
            formats.set_visible(False)

            format_check.connect(
                "toggled",
                lambda btn, combo=formats: combo.set_visible(btn.get_active())
            )

            self.partition_widgets[p] = {
                "mount_combo": mount_combo,
                "mount_entry": mount_entry,
                "flags": flags_combo,
                "format_check": format_check,
                "formats": formats
            }

            options.append(mount_combo)
            options.append(mount_entry)
            options.append(flags_combo)
            options.append(format_check)
            options.append(formats)

            row.append(title)
            row.append(options)

            self.partitions_box.append(row)

    def list_disks(self):
        disks = []
        output = subprocess.check_output(["lsblk", "-dn", "-o", "NAME,TYPE"]).decode()
        for line in output.splitlines():
            name, typ = line.split()
            if typ == "disk":
                disks.append(f"/dev/{name}")
        return disks

    def list_partitions(self, disk, button=None):
        partitions = []
        output = subprocess.check_output(["lsblk", "-ln", "-o", "NAME,TYPE", disk]).decode()
        for line in output.splitlines():
            name, typ = line.split()
            if typ == "part":
                partitions.append(f"/dev/{name}")
        return partitions

    def on_disk_changed(self, combo):
        disk = combo.get_active_text()
        if disk:
            self.show_partitions(disk)


    def on_next_clicked(self, button):
        from installer import partitions_flags
        from installer import partitions_mount_points
        from installer import partitions_format
        import installer

        installer.selected_disk = self.disk_combo.get_active_text()

        partitions_flags.clear()
        partitions_mount_points.clear()
        partitions_format.clear()

        for partition, widgets in self.partition_widgets.items():
            combo_value = widgets["mount_combo"].get_active_text()

            if combo_value == "Custom":
                mount_point = widgets["mount_entry"].get_text()
            else:
                mount_point = combo_value

            flag = widgets["flags"].get_active_text()
            format_enabled = widgets["format_check"].get_active()
            fs = widgets["formats"].get_active_text()

            if mount_point:
                partitions_mount_points[partition] = mount_point
                partitions_flags[partition] = flag

                if format_enabled:
                    partitions_format[partition] = fs
                else:
                    partitions_format[partition] = False
