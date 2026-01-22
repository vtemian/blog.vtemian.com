import { chromium } from 'playwright';

// Try the media tab which might show content without login
const url = 'https://x.com/sisif_ai/media';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 600, height: 900 },
  recordVideo: { dir: './', size: { width: 600, height: 900 } },
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
});

const page = await context.newPage();

console.log('Navigating to Twitter media tab...');
await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(3000);

// Dismiss dialogs
try {
  await page.getByText('Refuse non-essential cookies').click();
  await page.waitForTimeout(500);
} catch (e) {}

await page.keyboard.press('Escape');
await page.waitForTimeout(500);
await page.keyboard.press('Escape');
await page.waitForTimeout(1000);

await page.screenshot({ path: 'twitter-media.png' });
console.log('Screenshot saved');

// Scroll
for (let i = 0; i < 10; i++) {
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(600);
}

await page.waitForTimeout(1000);
const videoPath = await page.video().path();
await context.close();
await browser.close();

import { execSync } from 'child_process';
const videoFile = videoPath.split('/').pop();
execSync(`ffmpeg -y -i ${videoFile} -vf "fps=12,scale=500:-1:flags=lanczos" -loop 0 sisif-twitter-scroll.gif`, { stdio: 'inherit' });
console.log('Done!');
