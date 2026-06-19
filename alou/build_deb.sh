#!/bin/sh
set -e
PKG_DIR="$(pwd)"
OUT="../alou.deb"
PKG_BUILD="$(mktemp -d /tmp/alou-pkg.XXXXXX)"
trap 'rm -rf "$PKG_BUILD"' EXIT

echo "Preparing package files and permissions"
cp -a "$PKG_DIR"/DEBIAN "$PKG_BUILD"/
cp -a "$PKG_DIR"/etc "$PKG_BUILD"/
cp -a "$PKG_DIR"/usr "$PKG_BUILD"/

# Keep generated Python bytecode out of the Debian payload.
find "$PKG_BUILD" -type d -name "__pycache__" -prune -exec rm -rf {} \; || true
find "$PKG_BUILD" -type f -name "*.pyc" -delete || true

# Normalize package permissions, then restore executable entry points.
find "$PKG_BUILD" -type d -exec chmod 0755 {} \; || true
find "$PKG_BUILD" -type f -exec chmod 0644 {} \; || true
chmod +x "$PKG_BUILD"/DEBIAN/postinst || true
chmod +x "$PKG_BUILD"/DEBIAN/prerm || true
chmod +x "$PKG_BUILD"/DEBIAN/postrm || true
chmod +x "$PKG_BUILD"/usr/local/bin/alou || true
chmod +x "$PKG_BUILD"/usr/local/bin/alou-gui || true
find "$PKG_BUILD"/usr/local/alou -type f -name "*.sh" -exec chmod +x {} \; || true
find "$PKG_BUILD"/usr/local/alou -type f -name "*.py" -exec chmod +x {} \; || true

echo "Building package from $PKG_BUILD"
dpkg-deb --root-owner-group --build "$PKG_BUILD" "$OUT"
echo "Built $OUT"
