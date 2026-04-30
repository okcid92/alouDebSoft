#!/usr/bin/env python3
"""
Minimal GTK GUI for Alou — lightweight dashboard and actions.
Requires: python3-gi
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import subprocess
import threading


class AlouWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Alou ⚡ Toolbox")
        self.set_default_size(900, 600)
        self.set_border_width(8)

        # Apply simple dark CSS
        css = b"""
        window { background-color: #0D1117; color: #C9D1D9; }
        .surface { background-color: #161B22; border-radius: 8px; border: 1px solid #30363D; }
        .primary { background-color: #58A6FF; color: #0D1117; }
        .card { padding: 12px; margin: 6px; }
        """
        style = Gtk.CssProvider()
        style.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.add(hbox)

        # Sidebar
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        sidebar.set_size_request(220, -1)
        sidebar.get_style_context().add_class('surface')

        for name in ["Dashboard", "Actions", "Cleanup", "Install", "Network", "Downloads", "Settings"]:
            btn = Gtk.Button(label=name)
            btn.set_halign(Gtk.Align.FILL)
            btn.connect("clicked", self.on_nav_clicked)
            sidebar.pack_start(btn, False, False, 6)

        # Main area
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main.get_style_context().add_class('surface')

        title = Gtk.Label()
        title.set_markup('<span size="xx-large" weight="bold">Alou ⚡ Toolbox</span>')
        title.set_halign(Gtk.Align.START)
        main.pack_start(title, False, False, 8)

        # Quick action cards
        cards = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cards.set_halign(Gtk.Align.START)

        btn_update = Gtk.Button(label="Update System")
        btn_update.get_style_context().add_class('primary')
        btn_update.connect("clicked", self.on_update_clicked)
        cards.pack_start(btn_update, False, False, 0)

        btn_clean = Gtk.Button(label="Clean Project")
        btn_clean.connect("clicked", self.on_clean_clicked)
        cards.pack_start(btn_clean, False, False, 0)

        main.pack_start(cards, False, False, 8)

        # Logs area
        self.logview = Gtk.TextView()
        self.logview.set_editable(False)
        self.logview.set_wrap_mode(Gtk.WrapMode.WORD)
        font_desc = PangoFont = None
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.logview)
        scrolled.set_vexpand(True)
        main.pack_start(scrolled, True, True, 8)

        hbox.pack_start(sidebar, False, False, 0)
        hbox.pack_start(main, True, True, 0)

    def on_nav_clicked(self, widget):
        self.append_log(f"Navigation: {widget.get_label()}")

    def on_update_clicked(self, widget):
        self.append_log("Lancement: update système...")
        threading.Thread(target=self.run_cmd, args=(['/usr/bin/sudo','apt-get','update','-y'],)).start()

    def on_clean_clicked(self, widget):
        self.append_log("Lancement: nettoyage (node) dans le répertoire courant")
        threading.Thread(target=self.run_cmd, args=(['/bin/sh','-c','find . -type d -name node_modules -prune -exec rm -rf {} +'],)).start()

    def append_log(self, text):
        buf = self.logview.get_buffer()
        end = buf.get_end_iter()
        buf.insert(end, text + "\n")

    def run_cmd(self, cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in p.stdout:
                GLib.idle_add(self.append_log, line.rstrip())
            p.wait()
            GLib.idle_add(self.append_log, f"Commande terminée: {cmd} -> {p.returncode}")
        except Exception as e:
            GLib.idle_add(self.append_log, f"Erreur: {e}")


def main():
    win = AlouWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
