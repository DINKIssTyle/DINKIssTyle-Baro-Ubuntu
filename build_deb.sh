#!/bin/bash
set -e

APP_NAME="baro"
VERSION="1.0.0"
ARCH="amd64"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$SCRIPT_DIR/deb_dist"
DIST_DIR="$SCRIPT_DIR/dist"
ICON_DIR="$SCRIPT_DIR/icons"

echo "==================================="
echo "  Baro .deb Build Script"
echo "==================================="

# 1. Build Binary
echo "[1/5] Building binary..."
if [ -f "$SCRIPT_DIR/build.sh" ]; then
    "$SCRIPT_DIR/build.sh"
else
    echo "Error: build.sh not found!"
    exit 1
fi

# 2. Prepare Directory Structure
echo "[2/5] Creating directory structure..."
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR/DEBIAN"
mkdir -p "$WORK_DIR/usr/bin"
mkdir -p "$WORK_DIR/usr/share/applications"
mkdir -p "$WORK_DIR/usr/share/icons/hicolor/128x128/apps"

# 3. Copy Files
echo "[3/5] Copying files..."
cp "$DIST_DIR/$APP_NAME" "$WORK_DIR/usr/bin/"
chmod 755 "$WORK_DIR/usr/bin/$APP_NAME"

# Copy Icon
if [ -f "$ICON_DIR/appicon.png" ]; then
    cp "$ICON_DIR/appicon.png" "$WORK_DIR/usr/share/icons/hicolor/128x128/apps/$APP_NAME.png"
else
    echo "Warning: Icon not found!"
fi

# Create Desktop File for Package
cat > "$WORK_DIR/usr/share/applications/$APP_NAME.desktop" << EOF
[Desktop Entry]
Name=Baro
Name[ko]=바로
Comment=Path Quick Access Indicator
Comment[ko]=경로 빠른 접근 인디케이터
Exec=/usr/bin/$APP_NAME
Icon=$APP_NAME
Terminal=false
Type=Application
Categories=Utility;System;
Keywords=path;folder;shortcut;terminal;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF

# 4. Create Control File
echo "[4/5] Creating control file..."
SIZE=$(du -s "$WORK_DIR/usr" | cut -f1)

cat > "$WORK_DIR/DEBIAN/control" << EOF
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Depends: python3, gir1.2-appindicator3-0.1, gir1.2-gtk-3.0
Maintainer: DINKIssTyle <dinki@me.com>
Description: Path Quick Access Indicator
 Baro is a system tray indicator that provides quick access to your favorite folders.
 It allows you to open folders in your file manager or terminal with just two clicks.
EOF

# 5. Build Package
echo "[5/5] Building .deb package..."
dpkg-deb --build "$WORK_DIR" "${APP_NAME}_${VERSION}_${ARCH}.deb"

echo
echo "==================================="
echo "  Package created: ${APP_NAME}_${VERSION}_${ARCH}.deb"
echo "==================================="
