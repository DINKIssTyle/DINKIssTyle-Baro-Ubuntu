#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by DINKIssTyle on 2026.
Copyright (C) 2026 DINKI'ssTyle. All rights reserved.

Internationalization (i18n) module for Baro
"""

# 지원 언어 목록
LANGUAGES = {
    "en": "English",
    "ko": "한국어",
    "zh": "中文",
    "ja": "日本語",
    "es": "Español"
}

# 번역 데이터
TRANSLATIONS = {
    # 영어 (기본)
    "en": {
        # 메뉴
        "menu_open_in_terminal": "Open in Terminal",
        "menu_settings": "Settings...",
        "menu_refresh": "Refresh",
        "menu_quit": "Quit",
        "menu_no_paths": "(No paths configured)",
        
        # 설정 창
        "settings_title": "Baro Settings",
        "settings_language": "Language:",
        "settings_sort": "Sort:",
        "settings_sort_custom": "Custom Order",
        "settings_sort_name": "By Name",
        "settings_paths": "Path List",
        "settings_terminal": "Terminal:",
        "settings_add": "Add",
        "settings_edit": "Edit",
        "settings_delete": "Delete",
        "settings_move_up": "▲ Up",
        "settings_move_down": "▼ Down",
        "settings_cancel": "Cancel",
        "settings_save": "Save",
        
        # 경로 편집 다이얼로그
        "path_add_title": "Add Path",
        "path_edit_title": "Edit Path",
        "path_alias": "Alias:",
        "path_location": "Path:",
        "path_browse": "Browse...",
        "path_select_folder": "Select Folder",
        
        # 메시지
        "msg_select_item_edit": "Please select an item to edit.",
        "msg_select_item_delete": "Please select an item to delete.",
        "msg_confirm_delete": "Delete '{}'?",
        "msg_folder_not_found": "Path does not exist: {}",
        "msg_cannot_open_folder": "Cannot open folder: {}",
        "msg_cannot_open_terminal": "Cannot open terminal: {}",
    },
    
    # 한국어
    "ko": {
        # 메뉴
        "menu_open_in_terminal": "터미널에서 열기",
        "menu_settings": "설정...",
        "menu_refresh": "새로고침",
        "menu_quit": "종료",
        "menu_no_paths": "(경로가 없습니다)",
        
        # 설정 창
        "settings_title": "Baro 설정",
        "settings_language": "언어:",
        "settings_sort": "정렬:",
        "settings_sort_custom": "사용자 정렬순",
        "settings_sort_name": "이름순",
        "settings_paths": "경로 목록",
        "settings_terminal": "터미널:",
        "settings_add": "추가",
        "settings_edit": "수정",
        "settings_delete": "삭제",
        "settings_move_up": "▲ 위로",
        "settings_move_down": "▼ 아래로",
        "settings_cancel": "취소",
        "settings_save": "저장",
        
        # 경로 편집 다이얼로그
        "path_add_title": "경로 추가",
        "path_edit_title": "경로 수정",
        "path_alias": "별칭:",
        "path_location": "경로:",
        "path_browse": "찾아보기...",
        "path_select_folder": "폴더 선택",
        
        # 메시지
        "msg_select_item_edit": "수정할 항목을 선택하세요.",
        "msg_select_item_delete": "삭제할 항목을 선택하세요.",
        "msg_confirm_delete": "'{}' 항목을 삭제하시겠습니까?",
        "msg_folder_not_found": "경로가 존재하지 않습니다: {}",
        "msg_cannot_open_folder": "폴더를 열 수 없습니다: {}",
        "msg_cannot_open_terminal": "터미널을 열 수 없습니다: {}",
    },
    
    # 중국어
    "zh": {
        # 메뉴
        "menu_open_in_terminal": "在终端中打开",
        "menu_settings": "设置...",
        "menu_refresh": "刷新",
        "menu_quit": "退出",
        "menu_no_paths": "(没有配置路径)",
        
        # 设置窗口
        "settings_title": "Baro 设置",
        "settings_language": "语言:",
        "settings_sort": "排序:",
        "settings_sort_custom": "自定义顺序",
        "settings_sort_name": "按名称",
        "settings_paths": "路径列表",
        "settings_terminal": "终端:",
        "settings_add": "添加",
        "settings_edit": "编辑",
        "settings_delete": "删除",
        "settings_move_up": "▲ 上移",
        "settings_move_down": "▼ 下移",
        "settings_cancel": "取消",
        "settings_save": "保存",
        
        # 路径编辑对话框
        "path_add_title": "添加路径",
        "path_edit_title": "编辑路径",
        "path_alias": "别名:",
        "path_location": "路径:",
        "path_browse": "浏览...",
        "path_select_folder": "选择文件夹",
        
        # 消息
        "msg_select_item_edit": "请选择要编辑的项目。",
        "msg_select_item_delete": "请选择要删除的项目。",
        "msg_confirm_delete": "删除 '{}'？",
        "msg_folder_not_found": "路径不存在: {}",
        "msg_cannot_open_folder": "无法打开文件夹: {}",
        "msg_cannot_open_terminal": "无法打开终端: {}",
    },
    
    # 일본어
    "ja": {
        # メニュー
        "menu_open_in_terminal": "ターミナルで開く",
        "menu_settings": "設定...",
        "menu_refresh": "更新",
        "menu_quit": "終了",
        "menu_no_paths": "(パスが設定されていません)",
        
        # 設定ウィンドウ
        "settings_title": "Baro 設定",
        "settings_language": "言語:",
        "settings_sort": "並び替え:",
        "settings_sort_custom": "カスタム順",
        "settings_sort_name": "名前順",
        "settings_paths": "パスリスト",
        "settings_terminal": "ターミナル:",
        "settings_add": "追加",
        "settings_edit": "編集",
        "settings_delete": "削除",
        "settings_move_up": "▲ 上へ",
        "settings_move_down": "▼ 下へ",
        "settings_cancel": "キャンセル",
        "settings_save": "保存",
        
        # パス編集ダイアログ
        "path_add_title": "パスを追加",
        "path_edit_title": "パスを編集",
        "path_alias": "エイリアス:",
        "path_location": "パス:",
        "path_browse": "参照...",
        "path_select_folder": "フォルダを選択",
        
        # メッセージ
        "msg_select_item_edit": "編集する項目を選択してください。",
        "msg_select_item_delete": "削除する項目を選択してください。",
        "msg_confirm_delete": "'{}' を削除しますか？",
        "msg_folder_not_found": "パスが存在しません: {}",
        "msg_cannot_open_folder": "フォルダを開けません: {}",
        "msg_cannot_open_terminal": "ターミナルを開けません: {}",
    },
    
    # 스페인어
    "es": {
        # Menú
        "menu_open_in_terminal": "Abrir en Terminal",
        "menu_settings": "Configuración...",
        "menu_refresh": "Actualizar",
        "menu_quit": "Salir",
        "menu_no_paths": "(No hay rutas configuradas)",
        
        # Ventana de configuración
        "settings_title": "Configuración de Baro",
        "settings_language": "Idioma:",
        "settings_sort": "Ordenar:",
        "settings_sort_custom": "Orden personalizado",
        "settings_sort_name": "Por nombre",
        "settings_paths": "Lista de rutas",
        "settings_terminal": "Terminal:",
        "settings_add": "Añadir",
        "settings_edit": "Editar",
        "settings_delete": "Eliminar",
        "settings_move_up": "▲ Subir",
        "settings_move_down": "▼ Bajar",
        "settings_cancel": "Cancelar",
        "settings_save": "Guardar",
        
        # Diálogo de edición de ruta
        "path_add_title": "Añadir Ruta",
        "path_edit_title": "Editar Ruta",
        "path_alias": "Alias:",
        "path_location": "Ruta:",
        "path_browse": "Explorar...",
        "path_select_folder": "Seleccionar Carpeta",
        
        # Mensajes
        "msg_select_item_edit": "Seleccione un elemento para editar.",
        "msg_select_item_delete": "Seleccione un elemento para eliminar.",
        "msg_confirm_delete": "¿Eliminar '{}'?",
        "msg_folder_not_found": "La ruta no existe: {}",
        "msg_cannot_open_folder": "No se puede abrir la carpeta: {}",
        "msg_cannot_open_terminal": "No se puede abrir el terminal: {}",
    },
}


class I18n:
    """국제화(i18n) 관리 클래스"""
    
    def __init__(self, language: str = "en"):
        self._language = language if language in LANGUAGES else "en"
    
    @property
    def language(self) -> str:
        return self._language
    
    @language.setter
    def language(self, value: str):
        if value in LANGUAGES:
            self._language = value
    
    def t(self, key: str, *args) -> str:
        """번역된 문자열 반환"""
        translations = TRANSLATIONS.get(self._language, TRANSLATIONS["en"])
        text = translations.get(key, TRANSLATIONS["en"].get(key, key))
        
        if args:
            return text.format(*args)
        return text
    
    def get_languages(self) -> dict:
        """지원 언어 목록 반환"""
        return LANGUAGES.copy()


# 전역 인스턴스
_i18n = I18n()


def set_language(language: str):
    """전역 언어 설정"""
    _i18n.language = language


def get_language() -> str:
    """현재 언어 반환"""
    return _i18n.language


def t(key: str, *args) -> str:
    """번역된 문자열 반환 (편의 함수)"""
    return _i18n.t(key, *args)


def get_languages() -> dict:
    """지원 언어 목록 반환"""
    return LANGUAGES.copy()
