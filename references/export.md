# Export, déclinaisons et contrôle

`ffmpeg` désigne ici le binaire disponible (voir `outillage.md` s'il n'est pas dans le `PATH`).

## Ajouter le son à une vidéo muette

```bash
ffmpeg -i muet.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart sortie.mp4
```

## Master 16:9

```bash
ffmpeg -i rendu.mp4 -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart sujet-facebook.mp4
```

`-pix_fmt yuv420p` est obligatoire : sans lui, certains téléphones et lecteurs affichent une image noire.

## Vertical 9:16

Rendre la composition verticale (1080×1920) ; CRF 20 à 23 suffit pour TikTok, Reels et Shorts, qui recompressent de toute façon.

Recadrer un 16:9 n'est qu'un dépannage, pour un plan filmé dont le sujet est centré :

```bash
ffmpeg -i source.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:v libx264 -crf 21 -pix_fmt yuv420p -c:a copy vertical.mp4
```

## Version légère WhatsApp

```bash
ffmpeg -i master.mp4 -vf "scale=-2:720" -c:v libx264 -crf 27 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart sujet-whatsapp.mp4
```

- Vérifier le poids ; monter le CRF d'un cran ou passer à 540p si le fichier reste trop lourd pour être envoyé.
- Statut WhatsApp : 60 s au plus par segment ; découper proprement sur une coupe si la vidéo est plus longue.
- Pour un long montage de témoignages, la version légère fait couramment le quart du poids du master sans perte visible sur téléphone.

## Extrait, teaser

```bash
ffmpeg -ss 00:00:12 -to 00:00:27 -i master.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac teaser.mp4
```

Un vrai teaser se remonte (accroche, date, appel à l'action) ; l'extrait brut ne sert qu'à dépanner.

## Image d'affiche et miniature

```bash
ffmpeg -ss 4.5 -i master.mp4 -frames:v 1 -q:v 2 affiche.jpg
```

## Contrôle

```bash
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,pix_fmt -of default=nw=1 sortie.mp4
bash scripts/planche-contact.sh sortie.mp4 controle/planche.jpg 5   # une image toutes les 5 s
ffmpeg -ss 12.0 -i sortie.mp4 -frames:v 1 controle/image-12.0.jpg  # une image précise
```

Liste de contrôle avant livraison :

- [ ] durée = durée prévue ; fichier non vide ; piste audio présente
- [ ] `h264`, `yuv420p`, bonne taille de cadre, 30 i/s
- [ ] première et dernière image propres (pas de noir involontaire, pas de texte coupé)
- [ ] chaque texte lu en entier, sans faute, dans la zone sûre
- [ ] bon nom et bonne fonction sur chaque personne
- [ ] logo identique à l'original
- [ ] son synchrone sur une coupe repérable ; pas de saturation ; fin en fondu
- [ ] sous-titres présents, synchrones, `.srt` livré
- [ ] contact, date, lieu, prix conformes aux sources
- [ ] poids compatible avec la destination

## Rangement

```
source/      fichiers d'origine, jamais modifiés
public/ ou assets/   médias utilisés par le montage
controle/    images et planches de vérification, journaux de rendu
out/ ou livrables/   fichiers à remettre, nommés sujet-destination.mp4
```
