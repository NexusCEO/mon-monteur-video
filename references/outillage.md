# Outillage

## Vérifier ce qui est là

```bash
node --version        # 22 ou plus pour HyperFrames
which ffmpeg ffprobe
python3 --version
npx hyperframes doctor --json     # se fier à .ok, le code de sortie vaut toujours 0
```

## Poste sans droits administrateur

Pas de Homebrew ni de `sudo` : installer dans le dossier personnel.

- **Node** : archive officielle décompressée dans `~/.local/node`, puis `~/.local/node/bin` dans le `PATH`.
- **FFmpeg** sans installation système, au choix :
  - `pip install --user imageio-ffmpeg`, puis `python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` ;
  - `npm i ffmpeg-static ffprobe-static` dans le projet ;
  - Remotion embarque le sien : `npx remotion ffmpeg …` et `npx remotion ffprobe …`.
- Ne jamais télécharger un binaire depuis une source non vérifiée ; si l'installation est refusée, le dire et demander à la personne de l'installer.
- Python ancien sur le poste : créer un environnement virtuel par projet, ou faire tourner l'étape dans un conteneur.

## Serveur MCP Premiere Pro

- Construit depuis les sources (pas de paquet prêt à l'emploi) ; dépendances Python dans un environnement virtuel dédié, passé par `PYTHON_BIN`.
- Panneau CEP lié dans `~/Library/Application Support/Adobe/CEP/extensions`.
- Des services lancés depuis une session meurent avec elle. Les démarrer détachés :

```bash
PYTHON_BIN="$PWD/python-intelligence/.venv/bin/python" \
  nohup perl -MPOSIX -e 'POSIX::setsid(); exec @ARGV' ./scripts/start-all.sh \
  > start-all.out 2>&1 < /dev/null &
```

- Premiere doit être ouvert avec un projet ; tester avec `premiere_ping` avant toute commande.
- Sans FFmpeg, les outils d'analyse média du serveur (formes d'onde, détection de scènes) ne répondent pas ; le reste fonctionne.

## Rendus longs

- Moins de deux minutes : au premier plan.
- Plus long : en arrière-plan, sortie dans un journal, attendre la ligne de fin dans le journal plutôt que de surveiller le processus.
- Un rendu par projet à la fois ; deux rendus Chrome simultanés sur un poste modeste échouent ou ralentissent tout.

## Extraire depuis des fichiers de création

- **PDF ou AI vers PNG** : PDFKit (Swift), `mupdf` ou `sharp`, à l'échelle 3 ou 4 pour garder du piqué en zoom.
- **PSD** : exporter les calques utiles en PNG ; reconstituer un fond sans le texte par retouche (inpainting) si l'affiche n'existe qu'aplatie.
- **Site web** : capture pleine page en résolution Retina (WebKit) ou `npx hyperframes capture <url> --json`. Prendre une version « haut de page » et une version « pleine page » de chaque écran.
