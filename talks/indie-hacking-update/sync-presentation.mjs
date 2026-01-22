import { chromium } from 'playwright';
import { execSync } from 'child_process';
import fs from 'fs';

const url = process.argv[2] || 'http://localhost:4005/indie-hacking-update/indie-hacking-update.html';
const timingsFile = process.argv[3] || 'slide-timings.json';

// Load slide timings from ElevenLabs alignment data
console.log('📂 Loading slide timings from', timingsFile);
const slideTimes = JSON.parse(fs.readFileSync(timingsFile, 'utf-8'));

console.log(`⏱️ Slide start times (${slideTimes.length} slides):`);
slideTimes.forEach((t, i) => console.log(`  Slide ${i + 1}: ${t.toFixed(2)}s`));

// Get total audio duration
const durationOutput = execSync(
  `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3`,
  { encoding: 'utf-8' }
);
const totalDuration = parseFloat(durationOutput.trim());
console.log(`\n📊 Total audio duration: ${totalDuration.toFixed(2)}s`);

// Record video with synced transitions
console.log('\n🎬 Recording presentation with synced timing...');

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  recordVideo: { dir: './', size: { width: 1920, height: 1080 } }
});

const page = await context.newPage();
await page.goto(url, { waitUntil: 'networkidle' });

// Click to start video backdrop
await page.click('body');

const startTime = Date.now();

// Navigate through slides at the exact times from ElevenLabs
for (let i = 0; i < slideTimes.length - 1; i++) {
  const currentTime = (Date.now() - startTime) / 1000;
  const nextTransition = slideTimes[i + 1];
  const waitTime = Math.max(0, (nextTransition - currentTime) * 1000);

  console.log(`  Slide ${i + 1}: waiting ${(waitTime/1000).toFixed(1)}s until ${nextTransition.toFixed(1)}s`);
  await page.waitForTimeout(waitTime);
  await page.keyboard.press('ArrowRight');
}

// Wait for last slide until audio ends
const currentTime = (Date.now() - startTime) / 1000;
const remainingTime = Math.max(0, (totalDuration - currentTime) * 1000);
console.log(`  Last slide (${slideTimes.length}): waiting ${(remainingTime/1000).toFixed(1)}s until end`);
await page.waitForTimeout(remainingTime + 500);

await context.close();
await browser.close();

console.log('✅ Recording complete!');
