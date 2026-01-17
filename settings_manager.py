#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by DINKIssTyle on 2026.
Copyright (C) 2026 DINKI'ssTyle. All rights reserved.

Settings Manager for Baro Path Quick Access Indicator
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional

class SettingsManager:
    """경로 별칭 및 설정을 관리하는 클래스"""
    
    CONFIG_DIR = Path.home() / ".config" / "baro"
    CONFIG_FILE = CONFIG_DIR / "settings.json"
    
    DEFAULT_SETTINGS = {
        "language": "en",  # 언어 설정
        "sort_mode": "custom",  # "custom" or "name"
        "terminal": "gnome-terminal",
        "file_manager": "xdg-open",
        "paths": []
    }
    
    def __init__(self):
        self._settings: Dict = {}
        self._ensure_config_dir()
        self.load()
    
    def _ensure_config_dir(self):
        """설정 디렉토리가 없으면 생성"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> Dict:
        """설정 파일 로드"""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self._settings = json.load(f)
                # 기본값 병합 (새 키가 추가된 경우 대비)
                for key, value in self.DEFAULT_SETTINGS.items():
                    if key not in self._settings:
                        self._settings[key] = value
            except (json.JSONDecodeError, IOError) as e:
                print(f"설정 로드 오류: {e}")
                self._settings = self.DEFAULT_SETTINGS.copy()
        else:
            self._settings = self.DEFAULT_SETTINGS.copy()
            self.save()
        return self._settings
    
    def save(self):
        """설정 파일 저장"""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"설정 저장 오류: {e}")
    
    @property
    def language(self) -> str:
        """언어 설정 반환"""
        return self._settings.get("language", "en")
    
    @language.setter
    def language(self, value: str):
        """언어 설정"""
        self._settings["language"] = value
    
    @property
    def sort_mode(self) -> str:
        """정렬 모드 반환 ('custom' 또는 'name')"""
        return self._settings.get("sort_mode", "custom")
    
    @sort_mode.setter
    def sort_mode(self, value: str):
        """정렬 모드 설정"""
        if value in ("custom", "name"):
            self._settings["sort_mode"] = value
    
    @property
    def terminal(self) -> str:
        """터미널 명령어 반환"""
        return self._settings.get("terminal", "gnome-terminal")
    
    @terminal.setter
    def terminal(self, value: str):
        """터미널 명령어 설정"""
        self._settings["terminal"] = value
    
    @property
    def file_manager(self) -> str:
        """파일 관리자 명령어 반환"""
        return self._settings.get("file_manager", "xdg-open")
    
    @file_manager.setter
    def file_manager(self, value: str):
        """파일 관리자 명령어 설정"""
        self._settings["file_manager"] = value
    
    @property
    def paths(self) -> List[Dict]:
        """경로 목록 반환"""
        return self._settings.get("paths", [])
    
    def get_sorted_paths(self) -> List[Dict]:
        """정렬된 경로 목록 반환"""
        paths = self.paths.copy()
        if self.sort_mode == "name":
            paths.sort(key=lambda x: x.get("alias", "").lower())
        else:
            paths.sort(key=lambda x: x.get("order", 0))
        return paths
    
    def add_path(self, alias: str, path: str) -> bool:
        """새 경로 추가"""
        if not alias or not path:
            return False
        
        # 중복 검사
        for p in self.paths:
            if p.get("alias") == alias:
                return False
        
        order = len(self.paths)
        self._settings["paths"].append({
            "alias": alias,
            "path": path,
            "order": order
        })
        return True
    
    def update_path(self, old_alias: str, new_alias: str, new_path: str) -> bool:
        """경로 수정"""
        for p in self._settings["paths"]:
            if p.get("alias") == old_alias:
                p["alias"] = new_alias
                p["path"] = new_path
                return True
        return False
    
    def remove_path(self, alias: str) -> bool:
        """경로 삭제"""
        for i, p in enumerate(self._settings["paths"]):
            if p.get("alias") == alias:
                del self._settings["paths"][i]
                self._reorder_paths()
                return True
        return False
    
    def move_path(self, alias: str, direction: int) -> bool:
        """경로 순서 변경 (direction: -1 = 위로, 1 = 아래로)"""
        paths = self._settings["paths"]
        for i, p in enumerate(paths):
            if p.get("alias") == alias:
                new_index = i + direction
                if 0 <= new_index < len(paths):
                    paths[i], paths[new_index] = paths[new_index], paths[i]
                    self._reorder_paths()
                    return True
                return False
        return False
    
    def _reorder_paths(self):
        """경로 순서 재정렬"""
        for i, p in enumerate(self._settings["paths"]):
            p["order"] = i
    
    def set_paths(self, paths: List[Dict]):
        """경로 목록 전체 설정"""
        self._settings["paths"] = paths
        self._reorder_paths()


# 테스트용 코드
if __name__ == "__main__":
    manager = SettingsManager()
    
    # 테스트 경로 추가
    manager.add_path("문서", str(Path.home() / "Documents"))
    manager.add_path("다운로드", str(Path.home() / "Downloads"))
    manager.add_path("홈", str(Path.home()))
    manager.save()
    
    print("저장된 경로:")
    for p in manager.get_sorted_paths():
        print(f"  {p['alias']}: {p['path']}")
