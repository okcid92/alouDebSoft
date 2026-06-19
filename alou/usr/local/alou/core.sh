#!/bin/sh
# Alou core CLI functions

ALOU_DIR=/usr/local/alou

_alou_help() {
  cat <<EOF
Alou - commandes disponibles:
  alou help                Affiche cette aide
  alou maj                 Mise à jour système + environnements (basique)
  alou clean [opts] [type] Nettoyage: node, python, laravel, all
                           opts: --dry-run, --yes
  alou gitp [--yes] [msg]  git add/commit/push avec confirmation
  alou gita [--yes] [msg]  git add/commit local avec confirmation
  alou ext <archive>       Extraction universelle
  alou yt <url>            Téléchargement YouTube via yt-dlp
  alou dashboard           Affiche le dashboard terminal
EOF
}

alou_main() {
  cmd="$1"; shift || true
  case "$cmd" in
    help|--help|-h|"") _alou_help ;;
    # shellcheck source=/dev/null
    maj) . "$ALOU_DIR/system.sh" && maj "$@" ;;
    # shellcheck source=/dev/null
    update) . "$ALOU_DIR/system.sh" && maj "$@" ;;
    # shellcheck source=/dev/null
    clean) . "$ALOU_DIR/cleanup.sh" && cleanup "$@" ;;
    # shellcheck source=/dev/null
    gitp) . "$ALOU_DIR/git.sh" && gitp "$@" ;;
    # shellcheck source=/dev/null
    gita) . "$ALOU_DIR/git.sh" && gita "$@" ;;
    # shellcheck source=/dev/null
    ext) . "$ALOU_DIR/media.sh" && ext "$@" ;;
    # shellcheck source=/dev/null
    yt) . "$ALOU_DIR/media.sh" && yt "$@" ;;
    # shellcheck source=/dev/null
    dashboard) . "$ALOU_DIR/dashboard.sh" && _dashboard ;;
    *) echo "Alou: commande inconnue '$cmd'"; _alou_help; exit 2 ;;
  esac
}
