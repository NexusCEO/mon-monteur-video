# Parole filmée : transcrire, corriger, couper, sous-titrer

## 1. Préparer les prises

Extraire l'audio de chaque prise en WAV mono 16 kHz pour la transcription ; garder la vidéo d'origine intacte dans `source/`. Nommer les prises par une lettre ou un mot court (`a`, `b`, `ouverture`).

```bash
ffmpeg -i source/a.mp4 -vn -ac 1 -ar 16000 clips/a.wav
```

## 2. Transcrire mot à mot

```bash
npx hyperframes transcribe clips/a.wav --json
```

Il faut un horodatage par mot (`début`, `fin`, `texte`). Rassembler les prises dans un seul JSON : `{"a": [{"words": [{"s": 0.08, "e": 1.2, "w": "Bonjour"}]}], "b": [...]}`.

## 3. Corriger

Les moteurs de transcription se trompent surtout sur :

- les noms propres et les sigles (souvent transformés en mots courants) ;
- les homophones (`rênes`/`règnes`, `dessein`/`dessin`, `jour`/`joue`) ;
- les négations avalées (`il a cessé` au lieu de `il n'a cessé`) : une correction ici change le sens, la vérifier à l'oreille.

Écrire les corrections dans un fichier, pas dans le JSON transcrit : `{"a": [["séquence entendue", "séquence corrigée"]]}`. Le script répartit la durée de l'ancienne séquence sur les nouveaux mots et signale toute correction introuvable.

## 4. Couper les silences

```bash
python3 scripts/coupe-silences.py transcription.json src/edit.json \
  --ordre a,d,c,b --corrections corrections.json --fin d=34.3
```

- `--ecart 0.35` : au-delà de cet écart entre deux mots, on coupe.
- `--avant 0.08 --apres 0.15` : marge gardée autour de chaque segment, pour ne pas manger les attaques ni les finales.
- `--fin prise=secondes` : arrêter une prise sur sa dernière phrase audible.

La sortie donne, par prise, les segments à garder et les mots corrigés avec leur horodatage : de quoi monter les plans et afficher les sous-titres mot à mot.

Écouter le résultat : un écart de 0,35 s convient à un débit normal ; l'augmenter pour un orateur lent, sinon le montage halète.

## 5. Ordonner

Un montage de témoignages se construit : une ouverture brève et chaleureuse, les messages courts, puis le message le plus fort, de préférence celui qui se termine par la formule attendue (vœu, remerciement, appel). Fondre une musique discrète dessous, plus forte seulement entre les prises.

## 6. Sous-titres

- 1 à 2 lignes, 42 caractères au plus par ligne.
- 1 s minimum, 3,5 s maximum par carton ; environ 17 caractères par seconde.
- Couper entre les groupes de sens, jamais entre un article et son nom.
- Orthographe et ponctuation corrigées, sigles officiels en capitales.
- Dans le cadre : zone sûre 80 %, au-dessus de l'interface des applis en 9:16.
- Incrustés pour les réseaux sociaux (la plupart des gens regardent sans le son) ; livrer aussi le `.srt` pour YouTube, Facebook et Premiere.
- Style mot à mot surligné pour un format court ; phrase entière pour une présentation.

Chercher un style existant avant d'en coder un : `npx hyperframes catalog --query "caption" --type component --json`.
