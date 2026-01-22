import { chromium } from 'playwright';

const url = process.argv[2] || 'http://localhost:4005/indie-hacking-update/indie-hacking-update.html';

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  recordVideo: { dir: './', size: { width: 1920, height: 1080 } }
});

const page = await context.newPage();
await page.goto(url, { waitUntil: 'networkidle' });

// Click to start video backdrop if needed
await page.click('body');
await page.waitForTimeout(1000);

// Get total slides by pressing End to go to last, then count
// First let's navigate through slides
const slideDuration = 12958; // ms per slide (~79 sec total for 13 slides)

// Navigate through slides by pressing arrow right
for (let i = 0; i < 12; i++) {  // 13 slides = 12 transitions
  await page.waitForTimeout(slideDuration);
  await page.keyboard.press('ArrowRight');
}

// Pause at end
await page.waitForTimeout(2000);

await context.close();
await browser.close();

console.log('Presentation video recorded!');
