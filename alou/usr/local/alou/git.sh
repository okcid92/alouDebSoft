#!/bin/sh
# Git helper functions

gitp() {
  msg="$1"
  if [ -z "$msg" ]; then
    read -r -p "Commit message: " msg
  fi
  git add -A && git commit -m "$msg" && git push
}

gita() {
  msg="$1"
  if [ -z "$msg" ]; then
    read -r -p "Commit message (local only): " msg
  fi
  git add -A && git commit -m "$msg"
}

# gitp and gita will be available in interactive shells once sourced by /etc/profile.d/alou.sh