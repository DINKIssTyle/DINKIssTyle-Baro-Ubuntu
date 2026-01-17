# Baro - 경로 빠른 접근 인디케이터

<!--
Created by DINKIssTyle on 2026.
Copyright (C) 2026 DINKI'ssTyle. All rights reserved.
-->

우분투 시스템 트레이에서 자주 사용하는 폴더에 빠르게 접근할 수 있는 인디케이터 애플리케이션입니다.

## 기능

- 📁 **시스템 트레이 상주**: 메뉴바에서 항상 접근 가능
- 🗂️ **경로 별칭 관리**: 폴더에 알기 쉬운 별칭 지정
- 📂 **파일 브라우저 열기**: 클릭 한 번으로 폴더 열기
- 🖥️ **터미널 열기**: 해당 위치에서 바로 터미널 실행
- ⚙️ **설정 창**: 경로 추가/수정/삭제 및 순서 변경
- 🔤 **정렬 옵션**: 이름순 또는 사용자 정렬순

## 스크린샷

시스템 트레이 메뉴:
```
┌─────────────────────────────────┐
│ 📁 문서              [서브메뉴] │
│ 📁 다운로드          [서브메뉴] │
│ 📁 프로젝트          [서브메뉴] │
│ ─────────────────────────────── │
│ ⚙️ 설정...                      │
│ 🔄 새로고침                     │
│ ─────────────────────────────── │
│ ❌ 종료                         │
└─────────────────────────────────┘
```

## 설치

### 의존성

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
```

### 자동 설치

```bash
chmod +x install.sh
./install.sh
```

### 수동 실행

```bash
python3 baro_indicator.py
```

## 사용법

1. **경로 추가**: 트레이 메뉴 → 설정 → 추가 버튼
2. **폴더 열기**: 트레이 메뉴 → 경로 별칭 → 📂 폴더 열기
3. **터미널 열기**: 트레이 메뉴 → 경로 별칭 → 🖥️ 터미널 열기
4. **순서 변경**: 설정 창에서 ▲/▼ 버튼 또는 드래그 앤 드롭
5. **정렬 변경**: 설정 창 상단 정렬 옵션에서 선택

## 설정 파일

설정은 `~/.config/baro/settings.json`에 저장됩니다.

```json
{
  "sort_mode": "custom",
  "terminal": "gnome-terminal",
  "file_manager": "xdg-open",
  "paths": [
    {"alias": "문서", "path": "/home/user/Documents", "order": 0},
    {"alias": "다운로드", "path": "/home/user/Downloads", "order": 1}
  ]
}
```

## 지원 터미널

- gnome-terminal
- konsole
- xfce4-terminal
- tilix
- alacritty
- kitty
- 기타 (cwd 옵션 지원 필요)

## 라이선스

Copyright (C) 2026 DINKI'ssTyle. All rights reserved.
