#!/bin/sh
# Alou aliases

alias cat='batcat --paging=never 2>/dev/null || cat'
alias ls='lsd 2>/dev/null || ls'
alias reload="[ -f ~/.zshrc ] && source ~/.zshrc || true"

alias inst='sudo apt update && sudo apt install'
alias dinst='sudo apt remove'

alias usage='top -o %MEM'
alias ports="sudo lsof -i -P -n | grep LISTEN"

alias serverstart='sudo systemctl start mariadb apache2'
alias serverstop='sudo systemctl stop mariadb apache2'
alias serverrestart='sudo systemctl restart mariadb apache2'
alias serverstatus='sudo systemctl status mariadb apache2'

alias netscan="hostname -I | cut -d' ' -f1 | xargs -I {} nmap -sn {}/24"

alias nr="npm run"
alias dev="npm run dev"

alias py="python"
alias pip="python -m pip"
alias venv="python -m venv .venv && . .venv/bin/activate"

alias glog="git log --oneline --graph --decorate --all"
alias gp="git pull"

alias zshconfig="nano ~/.zshrc"

# Note: functions/aliases are loaded into interactive shells via /etc/profile.d/alou.sh