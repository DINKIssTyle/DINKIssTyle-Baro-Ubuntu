#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by DINKIssTyle on 2026.
Copyright (C) 2026 DINKI'ssTyle. All rights reserved.

Settings Dialog for Baro Path Quick Access Indicator
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

from settings_manager import SettingsManager
from i18n import t, set_language, get_language, get_languages


class PathEditDialog(Gtk.Dialog):
    """경로 추가/수정 다이얼로그"""
    
    def __init__(self, parent, is_edit=False, alias="", path=""):
        title = t("path_edit_title") if is_edit else t("path_add_title")
        super().__init__(title=title, transient_for=parent, modal=True)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        self.set_default_size(450, -1)
        
        content = self.get_content_area()
        content.set_spacing(10)
        content.set_margin_start(15)
        content.set_margin_end(15)
        content.set_margin_top(15)
        content.set_margin_bottom(15)
        
        # 별칭 입력
        alias_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        alias_label = Gtk.Label(label=t("path_alias"))
        alias_label.set_xalign(0)
        alias_label.set_width_chars(8)
        self.alias_entry = Gtk.Entry()
        self.alias_entry.set_text(alias)
        self.alias_entry.set_hexpand(True)
        alias_box.pack_start(alias_label, False, False, 0)
        alias_box.pack_start(self.alias_entry, True, True, 0)
        content.pack_start(alias_box, False, False, 0)
        
        # 경로 입력
        path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        path_label = Gtk.Label(label=t("path_location"))
        path_label.set_xalign(0)
        path_label.set_width_chars(8)
        self.path_entry = Gtk.Entry()
        self.path_entry.set_text(path)
        self.path_entry.set_hexpand(True)
        browse_btn = Gtk.Button(label=t("path_browse"))
        browse_btn.connect("clicked", self.on_browse)
        path_box.pack_start(path_label, False, False, 0)
        path_box.pack_start(self.path_entry, True, True, 0)
        path_box.pack_start(browse_btn, False, False, 0)
        content.pack_start(path_box, False, False, 0)
        
        self.show_all()
    
    def on_browse(self, button):
        """폴더 선택 다이얼로그"""
        dialog = Gtk.FileChooserDialog(
            title=t("path_select_folder"),
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK
            )
        )
        
        current_path = self.path_entry.get_text()
        if current_path:
            dialog.set_current_folder(current_path)
        
        if dialog.run() == Gtk.ResponseType.OK:
            self.path_entry.set_text(dialog.get_filename())
        dialog.destroy()
    
    def get_values(self):
        """입력값 반환"""
        return self.alias_entry.get_text().strip(), self.path_entry.get_text().strip()


class SettingsDialog(Gtk.Window):
    """Baro 설정 창"""
    
    def __init__(self, settings_manager: SettingsManager, on_save_callback=None):
        super().__init__(title=t("settings_title"))
        
        self.settings = settings_manager
        self.on_save_callback = on_save_callback
        
        # 현재 언어 적용
        set_language(self.settings.language)
        
        self.set_default_size(600, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(15)
        
        # 메인 박스
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(main_box)
        
        # 상단: 언어 및 정렬 옵션
        options_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        
        # 언어 선택
        lang_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lang_label = Gtk.Label(label=t("settings_language"))
        self.lang_combo = Gtk.ComboBoxText()
        for code, name in get_languages().items():
            self.lang_combo.append(code, name)
        self.lang_combo.set_active_id(self.settings.language)
        self.lang_combo.connect("changed", self.on_language_changed)
        lang_box.pack_start(lang_label, False, False, 0)
        lang_box.pack_start(self.lang_combo, False, False, 0)
        options_box.pack_start(lang_box, False, False, 0)
        
        # 정렬 선택
        sort_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        sort_label = Gtk.Label(label=t("settings_sort"))
        self.sort_combo = Gtk.ComboBoxText()
        self.sort_combo.append("custom", t("settings_sort_custom"))
        self.sort_combo.append("name", t("settings_sort_name"))
        self.sort_combo.set_active_id(self.settings.sort_mode)
        sort_box.pack_start(sort_label, False, False, 0)
        sort_box.pack_start(self.sort_combo, False, False, 0)
        options_box.pack_start(sort_box, False, False, 0)
        
        main_box.pack_start(options_box, False, False, 0)
        
        # 중간: 경로 목록
        list_frame = Gtk.Frame(label=t("settings_paths"))
        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        list_box.set_margin_start(10)
        list_box.set_margin_end(10)
        list_box.set_margin_top(10)
        list_box.set_margin_bottom(10)
        list_frame.add(list_box)
        
        # TreeView
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(250)
        
        # ListStore: alias, path, order
        self.store = Gtk.ListStore(str, str, int)
        self._load_paths()
        
        self.treeview = Gtk.TreeView(model=self.store)
        self.treeview.set_reorderable(True)
        
        # 열 설정
        renderer = Gtk.CellRendererText()
        col_alias = Gtk.TreeViewColumn(t("path_alias").replace(":", ""), renderer, text=0)
        col_alias.set_resizable(True)
        col_alias.set_min_width(120)
        self.treeview.append_column(col_alias)
        
        renderer = Gtk.CellRendererText()
        col_path = Gtk.TreeViewColumn(t("path_location").replace(":", ""), renderer, text=1)
        col_path.set_resizable(True)
        col_path.set_expand(True)
        self.treeview.append_column(col_path)
        
        scroll.add(self.treeview)
        list_box.pack_start(scroll, True, True, 0)
        
        # 버튼들
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        
        add_btn = Gtk.Button(label=t("settings_add"))
        add_btn.connect("clicked", self.on_add)
        edit_btn = Gtk.Button(label=t("settings_edit"))
        edit_btn.connect("clicked", self.on_edit)
        del_btn = Gtk.Button(label=t("settings_delete"))
        del_btn.connect("clicked", self.on_delete)
        
        btn_box.pack_start(add_btn, False, False, 0)
        btn_box.pack_start(edit_btn, False, False, 0)
        btn_box.pack_start(del_btn, False, False, 0)
        
        # 순서 변경 버튼
        spacer = Gtk.Label()
        btn_box.pack_start(spacer, True, True, 0)
        
        up_btn = Gtk.Button(label=t("settings_move_up"))
        up_btn.connect("clicked", self.on_move_up)
        down_btn = Gtk.Button(label=t("settings_move_down"))
        down_btn.connect("clicked", self.on_move_down)
        
        btn_box.pack_start(up_btn, False, False, 0)
        btn_box.pack_start(down_btn, False, False, 0)
        
        list_box.pack_start(btn_box, False, False, 0)
        main_box.pack_start(list_frame, True, True, 0)
        
        # 하단: 터미널 설정
        term_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        term_label = Gtk.Label(label=t("settings_terminal"))
        self.term_entry = Gtk.Entry()
        self.term_entry.set_text(self.settings.terminal)
        self.term_entry.set_hexpand(True)
        term_box.pack_start(term_label, False, False, 0)
        term_box.pack_start(self.term_entry, True, True, 0)
        main_box.pack_start(term_box, False, False, 0)
        
        # 하단: 저장/취소 버튼
        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        action_box.set_halign(Gtk.Align.END)
        
        cancel_btn = Gtk.Button(label=t("settings_cancel"))
        cancel_btn.connect("clicked", lambda b: self.destroy())
        save_btn = Gtk.Button(label=t("settings_save"))
        save_btn.get_style_context().add_class("suggested-action")
        save_btn.connect("clicked", self.on_save)
        
        action_box.pack_start(cancel_btn, False, False, 0)
        action_box.pack_start(save_btn, False, False, 0)
        main_box.pack_start(action_box, False, False, 0)
        
        self.connect("delete-event", lambda w, e: w.destroy() or True)
        self.show_all()
    
    def _load_paths(self):
        """설정에서 경로 목록 로드"""
        self.store.clear()
        for i, p in enumerate(self.settings.paths):
            self.store.append([p.get("alias", ""), p.get("path", ""), i])
    
    def _get_selected(self):
        """선택된 항목 반환"""
        selection = self.treeview.get_selection()
        model, iter_ = selection.get_selected()
        if iter_:
            return model, iter_
        return None, None
    
    def on_language_changed(self, combo):
        """언어 변경 시 UI 갱신 알림"""
        # 언어 변경은 저장 후 다시 열어야 적용됨
        pass
    
    def on_add(self, button):
        """경로 추가"""
        dialog = PathEditDialog(self, is_edit=False)
        if dialog.run() == Gtk.ResponseType.OK:
            alias, path = dialog.get_values()
            if alias and path:
                order = len(self.store)
                self.store.append([alias, path, order])
        dialog.destroy()
    
    def on_edit(self, button):
        """경로 수정"""
        model, iter_ = self._get_selected()
        if not iter_:
            self._show_message(t("msg_select_item_edit"))
            return
        
        alias = model[iter_][0]
        path = model[iter_][1]
        
        dialog = PathEditDialog(self, is_edit=True, alias=alias, path=path)
        if dialog.run() == Gtk.ResponseType.OK:
            new_alias, new_path = dialog.get_values()
            if new_alias and new_path:
                model[iter_][0] = new_alias
                model[iter_][1] = new_path
        dialog.destroy()
    
    def on_delete(self, button):
        """경로 삭제"""
        model, iter_ = self._get_selected()
        if not iter_:
            self._show_message(t("msg_select_item_delete"))
            return
        
        alias = model[iter_][0]
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=t("msg_confirm_delete", alias)
        )
        if dialog.run() == Gtk.ResponseType.YES:
            model.remove(iter_)
        dialog.destroy()
    
    def on_move_up(self, button):
        """선택 항목 위로 이동"""
        model, iter_ = self._get_selected()
        if not iter_:
            return
        
        path = model.get_path(iter_)
        if path[0] > 0:
            prev_iter = model.get_iter(path[0] - 1)
            model.swap(iter_, prev_iter)
    
    def on_move_down(self, button):
        """선택 항목 아래로 이동"""
        model, iter_ = self._get_selected()
        if not iter_:
            return
        
        next_iter = model.iter_next(iter_)
        if next_iter:
            model.swap(iter_, next_iter)
    
    def on_save(self, button):
        """설정 저장"""
        # 언어 저장
        new_lang = self.lang_combo.get_active_id()
        self.settings.language = new_lang
        set_language(new_lang)
        
        # 정렬 모드 저장
        self.settings.sort_mode = self.sort_combo.get_active_id()
        
        # 터미널 저장
        self.settings.terminal = self.term_entry.get_text().strip()
        
        # 경로 목록 저장
        paths = []
        for i, row in enumerate(self.store):
            paths.append({
                "alias": row[0],
                "path": row[1],
                "order": i
            })
        self.settings.set_paths(paths)
        self.settings.save()
        
        # 콜백 호출
        if self.on_save_callback:
            self.on_save_callback()
        
        self.destroy()
    
    def _show_message(self, message):
        """메시지 다이얼로그 표시"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()


# 테스트용 코드
if __name__ == "__main__":
    settings = SettingsManager()
    dialog = SettingsDialog(settings)
    dialog.connect("destroy", Gtk.main_quit)
    Gtk.main()
