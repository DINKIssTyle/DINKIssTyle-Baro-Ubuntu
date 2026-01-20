#!/bin/bash
# Created by DINKIssTyle on 2026.
# Copyright (C) 2026 DINKI'ssTyle. All rights reserved.
#
# Baro 설치 스크립트

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="baro"
DESKTOP_FILE="$SCRIPT_DIR/baro.desktop"

echo "==================================="
echo "  Baro - 경로 빠른 접근 인디케이터"
echo "  설치 스크립트"
echo "==================================="
echo

# 의존성 확인
echo "[1/4] 의존성 확인 중..."
MISSING_DEPS=""

# Python3 확인
if ! command -v python3 &> /dev/null; then
    MISSING_DEPS="$MISSING_DEPS python3"
fi

# PyGObject 확인
if ! python3 -c "import gi" 2>/dev/null; then
    MISSING_DEPS="$MISSING_DEPS python3-gi"
fi

# AppIndicator3 확인
if ! python3 -c "import gi; gi.require_version('AppIndicator3', '0.1'); from gi.repository import AppIndicator3" 2>/dev/null; then
    MISSING_DEPS="$MISSING_DEPS gir1.2-appindicator3-0.1"
fi

# GTK3 확인
if ! python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null; then
    MISSING_DEPS="$MISSING_DEPS gir1.2-gtk-3.0"
fi

if [ -n "$MISSING_DEPS" ]; then
    echo "누락된 패키지:$MISSING_DEPS"
    echo
    read -p "누락된 패키지를 설치하시겠습니까? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt update
        sudo apt install -y $MISSING_DEPS
    else
        echo "설치가 취소되었습니다."
        exit 1
    fi
else
    echo "모든 의존성이 충족되었습니다."
fi

# 실행 권한 부여
echo
echo "[2/4] 실행 권한 설정 중..."
chmod +x "$SCRIPT_DIR/baro_indicator.py"

# .desktop 파일 경로 업데이트
echo
echo "[3/4] 데스크톱 엔트리 생성 중..."

# .desktop 파일 내용 생성 (현재 경로 반영)
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Baro
Name[ko]=바로
Comment=Path Quick Access Indicator
Comment[ko]=경로 빠른 접근 인디케이터
Exec=python3 $SCRIPT_DIR/baro_indicator.py
Icon=$SCRIPT_DIR/icons/appicon.png
Terminal=false
Type=Application
Categories=Utility;System;
Keywords=path;folder;shortcut;terminal;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF

# 애플리케이션 메뉴 등록
mkdir -p ~/.local/share/applications
cp "$DESKTOP_FILE" ~/.local/share/applications/

# 자동 시작 등록
echo
echo "[4/4] 자동 시작 등록 중..."
read -p "로그인 시 자동 시작하시겠습니까? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    mkdir -p ~/.config/autostart
    cp "$DESKTOP_FILE" ~/.config/autostart/
    echo "자동 시작이 등록되었습니다."
else
    echo "자동 시작이 등록되지 않았습니다."
fi

echo
echo "==================================="
echo "  설치가 완료되었습니다!"
echo "==================================="
echo
echo "실행 방법:"
echo "  1. 터미널: python3 $SCRIPT_DIR/baro_indicator.py"
echo "  2. 애플리케이션 메뉴에서 'Baro' 검색"
echo
