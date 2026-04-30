#!/bin/sh
# Simple terminal dashboard displayed on interactive shells

_dashboard() {
  user="$(whoami)"
  host="$(hostname -s)"
  free_info="$(free -m | awk 'NR==2{printf "%dMB/%dMB (%.0f%%)", $3,$2,$3/$2*100 }')"
  disk_info="$(df -h / | awk 'NR==2{print $5 " used (" $4 " available)"}')"

  # colors if supported
  GREEN="\033[32m"; YELLOW="\033[33m"; RED="\033[31m"; RESET="\033[0m"

  echo
  echo "${GREEN}Alou Dashboard${RESET} - $user@$host"
  echo "RAM: $free_info"
  echo "Disk: $disk_info"
  echo
}

# Run dashboard automatically for interactive shells
case "$-" in
  *i*) _dashboard ;;
  *) ;;
esac
