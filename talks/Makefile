# Auto-discover talks (each subfolder with a .md file)
TALKS := $(patsubst %/,%,$(dir $(wildcard */*.md)))

.PHONY: all clean serve $(TALKS)

all: $(TALKS)

$(TALKS):
	@echo "Building $@..."
	npx @marp-team/marp-cli --html --allow-local-files $@/$@.md -o $@/$@.html
	node inject-backdrop.js $@/$@.html
	mkdir -p ../static/talks/$@
	cp $@/$@.html ../static/talks/$@/index.html
	cp waves.mp4 ../static/talks/$@/
	-cp $@/*.png ../static/talks/$@/ 2>/dev/null
	-cp $@/*.gif ../static/talks/$@/ 2>/dev/null
	-cp $@/*.jpg ../static/talks/$@/ 2>/dev/null
	@echo "Built $@ -> static/talks/$@/index.html"

clean:
	rm -f */*.html
	rm -rf ../static/talks

serve:
	python3 -m http.server 4005
