import { chromium } from 'playwright';

const url = process.argv[2];
const output = process.argv[3] || 'screenshot.png';

if (!url) {
  console.error('Usage: npx playwright test screenshot.mjs <url> [output.png]');
  process.exit(1);
}

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setViewportSize({ width: 1400, height: 800 });
await page.goto(url, { waitUntil: 'networkidle' });
await page.screenshot({ path: output });
await browser.close();
console.log(`Screenshot saved to ${output}`);
