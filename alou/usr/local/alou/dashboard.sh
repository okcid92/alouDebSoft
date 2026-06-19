#!/bin/sh
# Simple terminal dashboard displayed on interactive shells

_dashboard() {
  user="$(whoami)"
  host="$(hostname -s)"
  free_info="$(free -m | awk 'NR==2{printf "%dMB/%dMB (%.0f%%)", $3,$2,$3/$2*100 }')"
  disk_info="$(df -h / | awk 'NR==2{print $5 " used (" $4 " available)"}')"

  # colors if supported
  GREEN="$(printf '\033[32m')"; RESET="$(printf '\033[0m')"

  printf '\n%sAlou Dashboard%s - %s@%s\n' "$GREEN" "$RESET" "$user" "$host"
  printf 'RAM: %s\n' "$free_info"
  printf 'Disk: %s\n\n' "$disk_info"
}

# Optional automatic dashboard for interactive shells.
# Enable explicitly with: export ALOU_SHOW_DASHBOARD=1
case "$-" in
  *i*) [ "${ALOU_SHOW_DASHBOARD:-0}" = "1" ] && _dashboard ;;
  *) ;;
esac
