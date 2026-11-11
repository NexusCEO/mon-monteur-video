#!/usr/bin/env bash
# Fabrique une planche-contact (une image toutes les N secondes) pour contrôler un rendu d'un coup d'œil.
# Usage : planche-contact.sh <video> <sortie.jpg> [intervalle en secondes, défaut 5] [colonnes, défaut 4]
# FFMPEG=/chemin/vers/ffmpeg permet d'utiliser un binaire hors du PATH.
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage : planche-contact.sh <video> <sortie.jpg> [intervalle] [colonnes]" >&2
  exit 1
fi

video=$1
sortie=$2
intervalle=${3:-5}
colonnes=${4:-4}
ffmpeg_bin=${FFMPEG:-ffmpeg}

if [ ! -f "$video" ]; then
  echo "planche-contact : vidéo introuvable : $video" >&2
  exit 1
fi
if ! command -v "$ffmpeg_bin" >/dev/null 2>&1; then
  echo "planche-contact : ffmpeg introuvable (définir FFMPEG=/chemin/vers/ffmpeg)" >&2
  exit 1
fi

mkdir -p "$(dirname "$sortie")"
"$ffmpeg_bin" -v error -y -i "$video" \
  -vf "fps=1/${intervalle},scale=480:-2,tile=${colonnes}x0" \
  -frames:v 1 -q:v 3 "$sortie"
echo "$sortie"
