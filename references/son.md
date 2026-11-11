# Son

## D'où vient la musique

1. **Fournie par la personne** (hymne, jingle, titre dont elle a les droits) : mesurer le tempo, caler les coupes dessus.
2. **Catalogue sous licence** : `npx hyperframes media-use resolve --type bgm --intent "<ambiance>" --project <dossier>`.
3. **Synthétisée par script** : libre de droits par construction, durée exacte, structure calée sur les scènes.

Jamais de titre du commerce téléchargé. Créditer les sons CC BY.

## Musique synthétisée (Node, sans dépendance)

Recette qui a donné une ambiance « corporate » propre :

- 44 100 Hz, stéréo, tampons `Float32Array`, sortie WAV 16 bits.
- 120 BPM, progression Am7 – Fmaj7 – C – G, une mesure par accord.
- Couches : nappe (pad), arpège, basse, batterie légère, réverbération sur un bus d'envoi.
- Structure exprimée en mesures et calée sur les scènes : `build`, `main`, `break`, `drop`, `outro`, plus des montées (`risers`) avant les moments forts.
- Trois profils : long (présentation), publicité (appel à l'action final de 8 s), court vertical (énergique dès la première mesure, pas de pause).
- Fondu d'entrée court, fondu de sortie sur la dernière mesure.

Le script prend la durée en argument : `node scripts/music.mjs <secondes> <profil>`. La durée vient de la composition, jamais d'une constante.

## Bruitages

- Calés sur les repères du fichier de minutage (`cues`), en images converties en échantillons.
- Synthèse : bruit filtré passe-bande (biquad RBJ) pour souffles et glissements, sinus amortis pour tintements, clics courts pour apparitions de texte.
- Hasard semé (générateur congruentiel à graine fixe) : deux rendus donnent le même fichier.
- Panoramique à puissance constante : `gauche = cos((pan+1)·π/4)`, `droite = sin((pan+1)·π/4)`.
- Choisir la palette selon le sujet : cuisine et vaisselle pour la restauration, papier, épingle, notification et balayage pour une appli, impact sourd et ruban pour une annonce d'événement.
- Un bruitage par action visible importante. Trop de sons fatigue plus vite que pas assez.

Sons d'appoint tout prêts : `npx hyperframes media-use resolve --type sfx --intent "<son>"`.

## Mixage

`scripts/mix.mjs` : additionne des WAV 16 bits de même format avec un gain par piste, puis limite en douceur.

```bash
node scripts/mix.mjs out/bande-son.wav public/music.wav:0.62 public/sfx.wav:0.85
```

- Point de départ : musique 0,62, bruitages 0,85, voix 1,0.
- Limiteur : `tanh(v × 1,05) × 0,97`, jamais d'écrêtage dur.
- Sous une voix : musique autour de 0,25–0,35 pendant la parole, remontée dans les respirations.
- Normaliser la sortie finale (`npx hyperframes normalize-audio` ou `loudnorm` FFmpeg, cible −14 LUFS pour les réseaux).
- Garder les stems séparés (`voix.wav`, `musique.wav`, `effets.wav`, `mix.wav`) : ils servent pour une retouche dans Premiere.

## Voix off

- Écrire le texte, une ligne par idée, puis générer **un fichier par ligne** (`l1.wav`, `l2.wav`…).
- Voix gratuite locale : `npx hyperframes tts`. Voix de meilleure qualité ou clonée : service payant, après accord.
- Sigles : écrire la prononciation voulue dans le texte envoyé à la synthèse (lettres épelées ou mot), garder l'orthographe officielle à l'écran.
- Transcrire ensuite chaque ligne mot à mot et stocker `{src, dur, words:[{s,e,w}]}` : l'image lit ces durées réelles.
- Écouter chaque ligne avant de monter : une syllabe avalée se rattrape en régénérant une seule ligne.

## Caler l'image sur une musique fournie

```
images par temps   = 60 × fps / BPM
images par mesure  = 4 × images par temps
```

Exemple : 108 BPM à 30 i/s → 16,67 images par temps, 66,67 par mesure (2,22 s). Planifier chaque scène en nombre de mesures entières ; arrondir à l'image seulement au moment de poser la coupe, pas en cumulant des durées arrondies. Mesurer le tempo et le premier temps avec `npx hyperframes beats --json`.
