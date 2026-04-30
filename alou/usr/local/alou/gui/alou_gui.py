#!/usr/bin/env python3
"""Alou GTK GUI."""

import os
import shutil
import socket
import subprocess
import threading

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, GLib, Gtk


class AlouWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Alou Toolbox")
        self.set_default_size(1180, 760)
        self.set_border_width(0)

        self._running_processes = set()
        self._page_buttons = {}

        self._install_css()

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root)

        root.pack_start(self._build_header(), False, False, 0)

        body = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        body.set_hexpand(True)
        body.set_vexpand(True)
        root.pack_start(body, True, True, 0)

        self.sidebar = self._build_sidebar()
        body.pack_start(self.sidebar, False, False, 0)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(180)
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        body.pack_start(self.stack, True, True, 0)

        self.status_label = Gtk.Label(label="Ready")
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.set_xalign(0.0)
        self.status_label.get_style_context().add_class('status-text')

        root.pack_start(self._build_footer(), False, False, 0)

        self._build_pages()
        self._set_page('dashboard')
        self._refresh_system_info()

    def _install_css(self):
        css = b"""
        * {
            font-family: Sans;
        }

        window, .app-shell {
            background: #0b1220;
            color: #e5eefb;
        }

        .header {
            background: linear-gradient(90deg, #0f172a, #12233f);
            border-bottom: 1px solid #22314f;
            padding: 18px 20px;
        }

        .header-title {
            font-size: 22px;
            font-weight: 700;
            color: #f5faff;
        }

        .header-subtitle {
            color: #92a4c3;
            font-size: 12px;
        }

        .sidebar {
            min-width: 240px;
            background: #0f172a;
            border-right: 1px solid #22314f;
            padding: 16px;
        }

        .nav-button {
            background: #12233f;
            color: #dce7f7;
            border-radius: 12px;
            border: 1px solid #22314f;
            padding: 12px 14px;
            margin-bottom: 8px;
        }

        .nav-button.active {
            background: #1d4ed8;
            color: #ffffff;
            border-color: #3b82f6;
        }

        .content {
            background: #0b1220;
            padding: 18px;
        }

        .page-title {
            font-size: 24px;
            font-weight: 700;
            color: #f5faff;
        }

        .page-desc {
            color: #92a4c3;
            margin-top: 4px;
            margin-bottom: 16px;
        }

        .card {
            background: #111c33;
            border: 1px solid #22314f;
            border-radius: 16px;
            padding: 16px;
        }

        .card-title {
            font-size: 14px;
            font-weight: 700;
            color: #a9c2ff;
        }

        .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: #f8fbff;
        }

        .metric-label {
            color: #92a4c3;
        }

        .section-title {
            font-size: 16px;
            font-weight: 700;
            color: #eff5ff;
        }

        .primary-button {
            background: #1d4ed8;
            color: #ffffff;
            border-radius: 12px;
            border: 1px solid #3b82f6;
            padding: 10px 14px;
        }

        .secondary-button {
            background: #12233f;
            color: #dce7f7;
            border-radius: 12px;
            border: 1px solid #22314f;
            padding: 10px 14px;
        }

        .danger-button {
            background: #7f1d1d;
            color: #ffffff;
            border-radius: 12px;
            border: 1px solid #ef4444;
            padding: 10px 14px;
        }

        .status-bar {
            background: #0f172a;
            border-top: 1px solid #22314f;
            padding: 10px 16px;
        }

        .status-text {
            color: #92a4c3;
        }

        textview, textview text {
            background: #07111f;
            color: #dbeafe;
            caret-color: #dbeafe;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        screen = Gdk.Screen.get_default()
        if screen is not None:
            Gtk.StyleContext.add_provider_for_screen(
                screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

    def _build_header(self):
        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header.get_style_context().add_class('header')

        title = Gtk.Label()
        title.set_markup('<span size="xx-large" weight="bold">Alou Toolbox</span>')
        title.set_halign(Gtk.Align.START)
        title.set_xalign(0.0)

        subtitle = Gtk.Label(label='Developer actions, cleanup, downloads and system helpers in one place.')
        subtitle.get_style_context().add_class('header-subtitle')
        subtitle.set_halign(Gtk.Align.START)
        subtitle.set_xalign(0.0)

        header.pack_start(title, False, False, 0)
        header.pack_start(subtitle, False, False, 0)
        return header

    def _build_sidebar(self):
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        sidebar.get_style_context().add_class('sidebar')

        nav_title = Gtk.Label(label='Navigation')
        nav_title.set_halign(Gtk.Align.START)
        nav_title.set_xalign(0.0)
        nav_title.get_style_context().add_class('section-title')
        sidebar.pack_start(nav_title, False, False, 0)

        items = [
            ('dashboard', 'Dashboard'),
            ('actions', 'Actions'),
            ('cleanup', 'Cleanup'),
            ('install', 'Install'),
            ('network', 'Network'),
            ('downloads', 'Downloads'),
            ('settings', 'Settings'),
        ]

        for page_id, label in items:
            button = Gtk.Button(label=label)
            button.get_style_context().add_class('nav-button')
            button.set_halign(Gtk.Align.FILL)
            button.set_hexpand(True)
            button.connect('clicked', self.on_nav_clicked, page_id)
            self._page_buttons[page_id] = button
            sidebar.pack_start(button, False, False, 0)

        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        sidebar.pack_start(spacer, True, True, 0)

        help_label = Gtk.Label(label='No ~/.bashrc or ~/.zshrc changes required.')
        help_label.set_line_wrap(True)
        help_label.set_halign(Gtk.Align.START)
        help_label.set_xalign(0.0)
        help_label.get_style_context().add_class('status-text')
        sidebar.pack_start(help_label, False, False, 0)
        return sidebar

    def _build_footer(self):
        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        footer.get_style_context().add_class('status-bar')
        footer.pack_start(self.status_label, False, False, 0)
        return footer

    def _build_pages(self):
        self.stack.add_named(self._build_dashboard_page(), 'dashboard')
        self.stack.add_named(self._build_actions_page(), 'actions')
        self.stack.add_named(self._build_cleanup_page(), 'cleanup')
        self.stack.add_named(self._build_install_page(), 'install')
        self.stack.add_named(self._build_network_page(), 'network')
        self.stack.add_named(self._build_downloads_page(), 'downloads')
        self.stack.add_named(self._build_settings_page(), 'settings')

    def _page_shell(self, title, description):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        page.get_style_context().add_class('content')
        page.set_margin_left(18)
        page.set_margin_right(18)
        page.set_margin_top(18)
        page.set_margin_bottom(18)

        title_label = Gtk.Label()
        title_label.set_markup(
            f'<span size="xx-large" weight="bold">{GLib.markup_escape_text(title)}</span>'
        )
        title_label.set_halign(Gtk.Align.START)
        title_label.set_xalign(0.0)

        desc_label = Gtk.Label(label=description)
        desc_label.get_style_context().add_class('page-desc')
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_xalign(0.0)
        desc_label.set_line_wrap(True)

        page.pack_start(title_label, False, False, 0)
        page.pack_start(desc_label, False, False, 0)
        return page

    def _card(self, title, value=None, subtitle=None):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        card.get_style_context().add_class('card')

        title_label = Gtk.Label(label=title)
        title_label.set_halign(Gtk.Align.START)
        title_label.set_xalign(0.0)
        title_label.get_style_context().add_class('card-title')
        card.pack_start(title_label, False, False, 0)

        if value is not None:
            value_label = Gtk.Label(label=value)
            value_label.set_halign(Gtk.Align.START)
            value_label.set_xalign(0.0)
            value_label.get_style_context().add_class('metric-value')
            card.pack_start(value_label, False, False, 0)

        if subtitle is not None:
            subtitle_label = Gtk.Label(label=subtitle)
            subtitle_label.set_halign(Gtk.Align.START)
            subtitle_label.set_xalign(0.0)
            subtitle_label.set_line_wrap(True)
            subtitle_label.get_style_context().add_class('metric-label')
            card.pack_start(subtitle_label, False, False, 0)

        return card

    def _action_button(self, label, callback, style='secondary-button'):
        button = Gtk.Button(label=label)
        button.get_style_context().add_class(style)
        button.set_halign(Gtk.Align.FILL)
        button.set_hexpand(True)
        button.connect('clicked', callback)
        return button

    def _privileged_command(self, command):
        if shutil.which('pkexec'):
            return ['pkexec'] + command
        if shutil.which('sudo'):
            return ['sudo', '-n'] + command
        return command

    def _select_folder(self, title, initial_path):
        dialog = Gtk.FileChooserDialog(
            title=title,
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            ),
        )
        if initial_path and os.path.isdir(initial_path):
            dialog.set_current_folder(initial_path)

        chosen = None
        if dialog.run() == Gtk.ResponseType.OK:
            chosen = dialog.get_filename()
        dialog.destroy()
        return chosen

    def _build_dashboard_page(self):
        page = self._page_shell('Dashboard', 'Overview of the system and quick access to the most common actions.')

        grid = Gtk.Grid(column_spacing=12, row_spacing=12)
        grid.set_hexpand(True)

        self.cpu_card = self._card('Host', 'Loading...', 'System identity and session info')
        self.mem_card = self._card('Memory', 'Loading...', 'Current RAM usage')
        self.disk_card = self._card('Disk', 'Loading...', 'Filesystem usage on /')
        self.shell_card = self._card('Shell', 'Interactive ready', 'Alou loads automatically in interactive shells')

        grid.attach(self.cpu_card, 0, 0, 1, 1)
        grid.attach(self.mem_card, 1, 0, 1, 1)
        grid.attach(self.disk_card, 0, 1, 1, 1)
        grid.attach(self.shell_card, 1, 1, 1, 1)

        page.pack_start(grid, False, False, 0)

        actions_title = Gtk.Label(label='Quick actions')
        actions_title.get_style_context().add_class('section-title')
        actions_title.set_halign(Gtk.Align.START)
        actions_title.set_xalign(0.0)
        page.pack_start(actions_title, False, False, 8)

        quick_actions = Gtk.FlowBox()
        quick_actions.set_selection_mode(Gtk.SelectionMode.NONE)
        quick_actions.set_max_children_per_line(3)
        quick_actions.set_row_spacing(8)
        quick_actions.set_column_spacing(8)

        for label, callback, style in [
            ('Update system', self.on_update_clicked, 'primary-button'),
            ('Open dashboard', self.on_dashboard_clicked, 'secondary-button'),
            ('Open cleanup', self.on_cleanup_clicked, 'secondary-button'),
            ('Launch GUI test log', self.on_ping_clicked, 'secondary-button'),
        ]:
            child = Gtk.FlowBoxChild()
            child.add(self._action_button(label, callback, style))
            quick_actions.add(child)

        page.pack_start(quick_actions, False, False, 0)

        log_title = Gtk.Label(label='Live logs')
        log_title.get_style_context().add_class('section-title')
        log_title.set_halign(Gtk.Align.START)
        log_title.set_xalign(0.0)
        page.pack_start(log_title, False, False, 8)

        self.logview = Gtk.TextView()
        self.logview.set_editable(False)
        self.logview.set_cursor_visible(False)
        self.logview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.logview.set_monospace(True)
        self.logview.get_buffer().set_text('Alou GUI ready.\n')

        log_scroll = Gtk.ScrolledWindow()
        log_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        log_scroll.set_vexpand(True)
        log_scroll.add(self.logview)
        page.pack_start(log_scroll, True, True, 0)

        return page

    def _build_actions_page(self):
        page = self._page_shell('Actions', 'Centralized shell actions with visible feedback and no UI freeze.')

        grid = Gtk.Grid(column_spacing=12, row_spacing=12)
        grid.set_hexpand(True)
        grid.attach(self._card('System update', 'apt update + upgrade', 'Runs the system refresh workflow'), 0, 0, 1, 1)
        grid.attach(self._card('Git helpers', 'gitp / gita', 'Quick commit helpers from the shell'), 1, 0, 1, 1)
        grid.attach(self._card('Dashboard', 'Terminal overview', 'Shows RAM, disk, user and host information'), 0, 1, 1, 1)
        grid.attach(self._card('Command tools', 'yt / ext', 'Media and archive shortcuts'), 1, 1, 1, 1)
        page.pack_start(grid, False, False, 0)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.pack_start(self._action_button('Update system', self.on_update_clicked, 'primary-button'), True, True, 0)
        row.pack_start(self._action_button('Open terminal dashboard', self.on_dashboard_clicked), True, True, 0)
        row.pack_start(self._action_button('Send test log', self.on_ping_clicked), True, True, 0)
        page.pack_start(row, False, False, 0)

        return page

    def _build_cleanup_page(self):
        page = self._page_shell('Cleanup', 'Remove local build artifacts from the current project directory.')

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card.get_style_context().add_class('card')

        combo = Gtk.ComboBoxText()
        combo.append_text('node_modules')
        combo.append_text('__pycache__')
        combo.append_text('.venv')
        combo.append_text('vendor')
        combo.append_text('all')
        combo.set_active(0)
        self.cleanup_combo = combo

        self.cleanup_path_entry = Gtk.Entry()
        self.cleanup_path_entry.set_text(os.getcwd())

        card.pack_start(Gtk.Label(label='Target folder'), False, False, 0)
        card.pack_start(self.cleanup_path_entry, False, False, 0)
        card.pack_start(Gtk.Label(label='Cleanup mode'), False, False, 0)
        card.pack_start(combo, False, False, 0)

        button_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        button_row.pack_start(self._action_button('Run cleanup', self.on_cleanup_clicked, 'danger-button'), False, False, 0)
        button_row.pack_start(self._action_button('Open dashboard', self.on_dashboard_clicked), False, False, 0)
        card.pack_start(button_row, False, False, 0)

        page.pack_start(card, False, False, 0)
        return page

    def _build_install_page(self):
        page = self._page_shell('Install', 'Install missing tools or packages directly from the GUI.')

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card.get_style_context().add_class('card')

        self.install_entry = Gtk.Entry()
        self.install_entry.set_placeholder_text('Package name, for example: yt-dlp')

        card.pack_start(Gtk.Label(label='Package to install'), False, False, 0)
        card.pack_start(self.install_entry, False, False, 0)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.pack_start(self._action_button('Install package', self.on_install_clicked, 'primary-button'), False, False, 0)
        row.pack_start(self._action_button('Refresh system', self.on_update_clicked), False, False, 0)
        card.pack_start(row, False, False, 0)

        page.pack_start(card, False, False, 0)
        return page

    def _build_network_page(self):
        page = self._page_shell('Network', 'Quick visibility on local network and port checks.')

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card.get_style_context().add_class('card')

        self.network_target_entry = Gtk.Entry()
        self.network_target_entry.set_placeholder_text('Target host or IP, leave empty for local network scan')

        card.pack_start(Gtk.Label(label='Target'), False, False, 0)
        card.pack_start(self.network_target_entry, False, False, 0)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.pack_start(self._action_button('Ping target', self.on_network_ping_clicked, 'primary-button'), False, False, 0)
        row.pack_start(self._action_button('Scan local network', self.on_network_scan_clicked), False, False, 0)
        card.pack_start(row, False, False, 0)

        page.pack_start(card, False, False, 0)
        return page

    def _build_downloads_page(self):
        page = self._page_shell('Downloads', 'Paste a YouTube video or playlist link and download it without leaving the GUI.')

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card.get_style_context().add_class('card')

        self.download_url_entry = Gtk.Entry()
        self.download_url_entry.set_placeholder_text('Paste a YouTube video or playlist URL here')

        self.download_mode_combo = Gtk.ComboBoxText()
        self.download_mode_combo.append_text('Auto detect')
        self.download_mode_combo.append_text('Video only')
        self.download_mode_combo.append_text('Playlist only')
        self.download_mode_combo.set_active(0)

        self.download_dir_entry = Gtk.Entry()
        self.download_dir_entry.set_text(os.path.join(os.path.expanduser('~'), 'Downloads', 'Alou'))

        card.pack_start(Gtk.Label(label='YouTube URL'), False, False, 0)
        card.pack_start(self.download_url_entry, False, False, 0)

        url_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        url_row.pack_start(self._action_button('Paste from clipboard', self.on_youtube_paste_clicked), False, False, 0)
        url_row.pack_start(self._action_button('Clear URL', self.on_youtube_clear_clicked), False, False, 0)
        card.pack_start(url_row, False, False, 0)

        card.pack_start(Gtk.Label(label='Download mode'), False, False, 0)
        card.pack_start(self.download_mode_combo, False, False, 0)

        card.pack_start(Gtk.Label(label='Output directory'), False, False, 0)
        card.pack_start(self.download_dir_entry, False, False, 0)

        dir_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        dir_row.pack_start(self._action_button('Choose folder', self.on_youtube_browse_clicked), False, False, 0)
        dir_row.pack_start(self._action_button('Open dashboard', self.on_dashboard_clicked), False, False, 0)
        card.pack_start(dir_row, False, False, 0)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.pack_start(self._action_button('Download video/playlist', self.on_download_clicked, 'primary-button'), False, False, 0)
        row.pack_start(self._action_button('Refresh system info', self.on_refresh_clicked), False, False, 0)
        card.pack_start(row, False, False, 0)

        hint = Gtk.Label(label='Tip: if the URL is a playlist, Alou can download the full playlist or only the single video.')
        hint.set_line_wrap(True)
        hint.set_halign(Gtk.Align.START)
        hint.set_xalign(0.0)
        hint.get_style_context().add_class('metric-label')
        card.pack_start(hint, False, False, 0)

        page.pack_start(card, False, False, 0)
        return page

    def _build_settings_page(self):
        page = self._page_shell('Settings', 'Basic runtime preferences for the GUI.')

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card.get_style_context().add_class('card')

        self.autoscroll_check = Gtk.CheckButton(label='Auto-scroll logs')
        self.autoscroll_check.set_active(True)

        self.show_timestamp_check = Gtk.CheckButton(label='Prefix logs with time')
        self.show_timestamp_check.set_active(True)

        self.dark_mode_label = Gtk.Label(label='Theme')
        self.dark_mode_label.set_halign(Gtk.Align.START)
        self.dark_mode_label.set_xalign(0.0)

        card.pack_start(self.autoscroll_check, False, False, 0)
        card.pack_start(self.show_timestamp_check, False, False, 0)
        card.pack_start(self.dark_mode_label, False, False, 0)
        card.pack_start(Gtk.Label(label='Dark theme is applied by default.'), False, False, 0)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.pack_start(self._action_button('Refresh system info', self.on_refresh_clicked, 'primary-button'), False, False, 0)
        row.pack_start(self._action_button('Clear logs', self.on_clear_logs_clicked), False, False, 0)
        card.pack_start(row, False, False, 0)

        page.pack_start(card, False, False, 0)
        return page

    def _set_page(self, page_id):
        self.stack.set_visible_child_name(page_id)
        for current_id, button in self._page_buttons.items():
            style = button.get_style_context()
            if current_id == page_id:
                style.add_class('active')
            else:
                style.remove_class('active')

    def _set_status(self, text):
        self.status_label.set_text(text)

    def _append_log(self, text):
        buf = self.logview.get_buffer()
        end = buf.get_end_iter()
        if self.show_timestamp_check.get_active():
            stamp = GLib.DateTime.new_now_local().format('%H:%M:%S')
            text = f'[{stamp}] {text}'
        buf.insert(end, text + '\n')
        if self.autoscroll_check.get_active():
            mark = buf.create_mark(None, buf.get_end_iter(), False)
            self.logview.scroll_mark_onscreen(mark)

    def _run_command(self, command, description, cwd=None):
        def worker():
            process = None
            try:
                GLib.idle_add(self._set_status, f'Running: {description}')
                GLib.idle_add(self._append_log, f'Start: {description}')
                process = subprocess.Popen(
                    command,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                self._running_processes.add(process)
                for line in process.stdout:
                    GLib.idle_add(self._append_log, line.rstrip())
                returncode = process.wait()
                GLib.idle_add(self._append_log, f'Finished: {description} (code {returncode})')
                GLib.idle_add(self._set_status, f'Ready - {description} finished')
            except Exception as exc:
                GLib.idle_add(self._append_log, f'Error: {exc}')
                GLib.idle_add(self._set_status, 'Ready')
            finally:
                if process is not None:
                    self._running_processes.discard(process)

        threading.Thread(target=worker, daemon=True).start()

    def _refresh_system_info(self):
        user = os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'
        host = socket.gethostname()

        try:
            free_output = subprocess.check_output(['free', '-m'], text=True)
            mem_line = free_output.splitlines()[1].split()
            used_mem = mem_line[2]
            total_mem = mem_line[1]
            mem_value = f'{used_mem}MB / {total_mem}MB'
        except Exception:
            mem_value = 'Unavailable'

        try:
            df_output = subprocess.check_output(['df', '-h', '/'], text=True)
            disk_line = df_output.splitlines()[1].split()
            disk_value = f'{disk_line[4]} used, {disk_line[3]} free'
        except Exception:
            disk_value = 'Unavailable'

        self._set_card(self.cpu_card, 'Host', host, f'User: {user}')
        self._set_card(self.mem_card, 'Memory', mem_value, 'RAM usage on the system')
        self._set_card(self.disk_card, 'Disk', disk_value, 'Filesystem usage on /')
        self._set_card(self.shell_card, 'Shell', 'Interactive ready', 'bash and zsh interactive sessions are supported')
        self._set_status('System information refreshed')

    def _set_card(self, card, title, value, subtitle):
        children = card.get_children()
        if len(children) >= 1:
            children[0].set_text(title)
        if len(children) >= 2:
            children[1].set_text(value)
        if len(children) >= 3:
            children[2].set_text(subtitle)

    def on_nav_clicked(self, widget, page_id):
        self._set_page(page_id)
        self._set_status(f'Opened {widget.get_label()}')

    def on_update_clicked(self, widget):
        self._run_command(self._privileged_command(['/usr/bin/apt-get', 'update']), 'system update')

    def on_cleanup_clicked(self, widget):
        target = self.cleanup_path_entry.get_text().strip() if hasattr(self, 'cleanup_path_entry') else os.getcwd()
        mode = self.cleanup_combo.get_active_text() if hasattr(self, 'cleanup_combo') else 'node_modules'
        if not target:
            target = os.getcwd()

        if mode == 'all':
            script = 'find . \\( -type d -name node_modules -o -name vendor -o -name __pycache__ -o -name .venv -o -name target \\) -prune -exec rm -rf "{}" +'
        elif mode == 'node_modules':
            script = 'find . -type d -name node_modules -prune -exec rm -rf "{}" +'
        elif mode == '__pycache__':
            script = 'find . -type d -name __pycache__ -exec rm -rf "{}" +'
        elif mode == '.venv':
            script = 'find . -type d -name .venv -prune -exec rm -rf "{}" +'
        else:
            script = 'find . -type d -name vendor -prune -exec rm -rf "{}" +'

        self._run_command(['/bin/sh', '-lc', script], f'cleanup {mode}', cwd=target)

    def on_install_clicked(self, widget):
        package = self.install_entry.get_text().strip()
        if not package:
            self._append_log('No package selected')
            self._set_status('Package name required')
            return
        self._run_command(self._privileged_command(['/usr/bin/apt-get', 'install', '-y', package]), f'install {package}')

    def on_network_ping_clicked(self, widget):
        target = self.network_target_entry.get_text().strip()
        if not target:
            self._append_log('No network target provided')
            self._set_status('Target required')
            return
        self._run_command(['/bin/ping', '-c', '4', target], f'ping {target}')

    def on_network_scan_clicked(self, widget):
        target = self.network_target_entry.get_text().strip()
        if target:
            command = ['/usr/bin/nmap', '-sn', target]
            description = f'network scan {target}'
        else:
            command = ['/bin/sh', '-lc', "hostname -I | awk '{print $1}' | xargs -r -I {} nmap -sn {}/24"]
            description = 'local network scan'
        self._run_command(command, description)

    def on_download_clicked(self, widget):
        url = self.download_url_entry.get_text().strip()
        if not url:
            self._append_log('No URL provided')
            self._set_status('URL required')
            return

        output_dir = self.download_dir_entry.get_text().strip() if hasattr(self, 'download_dir_entry') else ''
        if not output_dir:
            output_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'Alou')

        mode = self.download_mode_combo.get_active_text() if hasattr(self, 'download_mode_combo') else 'Auto detect'
        command = ['yt-dlp', '--no-mtime', '-P', output_dir, '-o', '%(uploader)s/%(title)s.%(ext)s']

        if mode == 'Video only':
            command.append('--no-playlist')
        elif mode == 'Playlist only':
            command.append('--yes-playlist')

        command.append(url)
        self._run_command(command, f'youtube download ({mode.lower()})')

    def on_youtube_paste_clicked(self, widget):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = clipboard.wait_for_text()
        if not text:
            self._append_log('Clipboard is empty')
            self._set_status('No URL in clipboard')
            return

        cleaned = text.strip()
        self.download_url_entry.set_text(cleaned)
        self._append_log('URL pasted from clipboard')
        self._set_status('URL pasted')

    def on_youtube_clear_clicked(self, widget):
        self.download_url_entry.set_text('')
        self._set_status('YouTube URL cleared')

    def on_youtube_browse_clicked(self, widget):
        current_dir = self.download_dir_entry.get_text().strip() if hasattr(self, 'download_dir_entry') else ''
        chosen = self._select_folder('Choose a download folder', current_dir)
        if chosen:
            self.download_dir_entry.set_text(chosen)
            self._append_log(f'Download folder set to: {chosen}')
            self._set_status('Download folder updated')

    def on_dashboard_clicked(self, widget):
        self._set_page('dashboard')
        self._refresh_system_info()
        self._append_log('Dashboard refreshed')

    def on_refresh_clicked(self, widget):
        self._refresh_system_info()
        self._append_log('System information refreshed')

    def on_clear_logs_clicked(self, widget):
        self.logview.get_buffer().set_text('')
        self._set_status('Logs cleared')

    def on_ping_clicked(self, widget):
        self._append_log('GUI is responsive and ready')
        self._set_status('Test log written')


def main():
    win = AlouWindow()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
