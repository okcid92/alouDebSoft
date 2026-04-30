#!/bin/sh
# Alou loader: sources all scripts from /usr/local/alou for interactive shells

# Only run for interactive shells
case "$-" in
    *i*) ;;
    *) return 0;;
esac

ALOU_DIR=/usr/local/alou
if [ -d "$ALOU_DIR" ]; then
  for f in "$ALOU_DIR"/*.sh; do
    [ -r "$f" ] || continue
    # shellcheck source=/dev/null
    . "$f"
  done
fi

# Provide command-not-found handler for bash and zsh
command_not_found_handle() {
  cmd="$1"
  shift
  echo "alou: commande '$cmd' non trouvée. Voulez-vous l'installer via apt? (y/N)"
  read -r ans || return 127
  case "$ans" in
    y|Y)
      if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update
        sudo apt-get install -y "$cmd"
      else
        echo "apt-get non disponible"
      fi
      ;;
    *) return 127 ;;
  esac
}

# zsh uses command_not_found_handler
command_not_found_handler() { command_not_found_handle "$@"; }

export ALOU_DIR