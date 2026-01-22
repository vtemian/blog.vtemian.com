# Presentation Demo Generator
# Usage: make demo ELEVENLABS_API_KEY=sk_xxx

ELEVENLABS_API_KEY ?=
ELEVENLABS_VOICE_ID ?= pNInz6obpgDQGcFmaJgB
PRESENTATION_URL ?= http://localhost:4005/indie-hacking-update/indie-hacking-update.html
SLIDES ?= 13
AUDIO_DURATION ?= $(shell ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3 2>/dev/null || echo "80")

.PHONY: all demo audio video merge clean serve

all: demo

# Full pipeline: generate audio, record video, merge
demo: audio video merge
	@echo "✅ Demo created: presentation-with-audio.mp4"
	@open presentation-with-audio.mp4

# Generate audio from narration script using ElevenLabs
audio: narration.mp3

narration.mp3: narration-elevenlabs.txt generate-audio.mjs
ifndef ELEVENLABS_API_KEY
	$(error ELEVENLABS_API_KEY is required. Run: make demo ELEVENLABS_API_KEY=sk_xxx)
endif
	@echo "🎙️ Generating audio with ElevenLabs..."
	ELEVENLABS_API_KEY=$(ELEVENLABS_API_KEY) ELEVENLABS_VOICE_ID=$(ELEVENLABS_VOICE_ID) node generate-audio.mjs
	@echo "📊 Audio duration: $$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3) seconds"

# Record presentation video (requires server running)
video: presentation-demo.mp4

presentation-demo.mp4: record-presentation.mjs narration.mp3
	@echo "🎬 Recording presentation..."
	@# Calculate slide duration based on audio length
	$(eval AUDIO_LEN := $(shell ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration.mp3))
	$(eval SLIDE_MS := $(shell echo "scale=0; ($(AUDIO_LEN) * 1000) / $(SLIDES)" | bc))
	@echo "⏱️ Audio: $(AUDIO_LEN)s, Slide duration: $(SLIDE_MS)ms"
	@# Update slide duration in script
	@sed -i '' 's/const slideDuration = [0-9]*/const slideDuration = $(SLIDE_MS)/' record-presentation.mjs
	@node record-presentation.mjs $(PRESENTATION_URL)
	@# Convert latest webm to mp4
	@latest=$$(ls -t *.webm | head -1) && \
		ffmpeg -y -i "$$latest" -c:v libx264 -preset fast -crf 22 presentation-demo.mp4 2>/dev/null
	@echo "📊 Video duration: $$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 presentation-demo.mp4) seconds"

# Merge audio and video
merge: presentation-with-audio.mp4

presentation-with-audio.mp4: presentation-demo.mp4 narration.mp3
	@echo "🔗 Merging audio and video..."
	ffmpeg -y -i presentation-demo.mp4 -i narration.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest presentation-with-audio.mp4 2>/dev/null
	@echo "✅ Created presentation-with-audio.mp4"

# Start local server for recording
serve:
	@echo "🌐 Starting server at http://localhost:4005"
	@cd .. && python3 -m http.server 4005

# Clean generated files
clean:
	rm -f narration.mp3 presentation-demo.mp4 presentation-with-audio.mp4 *.webm

# Regenerate everything from scratch
regenerate: clean demo
