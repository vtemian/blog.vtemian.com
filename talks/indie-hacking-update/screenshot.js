const puppeteer = require('puppeteer');

const url = process.argv[2];
const output = process.argv[3] || 'screenshot.png';

if (!url) {
  console.error('Usage: node screenshot.js <url> [output.png]');
  process.exit(1);
}

async function screenshot(url, output) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  // Just capture viewport, no scrolling
  await page.screenshot({ path: output, clip: { x: 0, y: 0, width: 1400, height: 900 } });
  await browser.close();
  console.log(`Screenshot saved to ${output}`);
}

screenshot(url, output);
