#!/bin/sh
# System helper functions (maj)

maj() {
  echo "[alou] Mise à jour système (basique)"
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get autoremove -y
  else
    echo "apt-get non disponible"
  fi

  # Try update common dev managers if present (best-effort)
  if command -v nvm >/dev/null 2>&1; then
    echo "[alou] nvm présent — mise à jour manuelle recommandée"
  fi
  if command -v pyenv >/dev/null 2>&1; then
    echo "[alou] pyenv présent — mise à jour manuelle recommandée"
  fi

  echo "[alou] Mise à jour terminée"
}
