#!/bin/sh
# media helpers: ext and yt

ext() {
  f="$1"
  if [ -z "$f" ]; then
    echo "Usage: ext <archive>"; return 1
  fi
  case "$f" in
    *.tar.gz|*.tgz) tar xzf "$f" ;;
    *.tar.bz2) tar xjf "$f" ;;
    *.tar) tar xf "$f" ;;
    *.zip) unzip "$f" ;;
    *.rar) unrar x "$f" ;;
    *.7z) 7z x "$f" ;;
    *.gz) gunzip "$f" ;;
    *) echo "Format non supporté: $f"; return 2 ;;
  esac
}

yt() {
  url="$1"
  if [ -z "$url" ]; then
    echo "Usage: yt <url>"; return 1
  fi
  OUTDIR="$(pwd)/yt-downloads"
  mkdir -p "$OUTDIR"
  if command -v aria2c >/dev/null 2>&1; then
    aria_opts=("--external-downloader" "aria2c" "--external-downloader-args" "-x 4 -s 4 -k 1M")
  else
    aria_opts=()
  fi
  yt-dlp -o "$OUTDIR/%(uploader)s/%(playlist_index)s - %(title)s.%(ext)s" "${aria_opts[@]}" "$url"
}
