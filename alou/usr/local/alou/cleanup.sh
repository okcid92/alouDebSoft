#!/bin/sh
# Cleanup helper with dry-run and confirmation support.

_cleanup_usage() {
  echo "Usage: cleanup [--dry-run|-n] [--yes|-y] [node|python|django|laravel|all]"
}

_cleanup_confirm() {
  mode="$1"
  if [ "$CLEANUP_YES" = "1" ]; then
    return 0
  fi
  if [ ! -t 0 ]; then
    echo "Refus: confirmation requise pour cleanup $mode (utilise --yes pour automatiser)."
    return 1
  fi
  printf "Supprimer les artefacts '%s' depuis %s ? [y/N] " "$mode" "$(pwd)"
  read -r ans || return 1
  case "$ans" in
    y|Y|yes|YES|oui|OUI) return 0 ;;
    *) echo "Annulé."; return 1 ;;
  esac
}

_cleanup_run() {
  label="$1"
  shift
  if [ "$CLEANUP_DRY_RUN" = "1" ]; then
    echo "[dry-run] Cibles $label:"
    find "$@" -print
  else
    find "$@" -exec rm -rf '{}' +
  fi
}

cleanup() {
  CLEANUP_DRY_RUN=0
  CLEANUP_YES=0

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --dry-run|-n) CLEANUP_DRY_RUN=1; shift ;;
      --yes|-y) CLEANUP_YES=1; shift ;;
      --help|-h) _cleanup_usage; return 0 ;;
      *) break ;;
    esac
  done

  t="$1"
  case "$t" in
    node)
      _cleanup_confirm "$t" || return 1
      echo "Removing node_modules..."
      _cleanup_run node_modules . -type d -name node_modules -prune
      ;;
    python|django)
      _cleanup_confirm "$t" || return 1
      echo "Removing venv and __pycache__..."
      _cleanup_run __pycache__ . -type d -name __pycache__
      _cleanup_run .venv . -type d -name .venv -prune
      ;;
    laravel)
      _cleanup_confirm "$t" || return 1
      echo "Removing vendor and caches..."
      _cleanup_run vendor . -type d -name vendor -prune
      ;;
    all)
      _cleanup_confirm "$t" || return 1
      echo "Global cleanup: node_modules, vendor, __pycache__, .venv, target"
      _cleanup_run all . \( -type d -name node_modules -o -name vendor -o -name __pycache__ -o -name .venv -o -name target \) -prune
      ;;
    *)
      _cleanup_usage; return 2 ;;
  esac
}
