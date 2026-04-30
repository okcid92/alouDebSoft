# Alou

Alou est une boîte à outils pour développeurs distribuée sous forme de paquet Debian `.deb`.

Le projet installe un ensemble de scripts modulaires dans `/usr/local/alou/`, un lanceur CLI global, un chargement automatique pour les shells interactifs et une interface graphique simple.

## Ce que fournit Alou

- une commande globale `alou`
- des alias et fonctions chargés automatiquement dans les shells interactifs
- des helpers pour Git, système, nettoyage, médias et dashboard terminal
- une interface graphique légère via `alou-gui`

## Structure du projet

- `DEBIAN/` : scripts et métadonnées du paquet
- `etc/profile.d/alou.sh` : chargement automatique des scripts pour bash et zsh interactifs
- `usr/local/bin/alou` : point d’entrée CLI principal
- `usr/local/bin/alou-gui` : lanceur de l’interface graphique
- `usr/local/alou/` : modules shell et interface GTK
- `usr/share/applications/alou.desktop` : intégration au menu des applications

## Installation

Construire le paquet :

```sh
cd alou
./build_deb.sh
```

Installer le paquet :

```sh
sudo dpkg -i ../alou.deb
```

Après l’installation, ouvre un nouveau terminal pour charger automatiquement les alias et les fonctions.

## Utilisation

### CLI

```sh
alou help
alou update
alou clean
alou gitp "message de commit"
alou gita "message de commit local"
alou yt <url>
alou ext <archive>
alou dashboard
```

### Commandes disponibles dans le shell

Une fois le terminal relancé, les modules chargent automatiquement des commandes comme :

- `gitp`
- `gita`
- `maj`
- `cleanup`
- `mkcd`
- `yt`
- `ext`
- `help-cmd`

### GUI

Lancer l’interface graphique :

```sh
alou-gui
```

La GUI affiche une barre latérale, une zone principale et un journal d’actions. Elle sert de tableau de bord rapide pour certaines opérations courantes.

## Dépendances

Alou s’appuie sur plusieurs outils système, notamment :

- `git`
- `curl`
- `zsh`
- `yt-dlp`
- `aria2`
- `nmap`
- `lsd`
- `bat`

## Désinstallation

La suppression du paquet passe par l’outil Debian standard :

```sh
sudo apt remove alou
```

Pour supprimer aussi les fichiers de configuration restants, utiliser :

```sh
sudo apt purge alou
```

## Notes

- Le chargement automatique fonctionne pour les shells interactifs.
- Aucun changement manuel dans `~/.bashrc` ou `~/.zshrc` n’est requis.
- Le projet est pensé pour une installation simple via `.deb` et une utilisation immédiate.
