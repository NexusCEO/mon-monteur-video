#!/usr/bin/env node
// Mixe plusieurs WAV PCM 16 bits (même fréquence, même nombre de canaux) avec un gain par piste et un limiteur doux.
// Usage : node mix.mjs <sortie.wav> <piste.wav[:gain]> [<piste.wav[:gain]> …]
// Exemple : node mix.mjs out/bande-son.wav public/music.wav:0.62 public/sfx.wav:0.85
// La durée de la sortie est celle de la première piste.
import fs from "node:fs";
import path from "node:path";

const DRIVE = 1.05; // entrée du limiteur
const CEILING = 0.97; // niveau maximal en sortie
const FULL_SCALE = 32768;

const fail = (message) => {
  console.error(`mix.mjs : ${message}`);
  process.exit(1);
};

const readWav = (file) => {
  if (!fs.existsSync(file)) fail(`fichier introuvable : ${file}`);
  const buffer = fs.readFileSync(file);
  if (buffer.toString("ascii", 0, 4) !== "RIFF" || buffer.toString("ascii", 8, 12) !== "WAVE") {
    fail(`${file} n'est pas un fichier WAV`);
  }
  let offset = 12;
  let format = null;
  while (offset + 8 <= buffer.length) {
    const id = buffer.toString("ascii", offset, offset + 4);
    const size = buffer.readUInt32LE(offset + 4);
    const body = offset + 8;
    if (id === "fmt ") {
      format = {
        encoding: buffer.readUInt16LE(body),
        channels: buffer.readUInt16LE(body + 2),
        sampleRate: buffer.readUInt32LE(body + 4),
        bits: buffer.readUInt16LE(body + 14),
      };
    } else if (id === "data") {
      if (!format) fail(`${file} : bloc fmt manquant avant les données`);
      if (format.encoding !== 1 || format.bits !== 16) fail(`${file} : seul le PCM 16 bits est accepté`);
      const end = Math.min(body + size, buffer.length);
      return { ...format, header: buffer.subarray(0, body), samples: buffer.subarray(body, end) };
    }
    offset = body + size + (size % 2);
  }
  return fail(`${file} : bloc de données introuvable`);
};

const parseTrack = (argument) => {
  const cut = argument.lastIndexOf(":");
  const hasGain = cut > 0 && !Number.isNaN(Number(argument.slice(cut + 1)));
  const file = hasGain ? argument.slice(0, cut) : argument;
  const gain = hasGain ? Number(argument.slice(cut + 1)) : 1;
  return { file, gain, ...readWav(file) };
};

const [output, ...inputs] = process.argv.slice(2);
if (!output || inputs.length === 0) fail("usage : node mix.mjs <sortie.wav> <piste.wav[:gain]> …");

const tracks = inputs.map(parseTrack);
const [first] = tracks;
for (const track of tracks) {
  if (track.sampleRate !== first.sampleRate || track.channels !== first.channels) {
    fail(`${track.file} : fréquence ou nombre de canaux différent de ${first.file}`);
  }
}

const count = first.samples.length >> 1;
const mixed = Buffer.alloc(count * 2);
for (let i = 0; i < count; i++) {
  const position = i * 2;
  let value = 0;
  for (const track of tracks) {
    if (position + 1 < track.samples.length) value += (track.samples.readInt16LE(position) / FULL_SCALE) * track.gain;
  }
  mixed.writeInt16LE(Math.round(Math.tanh(value * DRIVE) * CEILING * (FULL_SCALE - 1)), position);
}

const header = Buffer.from(first.header);
header.writeUInt32LE(header.length - 8 + mixed.length, 4);
header.writeUInt32LE(mixed.length, header.length - 4);
fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
fs.writeFileSync(output, Buffer.concat([header, mixed]));
console.log(`${output} : ${(count / first.channels / first.sampleRate).toFixed(2)} s, ${tracks.length} piste(s)`);
