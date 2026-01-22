import { execSync } from 'child_process';
import fs from 'fs';

const markdownFile = process.argv[2] || 'indie-hacking-update.md';
const timingsFile = process.argv[3] || 'slide-timings.json';

// Load slide timings
console.log('📂 Loading slide timings...');
const slideTimes = JSON.parse(fs.readFileSync(timingsFile, 'utf-8'));

// Get total audio duration
const totalDuration = parseFloat(execSync(
  `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3`,
  { encoding: 'utf-8' }
).trim());

console.log(`⏱️ ${slideTimes.length} slides, audio duration: ${totalDuration.toFixed(2)}s`);

// Create slides directory
if (!fs.existsSync('slides')) fs.mkdirSync('slides');

// Export slides using Marp CLI (this exports full slides without fragment animations)
console.log('\n📸 Exporting slides with Marp CLI...');
execSync(`npx @marp-team/marp-cli ${markdownFile} --images png -o slides/slide.png --allow-local-files --image-scale 1.5`, { stdio: 'inherit' });

// Rename Marp output (slide.001.png) to our format (slide_000.png)
console.log('\n🔄 Renaming slide files...');
for (let i = 0; i < slideTimes.length; i++) {
  const marpName = `slides/slide.${String(i + 1).padStart(3, '0')}.png`;
  const ourName = `slides/slide_${String(i).padStart(3, '0')}.png`;
  if (fs.existsSync(marpName)) {
    fs.renameSync(marpName, ourName);
    console.log(`  ${marpName} -> ${ourName}`);
  }
}

// Calculate duration for each slide
const durations = [];
for (let i = 0; i < slideTimes.length; i++) {
  const start = slideTimes[i];
  const end = i < slideTimes.length - 1 ? slideTimes[i + 1] : totalDuration;
  durations.push(end - start);
}

console.log('\n⏱️ Slide durations:');
durations.forEach((d, i) => console.log(`  Slide ${i + 1}: ${d.toFixed(2)}s`));

// Create ffmpeg concat file with exact durations
let concatContent = '';
for (let i = 0; i < slideTimes.length; i++) {
  const filename = `slide_${String(i).padStart(3, '0')}.png`;
  concatContent += `file '${filename}'\n`;
  concatContent += `duration ${durations[i]}\n`;
}
// Add last image again (ffmpeg concat quirk)
concatContent += `file 'slide_${String(slideTimes.length - 1).padStart(3, '0')}.png'\n`;

fs.writeFileSync('slides/concat.txt', concatContent);
console.log('\n📝 Created concat.txt');

// Create video from images with exact timing
console.log('\n🎬 Creating video from slides...');
execSync(`cd slides && ffmpeg -y -f concat -safe 0 -i concat.txt -vsync vfr -pix_fmt yuv420p -c:v libx264 -preset fast -crf 22 ../presentation-slides.mp4`, { stdio: 'inherit' });

// Merge with audio
console.log('\n🔗 Merging with audio...');
execSync(`ffmpeg -y -i presentation-slides.mp4 -i narration.mp3 -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest presentation-with-audio.mp4`, { stdio: 'inherit' });

console.log('\n✅ Done! Created presentation-with-audio.mp4');
