import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

import subprocess
import threading

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

    def arch_chroot(self, cmd, MNT="/mnt"):
        subprocess.run(["sudo", "arch-chroot", MNT] + cmd)

    def install_system(self):

        import installer

        root = None

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
            if installer.partitions_flags[i] == "boot":
                subprocess.run(["sudo", "parted", "-s", i, "set", "1", "boot", "on"])
            if installer.partitions_flags[i] == "boot & esp":
                subprocess.run(["sudo", "parted", "-s", i, "set", "1", "boot", "on"])
                subprocess.run(["sudo", "parted", "-s", i, "set", "1", "esp", "on"])
            if installer.partitions_flags[i] == "swap":
                subprocess.run(["sudo", "parted", "-s", i, "set", i, "swap", "on"])



        for i in installer.partitions_mount_points.values():
            if i == "/":
                for o in installer.partitions_mount_points:
                    if installer.partitions_mount_points[o] == i:
                        root = o
                        subprocess.run(["sudo", "mount", root, "/mnt"])
        for p in installer.partitions_mount_points:
            mountpoint = "/mnt" + installer.partitions_mount_points[p]
            subprocess.run(["sudo", "mount", "--mkdir", p, mountpoint])

        print("copying airootfs")
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
            "/mnt"
        ]

        subprocess.run(cmd)


        MNT = "/mnt"

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

        self.arch_chroot(["pacman", "-Sy", "linux", "linux-headers", "--noconfirm"])

        self.arch_chroot(["mkinitcpio", "-c", "/etc/mkinitcpio.conf", "-g", "/boot/initramfs-linux.img"])

        self.arch_chroot(["grub-install", "--target=x86_64-efi", "--efi-directory=/boot", "--bootloader-id=YAVIX"])
        self.arch_chroot(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"])

        self.arch_chroot(["sudo", "umount", "/mnt"])

    def on_next_clicked(self, button):

        from installer import settings_password
        from installer import settings_pcname 
        from installer import settings_username

        print("your name: " + settings_username)
        print("your computer`s name: " + settings_pcname)
        print("your password: " + settings_password)

