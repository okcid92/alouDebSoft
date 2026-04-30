#!/bin/sh
set -e
PKG_DIR="$(pwd)"
OUT="../alou.deb"

echo "Preparing package files and permissions"
# Make sure executables and maintainer scripts are executable
chmod +x "$PKG_DIR"/DEBIAN/postinst || true
chmod +x "$PKG_DIR"/DEBIAN/prerm || true
chmod +x "$PKG_DIR"/DEBIAN/postrm || true
chmod +x "$PKG_DIR"/usr/local/bin/alou || true
find "$PKG_DIR"/usr/local/alou -type f -name "*.sh" -exec chmod +x {} \; || true

echo "Building package from $PKG_DIR"
dpkg-deb --build "$PKG_DIR" "$OUT"
echo "Built $OUT"
