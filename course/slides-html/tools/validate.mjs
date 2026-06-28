import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const file = process.argv[2];
if (!file) { console.error('usage: validate.mjs <deck.html>'); process.exit(2); }
const html = readFileSync(file, 'utf8');
const dir = dirname(file);
const fails = [];

// exactly one current slide
const current = (html.match(/class="[^"]*\bcurrent\b[^"]*"/g) || []).length;
if (current !== 1) fails.push(`expected exactly 1 current slide, found ${current}`);

// at least one figure
if (!/<figure|<img|<svg/i.test(html)) fails.push('no figure/img/svg present');

// zero MBA
if (/mba/i.test(html)) fails.push('contains "MBA"');

// every img src resolves (skip remote URLs and data URIs)
for (const m of html.matchAll(/<img[^>]*\ssrc="([^"]+)"/g)) {
  const src = m[1];
  if (/^(https?:)?\/\//.test(src) || src.startsWith('data:')) continue;
  if (!existsSync(resolve(dir, src))) fails.push(`missing image: ${src}`);
}

// balanced KaTeX $ delimiters (count un-escaped $)
const dollars = (html.match(/(?<!\\)\$/g) || []).length;
if (dollars % 2 !== 0) fails.push(`odd number of $ delimiters (${dollars}) — KaTeX will mis-render`);

if (fails.length) { for (const f of fails) console.log(`FAIL: ${f}`); process.exit(1); }
console.log(`OK: ${file}`);
