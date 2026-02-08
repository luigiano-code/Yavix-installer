import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

import subprocess
import threading

import re

class InstallationPage(Gtk.Box):
	def __init__(self):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		self.set_margin_top(50)
		self.set_margin_bottom(50)
		self.set_margin_start(50)
		self.set_margin_end(50)

		title = Gtk.Label(label="Installation started!")
		title.add_css_class("title-1")
		title.set_halign(Gtk.Align.CENTER)
		self.append(title)

		self.next_button = Gtk.Button(label="Next")
		self.next_button.add_css_class("suggested-action")
		self.next_button.connect("clicked", self.on_next_clicked)
		self.next_button.set_visible(False)
		self.append(self.next_button)

	def arch_chroot(self, cmd, MNT="/mnt"):
		subprocess.run(["sudo", "arch-chroot", MNT] + cmd)

	def install_system(self):
		from installer import settings_password
		from installer import settings_pcname 
		from installer import settings_username
		import installer

		root = None

		MNT = "/mnt"

		for i in installer.partitions_format:
			fmt = str(installer.partitions_format[i]).lower()

			if fmt == "ext4":
				subprocess.run(["sudo", "mkfs.ext4", "-F", i])

			if fmt == "ext3":
				subprocess.run(["sudo", "mkfs.ext3", "-F", i])

			if fmt == "ext2":
				subprocess.run(["sudo", "mkfs.ext2", "-F", i])

			if fmt == "exfat":
				subprocess.run(["sudo", "mkfs.exfat", "-f", i])

			if fmt == "btrfs":
				subprocess.run(["sudo", "mkfs.btrfs", "-f", i])

			if fmt == "fat32":
				subprocess.run(["sudo", "mkfs.fat", "-F", "32", "-I", i])

		for i in installer.partitions_flags:
			partition = i

			num_str = ""
			for c in reversed(partition):
				if c.isdigit():
					num_str = c + num_str
				else:
					break

			partition_number = int(num_str)

			if installer.partitions_flags[i] == "boot":
				subprocess.run(["sudo", "parted", "-s", installer.selected_disk, "set", str(partition_number), "boot", "on"])
			if installer.partitions_flags[i] == "boot & esp":
				subprocess.run(["sudo", "parted", "-s", installer.selected_disk, "set", str(partition_number), "boot", "on"])
				subprocess.run(["sudo", "parted", "-s", installer.selected_disk, "set", str(partition_number), "esp", "on"])
			if installer.partitions_flags[i] == "swap":
				subprocess.run(["sudo", "parted", "-s", installer.selected_disk, "set", str(partition_number), "swap", "on"])

		for i in installer.partitions_mount_points.values():
			if i == "/":
				for o in installer.partitions_mount_points:
					if installer.partitions_mount_points[o] == i:
						root = o
						subprocess.run(["sudo", "mount", root, MNT])
		for p in installer.partitions_mount_points:
			mountpoint = MNT + installer.partitions_mount_points[p]
			if mountpoint == MNT + "/":
				pass
			else:
				subprocess.run(["sudo", "mount", "--mkdir", p, mountpoint])

		cmd = [
			"sudo",
			"rsync",
			"-aAXHv",
			"--exclude=/dev/*",
			"--exclude=/proc/*",
			"--exclude=/sys/*",
			"--exclude=/tmp/*",
			"--exclude=/run/*",
			"--exclude=/mnt/*",
			"--exclude=/media/*",
			"--exclude=/lost+found",
			"/",
			MNT
		]

		subprocess.run(cmd)

		subprocess.run(["sudo", "mount", "--bind", "/dev", f"{MNT}/dev"])
		subprocess.run(["sudo", "mount", "--bind", "/proc", f"{MNT}/proc"])
		subprocess.run(["sudo", "mount", "--bind", "/sys", f"{MNT}/sys"])
		subprocess.run(["sudo", "mount", "--bind", "/run", f"{MNT}/run"])

		subprocess.run([
			"sudo",
			"sh",
			"-c",
			f"genfstab -U {MNT} > {MNT}/etc/fstab"
		])

		self.arch_chroot(["mv", "/etc/mkinitcpio.d/linux.preset", "/etc/mkinitcpio.d/linux.preset.bak"])
		self.arch_chroot(["mv", "/etc/mkinitcpio.d/installedlinux.preset", "/etc/mkinitcpio.d/linux.preset"])
		self.arch_chroot(["cp", "/etc/mkinitcpio.conf", "/etc/mkinitcpio.conf.d/mkinitcpio.conf"])
		self.arch_chroot(["rm", "-f", "/etc/mkinitcpio.conf.d/archiso.conf"])

		self.arch_chroot(["useradd", "-m", "-G", "wheel", "-s", "/bin/bash", settings_username])
		self.arch_chroot(["sh", "-c", f"echo 'root:{settings_password}' | chpasswd"])
		self.arch_chroot(["sh", "-c", f"echo '{settings_username}:{settings_password}' | chpasswd"])
		self.arch_chroot(["sh", "-c", f"echo '{settings_pcname}' > /etc/hostname"])
		self.arch_chroot(["sudo", "userdel", "-r", "liveuser"])
		self.arch_chroot(["sudo", "groupdel", "liveuser"])
		self.arch_chroot(["sudo", "mkdir", "-p", "/home/" + settings_username])
		self.arch_chroot(["sudo", "chown", "-R", settings_username + ":" + settings_username, "/home/" + settings_username])
		self.arch_chroot(["sudo", "chmod", "700", "/home/" + settings_username])

		self.arch_chroot(["sh", "-c", f"echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen"])
		self.arch_chroot(["sh", "-c", f"echo '{installer.language}' >> /etc/locale.gen"])
		self.arch_chroot(["locale-gen"])
		self.arch_chroot(["sh", "-c", f"echo 'LANG={installer.language}' > /etc/locale.conf"])
		self.arch_chroot(["ln", "-sf", f"/usr/share/zoneinfo/{installer.timezone}", "/etc/localtime"])
		self.arch_chroot(["hwclock", "--systohc"])
		self.arch_chroot(["sh", "-c", "echo '' > /etc/motd"])

		services = [
			"systemd-logind",
			"dbus",
			"NetworkManager",
			"gdm"
		]

		for service in services:
			self.arch_chroot(["sudo", "systemctl", "enable", service])

		self.arch_chroot(["pacman", "-Sy", "linux", "linux-headers", "--noconfirm"])
		self.arch_chroot(["pacman", "-Rns", "yavix-installer", "--noconfirm"])

		self.arch_chroot(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"])
		self.arch_chroot(["flatpak", "install", "-y", "flathub", "org.localsend.localsend_app"])

		if installer.browser == "zen":
			self.arch_chroot(["flatpak", "install", "-y", "flathub", "app.zen_browser.zen"])
			self.arch_chroot(["pacman", "-Rns", "firefox", "--noconfirm"])

		elif installer.browser == "brave":
			self.arch_chroot(["flatpak", "install", "-y", "flathub", "com.brave.Browser"])
			self.arch_chroot(["pacman", "-Rns", "firefox", "--noconfirm"])

		if installer.office == "libreoffice":
			self.arch_chroot(["flatpak", "install", "-y", "flathub", "org.libreoffice.LibreOffice"])

		elif installer.office == "onlyoffice":
			self.arch_chroot(["flatpak", "install", "-y", "flathub", "org.onlyoffice.desktopeditors"])

		self.arch_chroot(["mkinitcpio", "-c", "/etc/mkinitcpio.conf", "-g", "/boot/initramfs-linux.img"])

		self.arch_chroot(["grub-install", "--target=x86_64-efi", "--efi-directory=/boot", "--bootloader-id=YAVIX"])
		self.arch_chroot(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"])

	def on_next_clicked(self, button):
		pass
