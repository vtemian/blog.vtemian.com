import { chromium } from 'playwright';

const url = process.argv[2] || 'https://sisif.ai';
const output = process.argv[3] || 'scroll-video';

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1200, height: 800 },
  recordVideo: { dir: './', size: { width: 1200, height: 800 } }
});

const page = await context.newPage();
await page.goto(url, { waitUntil: 'networkidle' });

// Slow scroll down
const scrollHeight = await page.evaluate(() => document.body.scrollHeight);
const steps = 30;
const stepSize = scrollHeight / steps;

for (let i = 0; i < steps; i++) {
  await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'smooth' }), i * stepSize);
  await page.waitForTimeout(150);
}

// Pause at bottom
await page.waitForTimeout(500);

await context.close();
await browser.close();

console.log('Video recorded. Convert to GIF with:');
console.log('ffmpeg -i <video.webm> -vf "fps=15,scale=600:-1" -loop 0 sisif-scroll.gif');
