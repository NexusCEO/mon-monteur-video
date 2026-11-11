#!/usr/bin/env python3
"""Construit un plan de montage à partir d'une transcription mot à mot : mots corrigés et segments gardés.

Entrée  : {"<prise>": [{"words": [{"s": début, "e": fin, "w": "mot"}, ...]}, ...], ...}
Sortie  : {"clips": [{"id", "segments": [[début, fin], ...], "words": [...]}, ...]}

Usage :
  python3 coupe-silences.py transcription.json edit.json \
      [--ordre a,d,c,b] [--corrections corrections.json] [--fin d=34.3] \
      [--ecart 0.35] [--avant 0.08] [--apres 0.15]

corrections.json : {"<prise>": [["séquence entendue", "séquence corrigée"], ...]}
La comparaison ignore la casse et la ponctuation.
"""
import argparse
import json
import re
import sys


def normaliser(texte):
    return re.sub(r"[^\w']", "", texte.lower())


def fusionner_mots(segments):
    """Recolle les fragments que le moteur sépare autour des apostrophes et des traits d'union."""
    mots = []
    for segment in segments:
        for mot in segment["words"]:
            texte = mot["w"]
            colle = mots and (texte.startswith(("'", "-")) or mots[-1]["w"].endswith("'"))
            if colle:
                precedent = mots[-1]
                mots[-1] = {"s": precedent["s"], "e": mot["e"], "w": precedent["w"] + texte}
            else:
                mots.append({"s": mot["s"], "e": mot["e"], "w": texte})
    return mots


def corriger(mots, corrections, prise):
    """Remplace chaque séquence entendue par sa correction en répartissant la durée sur les nouveaux mots."""
    resultat = list(mots)
    for ancien, nouveau in corrections:
        cible = [normaliser(m) for m in ancien.split()]
        remplacants = nouveau.split()
        if not cible or not remplacants:
            print(f"{prise} : correction vide ignorée : {ancien!r}", file=sys.stderr)
            continue
        position = next(
            (i for i in range(len(resultat) - len(cible) + 1)
             if [normaliser(m["w"]) for m in resultat[i:i + len(cible)]] == cible),
            None,
        )
        if position is None:
            print(f"{prise} : correction introuvable : {ancien!r}", file=sys.stderr)
            continue
        debut = resultat[position]["s"]
        fin = resultat[position + len(cible) - 1]["e"]
        pas = (fin - debut) / len(remplacants)
        nouveaux = [
            {"s": round(debut + k * pas, 2), "e": round(debut + (k + 1) * pas, 2), "w": texte}
            for k, texte in enumerate(remplacants)
        ]
        resultat = resultat[:position] + nouveaux + resultat[position + len(cible):]
    return resultat


def segmenter(mots, ecart, avant, apres):
    """Regroupe les mots proches en segments et ajoute une marge autour de chacun."""
    segments = []
    for mot in mots:
        if segments and mot["s"] - segments[-1][1] <= ecart:
            segments[-1] = (segments[-1][0], mot["e"])
        else:
            segments.append((mot["s"], mot["e"]))
    return [[round(max(0.0, a - avant), 2), round(b + apres, 2)] for a, b in segments]


def lire_json(chemin):
    try:
        with open(chemin, encoding="utf-8") as fichier:
            return json.load(fichier)
    except (OSError, json.JSONDecodeError) as erreur:
        sys.exit(f"coupe-silences : lecture impossible de {chemin} : {erreur}")


def lire_fins(valeurs):
    fins = {}
    for valeur in valeurs:
        prise, _, secondes = valeur.partition("=")
        try:
            fins[prise] = float(secondes)
        except ValueError:
            sys.exit(f"coupe-silences : --fin attend prise=secondes, reçu {valeur!r}")
    return fins


def main():
    analyseur = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    analyseur.add_argument("transcription")
    analyseur.add_argument("sortie")
    analyseur.add_argument("--ordre", help="prises dans l'ordre du montage, séparées par des virgules")
    analyseur.add_argument("--corrections", help="fichier JSON de corrections par prise")
    analyseur.add_argument("--fin", action="append", default=[], metavar="PRISE=SECONDES",
                           help="ignorer les mots qui commencent après cet instant")
    analyseur.add_argument("--ecart", type=float, default=0.35, help="silence au-delà duquel on coupe (s)")
    analyseur.add_argument("--avant", type=float, default=0.08, help="marge avant chaque segment (s)")
    analyseur.add_argument("--apres", type=float, default=0.15, help="marge après chaque segment (s)")
    options = analyseur.parse_args()

    transcription = lire_json(options.transcription)
    corrections = lire_json(options.corrections) if options.corrections else {}
    fins = lire_fins(options.fin)
    ordre = options.ordre.split(",") if options.ordre else list(transcription)

    inconnues = [prise for prise in ordre if prise not in transcription]
    if inconnues:
        sys.exit(f"coupe-silences : prises absentes de la transcription : {', '.join(inconnues)}")

    clips = []
    for prise in ordre:
        mots = corriger(fusionner_mots(transcription[prise]), corrections.get(prise, []), prise)
        if prise in fins:
            mots = [mot for mot in mots if mot["s"] < fins[prise]]
        segments = segmenter(mots, options.ecart, options.avant, options.apres)
        clips.append({"id": prise, "segments": segments, "words": mots})
        duree = sum(fin - debut for debut, fin in segments)
        print(f"{prise} : {len(segments)} plans, {duree:.1f} s gardées", file=sys.stderr)

    with open(options.sortie, "w", encoding="utf-8") as fichier:
        json.dump({"clips": clips}, fichier, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
