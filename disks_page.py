import gi
from bauh.gems.flatpak.worker import FlatpakAsyncDataLoader
from wx.lib.inspection import orientFlags

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
        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        label = Gtk.Label(label="Select Disk:")
        label.set_halign(Gtk.Align.START)
        self.append(label)

        self.disk_combo = Gtk.ComboBoxText()
        for d in self.list_disks():
            self.disk_combo.append_text(d)
        self.disk_combo.set_active(0)
        self.vbox1.append(self.disk_combo)

        self.partition_combo = Gtk.ComboBoxText()
        self.partition_combo.append_text("Disk not selected")
        self.partition_combo.set_active(0)
        self.vbox1.append(self.partition_combo)

        self.append(self.vbox1)

        self.disk_combo.connect("changed", self.on_disk_changed)
        self.on_disk_changed(self.disk_combo)

        label2 = Gtk.Label(label="Select mount point:")
        label2.set_halign(Gtk.Align.START)
        self.vbox2.append(label2)

        self.mount_entry = Gtk.Entry()
        self.mount_entry.set_placeholder_text("Set mount point")
        self.vbox2.append(self.mount_entry)

        label3 = Gtk.Label(label="Select flag:")
        label3.set_halign(Gtk.Align.START)
        self.vbox3.append(label3)

        self.flags_combo = Gtk.ComboBoxText()
        self.flags_combo.append_text("Brak")
        self.flags_combo.append_text("boot")
        self.flags_combo.append_text("esp")
        self.flags_combo.append_text("swap")
        self.flags_combo.set_active(0)
        self.vbox3.append(self.flags_combo)

        self.append(self.vbox2)
        self.append(self.vbox3)

        self.checkbox = Gtk.CheckButton(label="format partition")
        self.checkbox.connect("toggled", self.on_toggled)
        self.vbox4.append(self.checkbox)

        self.formats = Gtk.ComboBoxText()
        self.formats.append_text("ext4")
        self.formats.append_text("ext3")
        self.formats.append_text("ext2")
        self.formats.append_text("btrfs")
        self.formats.append_text("exfat")
        self.formats.append_text("fat32")
        self.formats.set_active(0)
        self.formats.set_visible(False)
        self.vbox4.append(self.formats)

        self.append(self.vbox4)

        self.apply_button = Gtk.Button(label="Set for partition")
        self.apply_button.connect(
            "clicked",
            lambda btn: self.on_apply_clicked(
                btn,
                self.partition_combo.get_active_text(),
                self.mount_entry.get_text(),
                self.flags_combo.get_active_text()
            )
        )

        self.apply_button.add_css_class("suggested-action")
        self.append(self.apply_button)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.next_button.add_css_class("suggested-action")
        self.append(self.next_button)

    def list_disks(self):
        disks = []
        output = subprocess.check_output(["lsblk", "-dn", "-o", "NAME,TYPE"]).decode()
        for line in output.splitlines():
            name, typ = line.split()
            if typ == "disk":
                disks.append(f"/dev/{name}")
        return disks

    def list_partitions(self, disk):
        partitions = []
        output = subprocess.check_output(["lsblk", "-ln", "-o", "NAME,TYPE", disk]).decode()
        for line in output.splitlines():
            name, typ = line.split()
            if typ == "part":
                partitions.append(f"/dev/{name}")
        return partitions

    def on_toggled(self, button):
        self.formats.set_visible(button.get_active())

    def on_apply_clicked(self, button, partition, mount_point, flag):
        from installer import partitions_flags
        from installer import partitions_mount_points
        from installer import partitions_format

        self.partition_flags = partitions_flags
        self.partition_mount_points = partitions_mount_points
        self.partition_format = partitions_format

        self.partition_flags.update({partition: flag})
        self.partition_mount_points.update({partition: mount_point})
        if self.checkbox.get_active():
            self.partition_format.update({partition: self.formats.get_active_text()})
        else:
            self.partition_format.update({partition: False})

    def on_disk_changed(self, combo):
        disk = combo.get_active_text()
        self.partition_combo.remove_all()
        partitions = self.list_partitions(disk)
        if partitions:
            for p in partitions:
                self.partition_combo.append_text(p)
        else:
            self.partition_combo.append_text("No partition")
        self.partition_combo.set_active(0)

    def on_next_clicked(self, button):
            print(f"Selected Disk: {self.disk_combo.get_active_text()}")
            print(f"Selected Partition: {self.partition_combo.get_active_text()}")
            print(self.partition_flags)
            print(self.partition_mount_points)
            print(self.partition_format)

