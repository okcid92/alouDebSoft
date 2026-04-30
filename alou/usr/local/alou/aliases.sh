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

# Utility: create directory and cd into it
mkcd() {
	if [ -z "$1" ]; then
		echo "Usage: mkcd <dir>"; return 1
	fi
	mkdir -p "$1" && cd "$1" || return 1
}

# Show source for an alias/function by scanning /usr/local/alou/*.sh
help-cmd() {
	name="$1"
	if [ -z "$name" ]; then
		echo "Usage: help-cmd <name>"; return 1
	fi
	echo "Searching source for '$name' in /usr/local/alou/*.sh..."
	grep -nH -E "^[[:space:]]*(alias[[:space:]]+$name=|function[[:space:]]+$name\b|^$name\s*\()" /usr/local/alou/*.sh || \
		echo "Source not found in /usr/local/alou; try 'type $name' in your shell"
}