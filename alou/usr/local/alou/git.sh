#!/bin/sh
# Git helper functions

_alou_git_message() {
  msg="$1"
  prompt="$2"
  if [ -z "$msg" ]; then
    printf "%s" "$prompt" >&2
    read -r msg
  fi
  if [ -z "$msg" ]; then
    echo "Message de commit requis"
    return 1
  fi
  printf "%s" "$msg"
}

_alou_git_confirm() {
  action="$1"
  if [ "$ALOU_GIT_YES" = "1" ]; then
    return 0
  fi
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Ce dossier n'est pas un dépôt Git"
    return 1
  fi
  echo "Changements qui seront ajoutés:"
  git status --short
  if [ ! -t 0 ]; then
    echo "Refus: confirmation requise pour $action (utilise --yes pour automatiser)."
    return 1
  fi
  printf "Continuer avec '%s' ? [y/N] " "$action"
  read -r ans || return 1
  case "$ans" in
    y|Y|yes|YES|oui|OUI) return 0 ;;
    *) echo "Annulé."; return 1 ;;
  esac
}

gitp() {
  ALOU_GIT_YES=0
  if [ "$1" = "--yes" ] || [ "$1" = "-y" ]; then
    ALOU_GIT_YES=1
    shift
  fi
  msg="$(_alou_git_message "$1" "Commit message: ")" || return 1
  _alou_git_confirm "git add/commit/push" || return 1
  git add -A && git commit -m "$msg" && git push
}

gita() {
  ALOU_GIT_YES=0
  if [ "$1" = "--yes" ] || [ "$1" = "-y" ]; then
    ALOU_GIT_YES=1
    shift
  fi
  msg="$(_alou_git_message "$1" "Commit message (local only): ")" || return 1
  _alou_git_confirm "git add/commit" || return 1
  git add -A && git commit -m "$msg"
}

# gitp and gita will be available in interactive shells once sourced by /etc/profile.d/alou.sh
