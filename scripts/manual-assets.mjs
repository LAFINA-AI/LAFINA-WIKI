import { readFile, mkdir, copyFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root = fileURLToPath(new URL('../', import.meta.url));
const manual = JSON.parse(await readFile(path.join(root, 'src/data/manual.json'), 'utf8'));
const output = path.join(root, 'public/manual/screenshots');
await mkdir(output, { recursive: true });
let count = 0;
for (const chapter of manual.chapters) {
  for (const { image } of chapter.steps) {
    if (!image) continue;
    await copyFile(path.join(root, 'screenshots', image.source), path.join(output, image.file));
    count++;
  }
}
console.log(`Copied ${count} unique manual screenshots. Originals are unchanged.`);
