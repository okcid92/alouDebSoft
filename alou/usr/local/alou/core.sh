#!/bin/sh
# Alou core CLI functions

ALOU_DIR=/usr/local/alou

_alou_help() {
  cat <<EOF
Alou - commandes disponibles:
  alou help                Affiche cette aide
  alou maj                 Mise à jour système + environnements (basique)
  alou clean [type]        Nettoyage: node, python, laravel, all
  alou gitp [msg]          git add/commit/push
  alou gita [msg]          git add/commit (local)
  alou ext <archive>       Extraction universelle
  alou yt <url>            Téléchargement YouTube via yt-dlp
  alou dashboard           Affiche le dashboard terminal
EOF
}

alou_main() {
  cmd="$1"; shift || true
  case "$cmd" in
    help|--help|-h|"") _alou_help ;;
    maj) . "$ALOU_DIR"/system.sh && maj "$@" ;;
    update) . "$ALOU_DIR"/system.sh && maj "$@" ;;
    clean) . "$ALOU_DIR"/cleanup.sh && cleanup "$@" ;;
    gitp) . "$ALOU_DIR"/git.sh && gitp "$@" ;;
    gita) . "$ALOU_DIR"/git.sh && gita "$@" ;;
    ext) . "$ALOU_DIR"/media.sh && ext "$@" ;;
    yt) . "$ALOU_DIR"/media.sh && yt "$@" ;;
    dashboard) . "$ALOU_DIR"/dashboard.sh && _dashboard ;;
    *) echo "Alou: commande inconnue '$cmd'"; _alou_help; exit 2 ;;
  esac
}

if [ "${BASH_SOURCE:-}" = "" ]; then
  # when sourced nothing to do
  :
fi
