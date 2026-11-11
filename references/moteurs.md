# Moteurs de montage

## HyperFrames (par défaut pour une nouvelle vidéo)

HTML, CSS et animations GSAP rendus image par image ; le projet reste éditable dans l'aperçu Studio. Charger `/hyperframes` avant d'écrire une composition : le contrat de rendu n'est pas devinable.

Boucle de travail :

```bash
npx hyperframes init <dossier>            # ou: capture <url> --json pour un site
npx hyperframes lint
npx hyperframes check --json              # corriger chaque erreur
npx hyperframes snapshot --at 1,5,12      # regarder les PNG
npx hyperframes preview --background      # donner l'URL, attendre l'accord
npx hyperframes render --quality delivery --output out.mp4
```

Points qui cassent un rendu :

- Chaque élément minuté porte `class="clip"`, `data-start`, `data-duration` (secondes).
- Une timeline GSAP en pause par composition, enregistrée dans `window.__timelines["<id>"]`.
- Pas de `Date.now()`, de hasard non semé, de requête réseau, de `repeat: -1`.
- Ne jamais animer `display` ou `visibility` d'un `.clip` : animer un enfant.
- Chaque `<audio>` a un `id`, sinon il est absent du mix.
- Chemins d'assets relatifs à la racine (`assets/...`), y compris dans `compositions/`.
- Une scène par fichier dans `compositions/`, y compris `captions.html` pour tous les sous-titres.

Un projet par format (`projet-16x9/`, `projet-9x16/`) quand la mise en page diffère vraiment ; les sons et captures vivent dans un dossier commun.

## Remotion (projets existants)

React + TypeScript. Garder ce moteur pour modifier un projet qui l'utilise déjà.

Structure éprouvée :

```
src/Root.tsx          une <Composition> par variante et par format
src/timing.mjs        scènes, durées, variantes, repères — importé par l'image ET le son
src/components.tsx    briques réutilisées
scripts/music.mjs     musique synthétisée à la durée de la composition
scripts/sfx.mjs       bruitages calés sur timing.mjs
scripts/render.mjs    boucle variantes × formats
public/               médias ; out/ rendus ; source/ fichiers d'origine
```

```bash
npx remotion studio
npx remotion still <Id> controle/image-120.png --frame=120
npx remotion render <Id> out/sujet-facebook.mp4
npx remotion render <IdVertical> out/sujet-tiktok.mp4 --crf=23
```

- Épingler la même version exacte pour tous les paquets `remotion` et `@remotion/*`.
- Enchaîner dans `package.json` : durée → musique → bruitages → rendu, pour que le son suive toujours l'image.
- Polices : `@remotion/google-fonts` ou `@remotion/fonts` avec fichiers locaux ; attendre leur chargement.
- Migration vers HyperFrames : `/remotion-to-hyperframes`, avec comparaison image par image. `useState`, `useEffect` avec dépendances et kits d'interface React ne se traduisent pas.

## Premiere Pro (finition manuelle)

Via le serveur MCP `premiere-pro` : inspection du projet, import, placement de clips, transitions, niveaux audio, sous-titres depuis `.srt`, export.

1. `premiere_ping` : si pas de réponse, démarrer les services (voir `outillage.md`) et ouvrir Premiere.
2. `premiere_get_project`, `premiere_get_timeline` : lire avant d'écrire.
3. `premiere_save_sequence_version` avant toute modification destructive.
4. Importer rendu + stems + `.srt` ; `premiere_add_subtitles_from_srt`.
5. Export : `premiere_export` ou `premiere_export_via_ame`, puis contrôler le fichier comme tout autre rendu.

Premiere sert à la retouche humaine et à l'export, pas à fabriquer du motion design : le graphisme vient d'HyperFrames ou de Remotion.

## Python Pillow + FFmpeg (rendu procédural)

Utile quand il faut une maîtrise au pixel sans navigateur : dévoilement d'un logo vectoriel, défilement de captures de site dans un cadre de navigateur ou de téléphone.

- Une fonction `image(t)` pure qui renvoie l'image à l'instant `t` ; un mode `--image <t>` pour sortir une seule image de contrôle, un mode `--planche` pour une planche-contact.
- Écriture directe dans FFmpeg : `libx264`, `-crf 16`, `-preset slow`, `-pix_fmt yuv420p`.
- Rendre d'abord la vidéo muette, puis ajouter le son en une passe (`export.md`).
- Captures de site pleine page : WebKit (script Swift sur macOS) ou `npx hyperframes capture <url>`.
- Logo AI ou PDF vers PNG : PDFKit, `mupdf` ou `sharp`, à grande échelle, sans changer les couleurs.

## Vidéo générée par IA

Pour un plan impossible à filmer ou un avatar. Toujours annoncer le coût et obtenir l'accord avant un appel payant. Si le service demande une connexion, le dire et proposer la voie gratuite locale.
