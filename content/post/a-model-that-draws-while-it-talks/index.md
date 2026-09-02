---
title: "ChalkBoard - A tutoring model"
date: 2026-08-24T08:00:00+02:00
description: ""
keywords:
    - chalkboard
    - moshi
    - frame-aligned generation
    - interleaved token streams
    - dsl
    - rlvr
    - verifier as reward
    - dgx spark
    - lora
tags:
    - ai
    - ml
    - training
# Reachable by URL, listed nowhere: not in the blog index, the sitemap or the
# feed, and asking search engines to stay out.
noindex: true
build:
  list: never
  render: always
width: wide
---

{{< chalkboard-header >}}

Learning and explaining complex concepts have gotten way cheaper and easier using LLMs. Is not just text or audio. You can get personalized, interactive demos that are tailored to your level of understanding, are fun and {{< pencil "icap" >}}accelerate learning{{< /pencil >}}.

{{< deeper "How people actually learn" "icap" >}}
There is a big difference between **reading** something and **doing** something with it. Chi and Wylie's ICAP framework ranks four learning modes and predicts outcomes in that order:

**Passive.** You receive information and produce nothing: read or watch a video.

**Active.** You manipulate it without adding anything: drag a slider or underline a line.

**Constructive.** You produce something that was not there: explain it back, predict what happens next.

**Interactive.** A dialogue where both sides build on each other.

Using LLMs, you can improve from <mark>Passive to Active by generating interactive widgets</mark>, fidgetable elements.
Moving from Active to Constructive can be done by allowing someone to predict what a slider will do <u>BEFORE</u> they move it.

Where a model gets interesting is when it starts ask you question, notice what you got wrong, generates fidgetable elements and push just past what you already know. That's the <u>Interactive</u> mode.

**Sources:** [Chi & Wylie 2014](https://files.eric.ed.gov/fulltext/EJ1044018.pdf) is the framework, free full text. The underlying claim rests on [Freeman et al. 2014](https://www.pnas.org/doi/10.1073/pnas.1319030111), a meta-analysis over 225 studies comparing engagement against lecture. For predict-then-reveal specifically, see [Kim, Reinecke & Hullman 2017](https://doi.org/10.1145/3025453.3025592).
{{< /deeper >}}

Go and test it if you didn't had the chance. Just prompt your favorite frontier model, ask it to explain how derivatives work and to {{< note text="generate HTML and JS" >}}. You get to "play" with the elements, vizualize how a function accelerate or deccelerate in a given point, instead of just reading out an explanation. Also, detecting a wrong explanation is harder than detecting a wrong vizualization.{{< /note >}} with interactive elements and you will get a pretty fun learning exercise.

But still, it doesn't feel like a tutor, {{< note text="like a teacher" >}}In 1984 Bloom measured how much better one tutor does than a classroom. Students taught one to one, with mastery checks along the way, ended up about two standard deviations above the same material taught to a class. His question was how to get a class near that number, since one tutor per child is not a thing anyone can pay for.

Later work has not reproduced a gap that large, though what produces it still holds. A tutor watches you work and changes what comes next according to the specific thing you have wrong. No amount of quality in the explanation gets you that, because the explanation was written before you started.

**Source:** [Bloom 1984](https://doi.org/10.3102/0013189X013006004).{{< /note >}}. If you want to get the full experience, you need to know how to combine certain prompts with certain tools for text-to-speech and text-to-image.

You need to do an entire dance of prompting and tool use, but there should be a better way. Look at Khan Academy or {{< note text="3Blue1Brown" >}}Those animations are Python. Sanderson wrote Manim to make them, so each picture is the output of a program rather than a drawing someone made by hand.

That is the same shape as what a model like this has to produce. The output is instructions rather than pixels, and something else turns them into the picture. The people who explain best on video had already reduced their drawing to code, which means there is less for the model to invent.{{< /note >}}. It feels more natural, easier to follow and understand if somebody is {{< arrow "together" >}}speaking to you while they draw on a board{{< /arrow >}} and correlate it with their speech and their drawing.

{{< deeper "Why saying it while drawing it works" "together" >}}
Richard Mayer's group has spent decades measuring what happens when the words and the picture reach you at different times. <mark>The narration and the picture it describes have to arrive together.</mark> If you split them, you spend your effort holding the first half in your head while you wait for the second.

His second result rules out subtitles. If the words are printed next to the drawing, you have to look away from it to read them, and you miss the stroke you were watching. If you **hear** them instead, your eyes never leave the picture.

That is why Khan Academy and 3Blue1Brown are easy to follow. One hand draws <u>while one voice explains</u>, and you never have to look in two places.

**Source:** [Mayer & Moreno 2003](https://www.uky.edu/~gmswan3/544/9_ways_to_reduce_CL.pdf), nine ways to reduce cognitive load, for both the timing and the spoken-over-printed findings.
{{< /deeper >}}

## One model to rule them all

This correlation between speech and drawing, speech-to-draw, is hard to get it right using {{< pencil "toolcalls" >}}other techniques{{< /pencil >}}.

{{< deeper "Why tool calls drift" "toolcalls" >}}
One such technique is **tool-use**. You can have a frontier model acting like a tutor model that can output both voice and text. Inside the text output, you can have different tool calls that a client can interpret and draw.

You can define different shapes as tools or use existing drawing libraries and expose their API as tools to the frontier model.

Now, this approach can work most of the time, but you will end up with different **synchronization problems**: narration can go faster or slower than the drawing.
You'll have to account for this in client's implementation, use some heuristics for them, or hint the frontier model to do so.

The API confirms the shape of the problem. A realtime session with both modalities on "will respond with both audio and text content", and a tool call arrives as its own output item, `type: "function_call"`:

```
response.output_audio.delta              the voice
response.output_audio_transcript.delta   the words being said
response.function_call_arguments.delta   draw_line({ ... })
```

Three independent streams, and nothing in the protocol says where in the audio that `draw_line` belongs. <mark>There is no field for it, because there is no shared clock.</mark> Lining them up is the client's job, <u>forever</u>.

**Reference:** [OpenAI Realtime conversations](https://developers.openai.com/api/docs/guides/realtime-conversations)
{{< /deeper >}}

If you think about it, when you start to explain and draw something, you already have an inner monologue that usually is {{< arrow "ahead" "right" >}}a little bit ahead of your drawing and speech{{< /arrow >}}.

{{< deeper "The hand starts before the word" "ahead" >}}
Morrel-Samuels and Krauss filmed it, so this is more than something you notice about yourself.

They sat people in front of photographs and filmed them describing what they saw. A second group watched the tape afterwards and marked, for every movement of the hand, which word it went with. That left two moments to compare for each gesture: when the hand set off, and when the word was said. <mark>Your hand starts before your voice does.</mark>

How big the gap is depends on the word: **familiarity predicts it**. A word you know well leaves a short gap, and one you have to search for leaves a long one, so the gap measures how long the word took to find.

Nobody can film a monologue, so what they caught is the hand running ahead of the voice, not a thought running ahead of both. The second result is what connects the two. If the gap grows exactly when the word is hard to find, then at the moment the hand set off, the sentence had been decided and the word had not.

**Source:** [Morrel-Samuels & Krauss 1992](https://doi.org/10.1037/0278-7393.18.3.615). The earlier version of the same work is titled, plainly, <u>Gestures precede speech</u>.
{{< /deeper >}}

Now how can we translate something like that to a model?

You put everything on one clock. The sound gets cut into equal slices, {{< note text="one clock" >}}The clock is not free. At every position the model emits every stream it carries, whether or not that stream has anything to say. Silence costs a token, exactly like a word does.

You get alignment, which nothing else gives you. In exchange, every frame where a stream has nothing to say still costs you one token, for as long as the model runs.{{< /note >}}, about twelve of them a second. The words go on the slices they start in. One position in the sequence means one moment in time, and it means that for both of them at once.

{{< fold "Where that clock comes from" "4 min" >}}

Inside a text LLM, a token doesn't have the concept of duration. The only relationship between tokens is that one token come after another, in a sequence.
What adds this dimension of time is the audio codec. You can't tokenize sound, without deciding how much sound one token covers. The codec chops the waveform
into slices and maps each slice to a symbol. Mimi chops 12.5 slices per second, creating tokens that cover 80 milliseconds.

There are {{< pencil "codecs" >}} more granular codecs{{< /pencil >}} out there, with different upsides and downsides.

{{< deeper "Codecs Frequency" "codecs" >}}
The frequency you chop the waveform at decides everything that comes after it.

The rate depends on the codec and on how it is set up.

| Codec | Frames a second |
| --- | --- |
| EnCodec | 75 on 24kHz audio, 150 on 48kHz stereo |
| DAC | 86 |
| SoundStream | 50 or 75, depending on the sample rate it was built for |
| **Mimi** | **12.5** |

<mark>At 12.5 frames a second the model has 80 milliseconds to produce each position. At 86 it has 11.</mark> Eleven milliseconds is out of reach on hardware you can afford, and no amount of engineering around it changes that.

A low rate costs you precision. A frame is the <u>smallest thing you can point at</u>, so at 12.5 a second you can't place a word closer than 80 milliseconds and everything rounds to the nearest frame. A faster codec would let you line things up more finely, if you could afford to generate it.

A low rate also means every token has to carry more sound. Mimi uses 8 {{< note text="codebooks" >}}Eight learned tables, and the order of them matters. The first one picks the closest match it has to the frame, which is rough. Every table after it stores what the ones before it still got wrong.

So the eight are unequal shares of the sound. Most of the meaning sits in the first one or two, which is why you can drop the last few and still make out the speech, at some cost to how it sounds.{{< /note >}} per frame, 2048 entries each, and fits a second of speech into about 1.1 kilobits.

**Reference:** [Mimi is introduced inside the Moshi paper](https://arxiv.org/abs/2410.00037), section 3.3. [EnCodec](https://arxiv.org/abs/2210.13438), [DAC](https://arxiv.org/abs/2306.06546) and [SoundStream](https://arxiv.org/abs/2107.03312) for the rest.
{{< /deeper >}}

These tokens come out one after another, 12.5 of them every second. Position 13 is always 1.04 seconds in. The position now tells you when, on top of telling you what came first.

Anything else you want lined up with the audio has to sit on those same positions. The words are what we want lined up with it. Words don't come with positions though, {{< arrow "times" >}}they come with start times{{< /arrow >}}. So you divide the start time by the frame rate. A word that starts at 1.04 seconds goes on frame 13.

{{< deeper "Where the start times come from" "times" >}}
A transcript gives you the words in order and nothing about when each one starts.

**Forced alignment** gives you the times: you take audio you already have the words for, and work out where each one sits. Whisper is the usual tool for it. Out of the box it timestamps a segment at a time, a sentence or so; <mark>word-level times come from reading its attention, which is what the `word_timestamps` option does</mark>, or from running a separate aligner over the pair.

<u>The times are the whole dataset.</u> If you get them wrong by two frames, you have taught the model to speak slightly after it writes.

**Sources:** [Whisper](https://arxiv.org/abs/2212.04356) for the recogniser. [Moshi](https://arxiv.org/abs/2410.00037), section 3.4.4, for what it does with the alignment once it has it.
{{< /deeper >}}

But there is a slot for every tick, and words don't fill every slot. The empty ones still need a token. That token means "silent here". Most of what the model has to learn is when to stay quiet.

{{< align >}}

Now the text ticks at the same rate as the audio. That is what {{< note text="Moshi" >}}Kyutai's speech model, 2024. Unusually, it does not take turns: it models both sides of the conversation at once, its own voice and yours, and keeps generating while you are still talking.

That is what the shared clock is for. Turn-taking is a rule you have to impose on a system that can only attend to one thing at a time. If both sides are on one clock, the model can be interrupted, because it never stopped listening.{{< /note >}} calls the {{< pencil "monologue" >}}inner monologue{{< /pencil >}}.

{{< deeper "What the inner monologue is for" "monologue" >}}
<mark>The text stream is a plan that the voice follows</mark>, rather than a transcript for you to read.

An audio model on its own **drifts**. It generates something that sounds like speech but doesn't mean anything. The text stream stops the drift. Moshi's own words: modelling the text of its own speech gives "a scaffolding that increases the linguistic quality of its generation".

They measured it by taking the text stream away. Without it the scores drop to <u>about a third</u>.

This is Moshi's technique rather than common practice. Most speech models don't have a text stream at all. Qwen's models went the other way on purpose, and said that dropping this alignment makes training simpler.

**Reference:** [Moshi](https://arxiv.org/abs/2410.00037), section 3.4.4.
{{< /deeper >}}

Now two tokens need the same position. On frame 13 there is a text token and an audio token. The model has to take both.

This doesn't need a different kind of transformer. A transformer doesn't work with tokens directly. Every token becomes a vector first, and that vector is built before the model sees it. You are {{< arrow "summing" >}}already building it out of more than one thing{{< /arrow >}}.

{{< deeper "One position, several embeddings" "summing" >}}
In {{< note text="nanoGPT" >}}Karpathy's teaching implementation of GPT-2, about three hundred lines. Everybody reads it first because nothing hides behind a library call: the forward pass **is** the architecture.

If what a transformer reads at each position is a sum, then adding a stream is one more thing to add, and none of the parts underneath have to change.{{< /note >}}, the input to the first block is this:

```python
tok_emb = self.transformer.wte(idx)   # what the token is
pos_emb = self.transformer.wpe(pos)   # where it sits
x = tok_emb + pos_emb
```

That row is already two embeddings added together. <mark>Adding more of them is the same operation carried further.</mark>

Moshi adds **seventeen**: one for the text, then eight for each voice, its own and yours. Its code does it in a loop, adding each audio codebook and then the text, before anything reaches the transformer.

Getting them back out works the same way <u>in reverse</u>. The model produces one output per position, and every stream has its own small head that reads its part out of it.
{{< /deeper >}}

{{< endfold >}}

Once two streams share that clock, a third one {{< note text="costs almost nothing" >}}Inside the model, near enough nothing. The stream needs an embedding table on the way in and a head on the way out, and both are tiny next to the transformer they hang off.

The hard part is the data. Every example you train on now needs that third stream, aligned to the same frames as the other two, and there is nothing you can download that has it. You record it or you generate it. The cost of building that data is why a third stream is rare.{{< /note >}}. {{< arrow "others" >}}The model doesn't care what is in it{{< /arrow >}}. Somebody already put facial motion on that clock. Somebody else put robot actions on it.

{{< deeper "What else people have put on it" "others" >}}
**RT-2** puts robot actions into the sequence by writing them as text. Its own words: to fit language and actions into one format, it expresses <mark>the actions as text tokens, in the same training set as the language.</mark> One model reads the instruction and moves the arm.

**Audio to Photoreal Embodiment** does it with people. If you give it the speech from a conversation, it produces the body that goes with it, face and hands included, quantised into a codebook the way audio is, so the motion lands on the same timeline as the sound that caused it.

Neither is doing anything the drawing stream will not. <u>The stream will hold any kind of token.</u>

**Sources:** [RT-2](https://arxiv.org/abs/2307.15818) and [From Audio to Photoreal Embodiment](https://arxiv.org/abs/2401.01885).
{{< /deeper >}}

We put drawing commands on it.

{{< heads >}}
