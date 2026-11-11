#!/usr/bin/env node
// Affiche la durée (en secondes) d'une composition Remotion, pour générer la musique à la bonne longueur.
// À lancer depuis la racine du projet Remotion.
// Usage : node duree-composition.mjs <IdComposition> [point d'entrée, défaut src/index.ts]
// Exemple : D=$(node scripts/duree-composition.mjs Pub) && node scripts/music.mjs "$D" pub
import { bundle } from "@remotion/bundler";
import { selectComposition } from "@remotion/renderer";

const [id, entryPoint = "src/index.ts"] = process.argv.slice(2);
if (!id) {
  console.error("usage : node duree-composition.mjs <IdComposition> [point d'entrée]");
  process.exit(1);
}

try {
  const serveUrl = await bundle({ entryPoint });
  const composition = await selectComposition({ serveUrl, id });
  console.log((composition.durationInFrames / composition.fps).toFixed(2));
} catch (error) {
  console.error(`duree-composition : ${error.message}`);
  process.exit(1);
}
