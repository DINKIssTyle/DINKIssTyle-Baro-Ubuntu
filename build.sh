#!/bin/bash
# Created by DINKIssTyle on 2026.
# Copyright (C) 2026 DINKI'ssTyle. All rights reserved.
#
# Baro 빌드 스크립트
# PyInstaller를 사용하여 단일 실행 파일로 빌드합니다.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="baro"
MAIN_SCRIPT="baro_indicator.py"
OUTPUT_DIR="$SCRIPT_DIR/dist"

echo "==================================="
echo "  Baro 빌드 스크립트"
echo "==================================="
echo

# PyInstaller 확인 및 설치
echo "[1/3] PyInstaller 확인 중..."
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller가 설치되어 있지 않습니다."
    read -p "PyInstaller를 설치하시겠습니까? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        pip3 install --user pyinstaller
    else
        echo "빌드가 취소되었습니다."
        exit 1
    fi
fi

# 의존성 확인
echo
echo "[2/3] 의존성 확인 중..."
python3 -c "
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3
print('✓ 의존성 확인 완료')
"

# 구문 검증
echo
echo "[3/3] 빌드 중..."
cd "$SCRIPT_DIR"

# PyInstaller 실행
pyinstaller \
    --onefile \
    --name="$APP_NAME" \
    --windowed \
    --hidden-import=gi \
    --hidden-import=gi.repository.Gtk \
    --hidden-import=gi.repository.AppIndicator3 \
    --hidden-import=gi.repository.GLib \
    --hidden-import=gi.repository.Gdk \
    --hidden-import=gi.repository.GdkPixbuf \
    --add-data="settings_manager.py:." \
    --add-data="settings_dialog.py:." \
    "$MAIN_SCRIPT"

# 결과 확인
if [ -f "$OUTPUT_DIR/$APP_NAME" ]; then
    echo
    echo "==================================="
    echo "  빌드 완료!"
    echo "==================================="
    echo
    echo "실행 파일: $OUTPUT_DIR/$APP_NAME"
    echo "크기: $(du -h "$OUTPUT_DIR/$APP_NAME" | cut -f1)"
    echo
    echo "실행 방법: $OUTPUT_DIR/$APP_NAME"
else
    echo
    echo "빌드 실패!"
    exit 1
fi
