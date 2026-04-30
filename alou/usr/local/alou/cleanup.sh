#!/bin/sh
# Cleanup helper

cleanup() {
  t="$1"
  case "$t" in
    node)
      echo "Removing node_modules..."
      find . -type d -name node_modules -prune -exec rm -rf '{}' +
      ;;
    python|django)
      echo "Removing venv and __pycache__..."
      find . -type d -name __pycache__ -exec rm -rf '{}' +
      find . -type d -name .venv -prune -exec rm -rf '{}' +
      ;;
    laravel)
      echo "Removing vendor and caches..."
      find . -type d -name vendor -prune -exec rm -rf '{}' +
      ;;
    all)
      echo "Global cleanup: node_modules, vendor, __pycache__, .venv, target"
      find . \( -type d -name node_modules -o -name vendor -o -name __pycache__ -o -name .venv -o -name target \) -prune -exec rm -rf '{}' +
      ;;
    *)
      echo "Usage: cleanup [node|python|laravel|all]" ;;
  esac
}
