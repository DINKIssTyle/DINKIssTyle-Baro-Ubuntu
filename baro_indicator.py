#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by DINKIssTyle on 2026.
Copyright (C) 2026 DINKI'ssTyle. All rights reserved.

Baro - Path Quick Access Indicator for Ubuntu
우분투 시스템 트레이에서 빠르게 경로에 접근할 수 있는 인디케이터 앱
"""

import os
import subprocess
import signal
import sys

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

from settings_manager import SettingsManager
from settings_dialog import SettingsDialog
from i18n import t, set_language


class BaroIndicator:
    """Baro 시스템 트레이 인디케이터"""
    
    APPINDICATOR_ID = "baro-path-indicator"
    
    def __init__(self):
        self.settings = SettingsManager()
        
        # 언어 설정 적용
        set_language(self.settings.language)
        
        # 아이콘 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = os.path.join(script_dir, "icons")
        app_icon = os.path.join(self.icons_dir, "appicon.png")
        
        # AppIndicator 생성
        self.indicator = AppIndicator3.Indicator.new(
            self.APPINDICATOR_ID,
            app_icon,  # 커스텀 아이콘 사용
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title("Baro")
        
        # 메뉴 생성
        self.build_menu()
    
    def build_menu(self):
        """메뉴 구성"""
        menu = Gtk.Menu()
        
        # 아이콘 파일 경로
        folder_icon_path = os.path.join(self.icons_dir, "folder.png")
        terminal_icon_path = os.path.join(self.icons_dir, "terminal.png")
        settings_icon_path = os.path.join(self.icons_dir, "settings.png")
        refresh_icon_path = os.path.join(self.icons_dir, "refresh.png")
        quit_icon_path = os.path.join(self.icons_dir, "quit.png")
        
        # 경로 목록 추가
        paths = self.settings.get_sorted_paths()
        
        if paths:
            for path_item in paths:
                alias = path_item.get("alias", "")
                path = path_item.get("path", "")
                
                # 메인 항목: 별칭 (클릭 시 파일 브라우저 열기)
                folder_item = Gtk.ImageMenuItem()
                folder_item.set_label(alias)
                folder_item.set_always_show_image(True)
                
                # 폴더 아이콘
                if os.path.exists(folder_icon_path):
                    icon = Gtk.Image.new_from_file(folder_icon_path)
                    folder_item.set_image(icon)
                
                folder_item.connect("activate", self.on_open_folder, path)
                menu.append(folder_item)
            
            # 구분선
            menu.append(Gtk.SeparatorMenuItem())
            
            # 터미널 서브메뉴
            term_menu_item = Gtk.ImageMenuItem()
            term_menu_item.set_label(t("menu_open_in_terminal"))
            term_menu_item.set_always_show_image(True)
            if os.path.exists(terminal_icon_path):
                icon = Gtk.Image.new_from_file(terminal_icon_path)
                term_menu_item.set_image(icon)
            
            term_submenu = Gtk.Menu()
            
            for path_item in paths:
                alias = path_item.get("alias", "")
                path = path_item.get("path", "")
                
                term_item = Gtk.ImageMenuItem()
                term_item.set_label(alias)
                term_item.set_always_show_image(True)
                if os.path.exists(terminal_icon_path):
                    icon = Gtk.Image.new_from_file(terminal_icon_path)
                    term_item.set_image(icon)
                term_item.connect("activate", self.on_open_terminal, path)
                term_submenu.append(term_item)
            
            term_menu_item.set_submenu(term_submenu)
            menu.append(term_menu_item)
            
            # 구분선
            menu.append(Gtk.SeparatorMenuItem())
        else:
            # 경로가 없을 때
            empty_item = Gtk.MenuItem(label=t("menu_no_paths"))
            empty_item.set_sensitive(False)
            menu.append(empty_item)
            menu.append(Gtk.SeparatorMenuItem())
        
        # 설정 메뉴
        settings_item = Gtk.ImageMenuItem()
        settings_item.set_label(t("menu_settings"))
        settings_item.set_always_show_image(True)
        if os.path.exists(settings_icon_path):
            icon = Gtk.Image.new_from_file(settings_icon_path)
            settings_item.set_image(icon)
        settings_item.connect("activate", self.on_settings)
        menu.append(settings_item)
        
        # 새로고침 메뉴
        refresh_item = Gtk.ImageMenuItem()
        refresh_item.set_label(t("menu_refresh"))
        refresh_item.set_always_show_image(True)
        if os.path.exists(refresh_icon_path):
            icon = Gtk.Image.new_from_file(refresh_icon_path)
            refresh_item.set_image(icon)
        refresh_item.connect("activate", self.on_refresh)
        menu.append(refresh_item)
        
        # 구분선
        menu.append(Gtk.SeparatorMenuItem())
        
        # 종료 메뉴
        quit_item = Gtk.ImageMenuItem()
        quit_item.set_label(t("menu_quit"))
        quit_item.set_always_show_image(True)
        if os.path.exists(quit_icon_path):
            icon = Gtk.Image.new_from_file(quit_icon_path)
            quit_item.set_image(icon)
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)
        
        menu.show_all()
        self.indicator.set_menu(menu)
    
    def on_open_folder(self, widget, path):
        """파일 브라우저로 폴더 열기"""
        # GVFS 경로 (sftp, smb 등) 또는 로컬 경로 지원
        is_gvfs = path.startswith("/run/user/") and "/gvfs/" in path
        
        if is_gvfs or os.path.exists(path):
            try:
                if is_gvfs:
                    # GVFS 경로는 파일 관리자를 직접 호출 (가장 확실한 방법)
                    file_managers = ["nautilus", "nemo", "thunar", "dolphin", "pcmanfm"]
                    opened = False
                    
                    for fm in file_managers:
                        try:
                            subprocess.Popen([fm, path])
                            opened = True
                            break
                        except FileNotFoundError:
                            continue
                    
                    if not opened:
                        # 최후의 수단: xdg-open with file:// URI
                        file_uri = "file://" + path
                        subprocess.Popen(["xdg-open", file_uri])
                else:
                    subprocess.Popen([self.settings.file_manager, path])
            except Exception as e:
                self._show_error(t("msg_cannot_open_folder", str(e)))
        else:
            self._show_error(t("msg_folder_not_found", path))
    
    def on_open_terminal(self, widget, path):
        """터미널로 폴더 열기"""
        # GVFS 경로 (sftp, smb 등) 또는 로컬 경로 지원
        is_gvfs = path.startswith("/run/user/") and "/gvfs/" in path
        
        if is_gvfs or os.path.exists(path):
            try:
                terminal = self.settings.terminal
                # 다양한 터미널 지원
                if "gnome-terminal" in terminal:
                    subprocess.Popen([terminal, "--working-directory", path])
                elif "konsole" in terminal:
                    subprocess.Popen([terminal, "--workdir", path])
                elif "xfce4-terminal" in terminal:
                    subprocess.Popen([terminal, "--working-directory", path])
                elif "tilix" in terminal:
                    subprocess.Popen([terminal, "--directory", path])
                elif "alacritty" in terminal:
                    subprocess.Popen([terminal, "--working-directory", path])
                elif "kitty" in terminal:
                    subprocess.Popen([terminal, "--directory", path])
                else:
                    # 기본: 해당 디렉토리로 이동 후 터미널 실행
                    subprocess.Popen(terminal, cwd=path, shell=True)
            except Exception as e:
                self._show_error(t("msg_cannot_open_terminal", str(e)))
        else:
            self._show_error(t("msg_folder_not_found", path))
    
    def on_settings(self, widget):
        """설정 창 열기"""
        dialog = SettingsDialog(self.settings, on_save_callback=self.build_menu)
        dialog.show_all()
    
    def on_refresh(self, widget):
        """메뉴 새로고침"""
        self.settings.load()
        self.build_menu()
    
    def on_quit(self, widget):
        """앱 종료"""
        Gtk.main_quit()
    
    def _show_error(self, message):
        """오류 다이얼로그 표시"""
        dialog = Gtk.MessageDialog(
            parent=None,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()


def main():
    # SIGINT 시그널 처리 (Ctrl+C)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # GTK 메인 루프 실행
    indicator = BaroIndicator()
    Gtk.main()


if __name__ == "__main__":
    main()
