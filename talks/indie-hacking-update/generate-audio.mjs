import fs from 'fs';

const ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY;
const VOICE_ID = process.env.ELEVENLABS_VOICE_ID || 'pNInz6obpgDQGcFmaJgB'; // Adam voice default

if (!ELEVENLABS_API_KEY) {
  console.error('Set ELEVENLABS_API_KEY environment variable');
  process.exit(1);
}

const text = fs.readFileSync('./narration-elevenlabs.txt', 'utf-8');

console.log('🎙️ Generating audio with timestamps from ElevenLabs...');

// Use the with-timestamps endpoint
const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}/with-timestamps`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'xi-api-key': ELEVENLABS_API_KEY
  },
  body: JSON.stringify({
    text: text,
    model_id: 'eleven_multilingual_v2',
    voice_settings: {
      stability: 0.5,
      similarity_boost: 0.75,
      style: 0.0,
      use_speaker_boost: true
    }
  })
});

if (!response.ok) {
  const error = await response.text();
  console.error('ElevenLabs API error:', error);
  process.exit(1);
}

const result = await response.json();

// Save audio (base64 encoded)
const audioBuffer = Buffer.from(result.audio_base64, 'base64');
fs.writeFileSync('./narration.mp3', audioBuffer);
console.log('✅ Audio saved to narration.mp3');

// Save alignment data
const alignment = result.alignment;
fs.writeFileSync('./narration-alignment.json', JSON.stringify(alignment, null, 2));
console.log('✅ Alignment data saved to narration-alignment.json');

// Parse alignment to find slide transition points (where "..." occurs)
const chars = alignment.characters;
const startTimes = alignment.character_start_times_seconds;
const endTimes = alignment.character_end_times_seconds;

// Find positions of "..." in text and get their timestamps
const slideMarkers = [];
let searchPos = 0;

while (true) {
  const dotPos = text.indexOf('...', searchPos);
  if (dotPos === -1) break;

  // Get the end time of the "..." marker
  if (dotPos + 2 < endTimes.length) {
    slideMarkers.push({
      position: dotPos,
      time: endTimes[dotPos + 2]  // End of the third dot
    });
  }
  searchPos = dotPos + 3;
}

console.log(`\n📍 Found ${slideMarkers.length} slide transition markers:`);
slideMarkers.forEach((m, i) => {
  console.log(`  Slide ${i + 2} starts at: ${m.time.toFixed(2)}s`);
});

// Save slide timings for the video recorder
const slideTimes = [0, ...slideMarkers.map(m => m.time)];
fs.writeFileSync('./slide-timings.json', JSON.stringify(slideTimes, null, 2));
console.log('\n✅ Slide timings saved to slide-timings.json');
console.log('   Timings:', slideTimes.map(t => t.toFixed(1) + 's').join(', '));
