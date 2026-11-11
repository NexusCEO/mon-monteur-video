# Mon Monteur Vidéo

Skill pour Claude Code : un monteur vidéo de bout en bout. Il choisit le moteur adapté (HyperFrames, Remotion, Premiere Pro, Pillow + FFmpeg), cale l'image et le son sur une seule source de temps, fabrique musique, bruitages, voix et sous-titres, contrôle le rendu image par image, puis décline les formats (16:9, 9:16, WhatsApp).

Il condense les méthodes et les retours de plusieurs projets réels : vidéos promo, annonces d'événement, présentations de site et d'application, montages de témoignages.

## Installation

```bash
git clone https://github.com/NexusCEO/mon-monteur-video.git ~/.claude/skills/mon-monteur-video
```

Puis, dans Claude Code : `/mon-monteur-video`, ou simplement « monte-moi une vidéo… ».

## Contenu

| Fichier | Rôle |
| --- | --- |
| `SKILL.md` | La méthode : brief, choix du moteur, minutage, rythme, son, parole, contrôle, export |
| `references/moteurs.md` | HyperFrames, Remotion, Premiere Pro, Pillow + FFmpeg, vidéo générée |
| `references/son.md` | Musique synthétisée, bruitages, mixage, voix off, calage sur le tempo |
| `references/parole.md` | Transcription, corrections, coupe des silences, sous-titres |
| `references/export.md` | Commandes FFmpeg, déclinaisons, liste de contrôle |
| `references/outillage.md` | Installation sans droits administrateur, MCP Premiere |
| `references/lecons.md` | Retours reçus sur des projets réels |
| `scripts/mix.mjs` | Mixage de WAV avec gains et limiteur doux |
| `scripts/coupe-silences.py` | Plan de montage depuis une transcription mot à mot |
| `scripts/duree-composition.mjs` | Durée d'une composition Remotion |
| `scripts/planche-contact.sh` | Planche-contact de contrôle |

## Skills complémentaires

Ce skill oriente vers des skills spécialisés quand ils sont installés ; il ne les contient pas : `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `remotion-to-hyperframes`, `reverse-any-video`. Sans eux, la méthode, les références et les scripts restent utilisables.

## Prérequis

Node.js 22+, FFmpeg, Python 3.9+. Premiere Pro et son serveur MCP sont facultatifs.

## Licence

MIT — voir `LICENSE`.
