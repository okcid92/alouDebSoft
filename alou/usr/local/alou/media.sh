#!/bin/sh
# media helpers: ext and yt

ext() {
  f="$1"
  if [ -z "$f" ]; then
    echo "Usage: ext <archive>"; return 1
  fi
  if [ ! -f "$f" ]; then
    echo "Archive introuvable: $f"; return 1
  fi
  case "$f" in
    *.tar.gz|*.tgz) tar xzf "$f" ;;
    *.tar.bz2) tar xjf "$f" ;;
    *.tar) tar xf "$f" ;;
    *.zip) command -v unzip >/dev/null 2>&1 || { echo "unzip manquant"; return 1; }; unzip "$f" ;;
    *.rar)
      if command -v unrar >/dev/null 2>&1; then
        unrar x "$f"
      elif command -v unrar-free >/dev/null 2>&1; then
        unrar-free -x "$f"
      else
        echo "unrar ou unrar-free manquant"; return 1
      fi
      ;;
    *.7z) command -v 7z >/dev/null 2>&1 || { echo "7z manquant"; return 1; }; 7z x "$f" ;;
    *.gz) gunzip "$f" ;;
    *) echo "Format non supporté: $f"; return 2 ;;
  esac
}

yt() {
  url="$1"
  if [ -z "$url" ]; then
    echo "Usage: yt <url>"; return 1
  fi
  if ! command -v yt-dlp >/dev/null 2>&1; then
    echo "yt-dlp manquant"; return 1
  fi
  OUTDIR="$(pwd)/yt-downloads"
  mkdir -p "$OUTDIR"
  if command -v aria2c >/dev/null 2>&1; then
    set -- --external-downloader aria2c --external-downloader-args "-x 4 -s 4 -k 1M"
  else
    set --
  fi
  yt-dlp -o "$OUTDIR/%(uploader)s/%(playlist_index)s - %(title)s.%(ext)s" "$@" "$url"
}
