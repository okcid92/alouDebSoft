#!/bin/sh
set -e
PKG_DIR="$(pwd)"
OUT="../alou.deb"

echo "Building package from $PKG_DIR"
dpkg-deb --build "$PKG_DIR" "$OUT"
echo "Built $OUT"
