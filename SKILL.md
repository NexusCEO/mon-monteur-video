---
name: mon-monteur-video
description: Mon Monteur Vidéo — monteur vidéo de bout en bout pour vidéos promo, annonces d'événement, présentations de site ou d'application, montages de témoignages et déclinaisons réseaux sociaux (16:9, 9:16, WhatsApp). Choisit le bon moteur (HyperFrames, Remotion, Premiere Pro, Pillow+ffmpeg), cale image et son sur une seule source de temps, fabrique musique, bruitages, voix et sous-titres, puis contrôle le rendu image par image avant de livrer. À utiliser pour « monte une vidéo », « fais une pub », « teaser », « version TikTok », « coupe les silences », « ajoute des sous-titres », « cale sur la musique ».
---

# Mon Monteur Vidéo

Un monteur qui livre un fichier vérifié, pas un brouillon. Ce skill ne remplace pas les skills spécialisés : il décide lequel utiliser, dans quel ordre, et applique les règles apprises sur des projets réels.

## 1. Avant de toucher au montage

1. **Lire le brief et les sources.** Lister ce qui existe : affiche (PSD, PDF, JPG), logo, photos, rushs, musique fournie, voix, texte.
2. **Vérifier l'outillage** (`references/outillage.md`) : Node 22+, FFmpeg, Python, Premiere ouvert ou non. Sur un poste sans FFmpeg système, utiliser celui d'un paquet (`imageio-ffmpeg`, Remotion) plutôt que de bloquer.
3. **Fixer trois choses avec la personne, en une seule question si elles manquent :** le message unique de la vidéo, les formats de sortie (16:9, 9:16, WhatsApp), la durée visée. Tout le reste se décide seul.
4. **Ne rien inventer sur le fond.** Dates, lieux, prix, numéros, noms et fonctions viennent des sources ou de la personne. Un doute sur un nom propre : demander.

## 2. Choisir le moteur

| Situation | Moteur | Skill à charger |
| --- | --- | --- |
| Nouvelle vidéo motion design, promo, explainer, vertical | HyperFrames (HTML rendu en vidéo) | `/hyperframes`, puis `/hyperframes-cli` |
| Effet, transition, style de sous-titre, graphique « nommé » | Registre HyperFrames avant de coder à la main | `/hyperframes-registry` |
| Musique, bruitages, voix, transcription, détourage, étalonnage | Outils média | `/media-use` |
| Projet Remotion existant à modifier | Rester en Remotion ; ne migrer que si demandé | `/remotion-to-hyperframes` pour migrer |
| Refaire une vidéo de référence à l'identique | Rétro-ingénierie image par image | `/reverse-any-video` |
| Finition, export, sous-titres sur un montage déjà dans Premiere | MCP `premiere-pro` | — |
| Rendu procédural pur (logo dévoilé, captures de site), aucun navigateur | Python Pillow + FFmpeg, image par image | — |
| Vidéo générée par IA, avatar | Higgsfield ou HeyGen, après accord sur le coût | `/higgsfield-generate`, `/media-use` |

Règle de choix : le moteur le plus simple qui rend le résultat éditable par la personne ensuite. Détails et pièges de chaque moteur : `references/moteurs.md`.

## 3. Une seule source de temps

La cause n°1 d'un montage raté est un son et une image qui ne lisent pas le même minutage.

- Écrire **un fichier de minutage** (`timing.mjs`, `plan.json`) : liste des scènes avec leur durée, et la liste des repères (`cues`) où quelque chose se passe à l'écran.
- L'image **et** les scripts audio importent ce fichier. Jamais de durée recopiée à deux endroits.
- Calculer la durée totale depuis la composition, puis générer la musique à cette durée (`scripts/duree-composition.mjs` pour Remotion).
- **Musique fournie :** mesurer son tempo, puis compter en mesures. `temps = 60 × fps / BPM` images, `mesure = 4 × temps`. Chaque coupe tombe sur un premier temps ; noter le décalage du premier temps (souvent 0,02 à 0,03 s).
- **Déclinaisons** (plusieurs intervenants, plusieurs offres) : un objet de variantes dans le fichier de minutage, une composition par variante et par format, un script `render` qui boucle dessus.

## 4. Rythme et contenu

- **Environ 5 s par visuel à lire.** Trop rapide est le reproche le plus fréquent. Un format court vertical peut descendre à 2–3 s, pas moins pour du texte.
- **Vidéo publique = offre, preuve, appel à l'action.** Les pages internes (charte graphique, typographies, maquettes de papeterie) n'intéressent pas le public : les sortir du montage.
- **Appel à l'action final** tenu 5 à 8 s, avec le contact confirmé et les moyens de paiement ou d'inscription.
- **Logo jamais retouché.** Partir du fichier d'origine (AI, PDF, SVG), ne pas le recolorer ni le redessiner ; animer seulement son apparition (masque qui le dévoile). La dernière image du logo est identique à l'original.
- **Personnes à l'écran :** étiquette nom + fonction, pointée sur la bonne personne (coordonnées en pixels de la photo dans le fichier de minutage), caméra qui passe sur chacun puis plan large.
- **Affiche fournie en PSD/PDF :** en extraire les calques et le fond plutôt que de recomposer de mémoire ; reprendre ses couleurs et ses polices.
- **Zones sûres :** contenu dans 90 % du cadre, texte clé et sous-titres dans 80 %. En 9:16, laisser libre le bas (interface TikTok, Reels) et le haut.

## 5. Son

Détails : `references/son.md`.

- Une vidéo de plus de ~15 s qui raconte quelque chose a de la musique et des bruitages sur les actions visibles, sauf demande de silence.
- **Droits :** musique fournie par la personne, catalogue sous licence, ou musique synthétisée par script (libre de droits par construction). Jamais un titre du commerce récupéré en ligne.
- **Bruitages** calés sur les `cues` du fichier de minutage, dans l'ambiance du sujet (cuisine pour un traiteur, papier et notifications pour une appli).
- **Mixage de départ :** musique 0,62, bruitages 0,85, limiteur doux `tanh` (`scripts/mix.mjs`). Sous une voix, baisser la musique (ducking) ; la voix reste intelligible sur un haut-parleur de téléphone.
- **Voix off :** une ligne par fichier, puis transcription mot à mot pour caler texte et sous-titres sur la voix réelle, pas sur une estimation.

## 6. Parole filmée : couper et sous-titrer

Détails : `references/parole.md`.

1. Transcrire avec horodatage par mot (`npx hyperframes transcribe`, Whisper ou Parakeet).
2. **Corriger la transcription** : noms propres, sigles, homophones. Les moteurs écorchent presque toujours les noms et les sigles ; relire chaque phrase.
3. Couper les silences : `scripts/coupe-silences.py` regroupe les mots séparés de moins de 0,35 s et ajoute 0,08 s avant, 0,15 s après. Finir sur une phrase complète ; retirer une fin inaudible.
4. Ordonner les prises pour raconter : ouverture courte et chaleureuse, message long au milieu ou en fin s'il se conclut bien.
5. Sous-titres : 1 à 2 lignes, ≤ 42 caractères par ligne, 1 à 3,5 s par carton, jamais coupés au milieu d'un groupe de mots. Livrer aussi le `.srt`.

## 7. Contrôler avant de livrer

Ne jamais annoncer « terminé » sur la seule foi d'un rendu sans erreur.

1. Extraire des images aux moments clés : début, chaque transition, milieu de chaque scène, dernière image. Les **regarder**. Une planche-contact suffit pour le rythme.
2. Vérifier : texte lisible et sans faute, rien de coupé au bord, bon nom sur la bonne personne, logo intact, dernière image propre.
3. Vérifier le fichier : non vide, durée = durée prévue, piste audio présente, `yuv420p`, son synchrone à une coupe précise.
4. HyperFrames : `npx hyperframes check --json` sans erreur, puis `snapshot`. Remotion : `remotion still` aux images clés.
5. Montrer l'aperçu et attendre l'accord avant le rendu final ou toute publication, sauf demande explicite d'aller au bout.

## 8. Exporter et décliner

Détails et commandes : `references/export.md`.

| Sortie | Cadre | Réglage de départ |
| --- | --- | --- |
| Master, YouTube, Facebook | 1920×1080, 30 i/s | H.264, CRF 16–18, `yuv420p`, AAC 192 k |
| TikTok, Reels, Shorts | 1080×1920, 30 i/s | H.264, CRF 20–23 |
| WhatsApp, envoi direct | 1280×720 ou 720×1280 | H.264, CRF 26–28, AAC 128 k, `+faststart`, viser < 100 Mo (statut : ≤ 60 s) |
| Site web | selon la page | version légère + image d'affiche |

- Le 9:16 est **recomposé**, pas recadré : mêmes scènes, mise en page verticale, textes plus gros.
- Nommer les fichiers par contenu et destination : `sujet-facebook.mp4`, `sujet-tiktok.mp4`, `sujet-whatsapp.mp4`. Sorties dans `out/` ou `livrables/`, sources dans `source/`.
- Passer par Premiere seulement si la personne veut retoucher à la main : y importer le rendu, les stems audio et le `.srt`.

## 9. Travailler à plusieurs sessions

Une seule session écrit dans un dossier de projet à la fois. Deux sessions sur le même dossier s'écrasent. Les rendus longs tournent en arrière-plan, détachés, avec un journal qu'on relit.

## Fichiers du skill

- `references/moteurs.md` — forces, pièges et commandes de chaque moteur
- `references/son.md` — musique synthétisée, bruitages, mixage, voix
- `references/parole.md` — transcription, corrections, coupe des silences, sous-titres
- `references/export.md` — commandes FFmpeg de déclinaison et de contrôle
- `references/outillage.md` — installation sans droits administrateur, Premiere MCP
- `references/lecons.md` — retours reçus sur des projets réels, à relire avant chaque livraison
- `scripts/mix.mjs`, `scripts/coupe-silences.py`, `scripts/duree-composition.mjs`, `scripts/planche-contact.sh`
