import { execSync } from 'node:child_process';
import { existsSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');

const input = path.join(rootDir, 'media', 'versao mobile.mp4');
const outMp4 = path.join(rootDir, 'media', 'hero-video-mobile.mp4');
const outWebm = path.join(rootDir, 'media', 'hero-video-mobile.webm');
const outThumb = path.join(rootDir, 'media', 'video-preview-thumb-mobile.jpg');

if (!existsSync(input)) {
  console.error(`Erro: Arquivo original não encontrado em ${input}`);
  process.exit(1);
}

console.log('[1/3] Codificando MP4 mobile sem áudio (H.264, crf 26, faststart)...');
execSync(`ffmpeg -i "${input}" -an -vcodec libx264 -crf 26 -preset slow -movflags +faststart -y "${outMp4}"`, { stdio: 'inherit' });

console.log('[2/3] Codificando WebM mobile sem áudio (VP9, crf 32)...');
execSync(`ffmpeg -i "${outMp4}" -an -c:v libvpx-vp9 -crf 32 -b:v 0 -deadline realtime -cpu-used 4 -row-mt 1 -y "${outWebm}"`, { stdio: 'inherit' });

console.log('[3/3] Extraindo thumbnail/poster mobile de alta fidelidade...');
execSync(`ffmpeg -ss 00:00:03 -i "${outMp4}" -frames:v 1 -q:v 2 -y "${outThumb}"`, { stdio: 'inherit' });

const sizeOrig = (statSync(input).size / 1024 / 1024).toFixed(2);
const sizeMp4 = (statSync(outMp4).size / 1024 / 1024).toFixed(2);
const sizeWebm = (statSync(outWebm).size / 1024 / 1024).toFixed(2);

console.log('\n--- Resultado da Otimização Mobile ---');
console.log(`Original:     ${sizeOrig} MB`);
console.log(`MP4 Mobile:   ${sizeMp4} MB (-${Math.round((1 - sizeMp4 / sizeOrig) * 100)}%)`);
console.log(`WebM Mobile:  ${sizeWebm} MB (-${Math.round((1 - sizeWebm / sizeOrig) * 100)}%)`);
