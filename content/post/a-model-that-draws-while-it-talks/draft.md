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
draft: true
---

## 1. Start from the behaviour, not the model

*Describe what the thing has to do, in human terms, before you look at any architecture. That description is what rules models out later.*

Watch someone explain a derivative at a board. They talk, and while they are talking a line appears under the words. Then they stop. The stop is not dead air, it is the second in which the thing they just drew is meant to land. Then they carry on. Sal Khan's early videos are the purest version of this: one take, no editing, digital ink, a voice deciding what to say while the hand is already moving.

None of that is hard to describe. It is hard to build, and it is worth describing precisely before you look at a single architecture, because the description is the thing that rules models out later. I wrote mine down before I chose anything, and every decision in this article traces back to a sentence in it.

Three things happen at once. There is a voice. There are words, which are not the same as the voice, because the words are the thought and the voice is the delivery. And there is a hand. The drawing does not follow the sentence and it does not precede it. It arrives while the sentence does.

Pull those apart and each piece is already solved. A text model has all the knowledge and no delivery. A speech model has a voice and nothing of its own to say. An image model draws, but off the clock, and often draws something that contradicts the words next to it. Each one is excellent at its third of the job.

The obvious way to assemble them is tool use: let a text model narrate, and let it call a drawing tool when it wants ink. I want to be fair about this, because it works. You can stream the tool arguments, execute drawing commands as they arrive, run a fast model, and end up with something a student would find useful. If somebody tells you they built a decent tutoring demo this way, believe them.

What tool use cannot give you is the drawing starting before the drawing has been decided. A tool call is one block. The model composes the whole figure, emits it, and only then does the renderer see anything. You can make the block arrive faster. You cannot make it arrive before it exists.

And there is a second cost that shows up later, in maintenance rather than in the demo. The moment you want the line to appear under the word that names it, you have two clocks: the audio playing back, and the model generating. Reconciling them is a scheduler, a buffer policy, a set of timestamps, and a decision about what happens when generation runs ahead or falls behind. That scheduler is code you write, and then keep writing, forever. It never becomes correct, it becomes tuned.

So the question I actually wanted to answer was not "can this be faster". It was this: can one model produce all three channels on one clock, so that synchronisation is a property of the representation instead of a thing my code maintains?

That question is what the rest of this article is about, and most of what I learned answering it had nothing to do with drawing.

## 2. How a talking model works, and which one to build on

*Audio only became modellable when someone made it discrete. And when you intend to modify a model, quality is what it does, room is what you can do to it, and the two are not correlated.*

Say a sentence out loud. You are not reading it off anything. You are deciding it while your mouth is already moving, and neither half waits for the other. If the idea gets complicated halfway through, your speech slows down to match, without you arranging that.

Machines usually split this in two. One model settles on the words, a second one reads them aloud. The reader has no opinion about what was said. The writer has no idea how long it takes to say. You can hear the seam even when both halves are excellent. A cascade cannot slow down because an idea turned out to be hard, and it cannot stop when you interrupt, because the sentence it is speaking was finished a second before you heard the beginning of it.

The design that fixes this is called an inner monologue, and it comes from Moshi. The model generates a text stream and its speech at the same time, with the text running slightly ahead of the audio it corresponds to. The written stream is the thought. The spoken stream is the delivery. The interesting part is that the text is not a transcript for your benefit. It is what keeps the audio coherent. Without it, an audio model drifts into speech that sounds completely fluent and means nothing. Moshi's own ablation puts this plainly: removing the inner monologue nearly triples the error on their benchmarks.

That result is the reason I thought this project was possible at all. Somebody had already discovered that a talking model needs a symbolic channel on the same clock in order to stay coherent. Once a model can hold two channels on one clock, a third stops being strange. Thought, voice, hand.

Which brings up the question of what to build on, and this is where I made the decision I would most like other people to steal.

I was not looking for the best open speech model. I was looking for the one with a slot I could add to. Those are different searches and they end at different models.

Five things had to be true. Open weights, because the work is adding an embedding table and an output head. A fixed frame rate, or "one token per channel per frame" means nothing at all. Several parallel streams already present, so that a new channel is a new row rather than a new mechanism. A trunk that advances one position per frame instead of flattening everything into one long sequence, because a flattened model has no position that means *now*. And a text stream already aligned to the audio, so I had a layout to copy instead of one to invent.

Almost nothing has all five. Most open speech models are a text model with speech attached: an encoder in front, a vocoder behind, a language model in the middle. There is no shared clock anywhere in that design, so there is no position for a drawing token to sit in. I would have been building the clock from scratch on a model that does not think in frames.

Underneath that first question sits a second one that decides more than model quality does: how much room does this checkpoint leave you to change it? Two models of equal ability can differ enormously in how much can be added to them for the data budget you have. Quality is what a model does. Room is what you can do to it. They are not correlated, nobody publishes the second number, and you find it out by reading the checkpoint.

{{< deeper "How a machine gets audio into tokens at all" >}}
Sound is a pressure wave, and recording it means measuring that pressure thousands of
times a second. Speech is usually sampled 16,000 or 24,000 times. So one second of voice
is twenty-four thousand numbers in a row, and every difficulty comes from that.

You can predict the numbers directly. WaveNet did in 2016 and it sounded real. It also
took minutes to produce seconds, because a second of audio is twenty-four thousand
forward passes.

You can predict something smaller. A spectrogram is a picture of which frequencies are
present over time, maybe eighty numbers every twelve milliseconds. One model draws the
picture and a second turns it back into sound. But a spectrogram is continuous: you can
regress toward it, you cannot do next-token prediction over it, and none of the machinery
built for language applies.

Or you make audio discrete. A codec learns a fixed inventory of sound fragments and
represents each slice as a few indices into it. That is the move that changed everything.
Once audio is a sequence of symbols from a fixed vocabulary, it is a language.

**Sources:** [WaveNet](https://arxiv.org/abs/1609.03499), and [Parallel WaveNet](https://arxiv.org/abs/1711.10433) for how slow it was: 172 timesteps per second against over 500,000 · [Tacotron 2](https://arxiv.org/abs/1712.05884) for the spectrogram-plus-vocoder split, and [HiFi-GAN](https://arxiv.org/abs/2010.05646) for the vocoder · [AudioLM](https://arxiv.org/abs/2209.03143) for casting audio generation as language modelling

{{< deeper "Why one index per slice is not enough" >}}
A single index cannot carry a voice. The inventory would have to hold every possible
80 ms of human sound, which is not a vocabulary, it is a memory.

So codecs quantise in layers. Encode the slice, see what the encoding got wrong, encode
that error, repeat. Each codebook corrects the residual the last one left. A frame of
audio is therefore not one token but a **column** of them, coarse at the top, finer below.

That is the real break from text. A text position holds one token. An audio position
holds a stack.

**Sources:** [SoundStream](https://arxiv.org/abs/2107.03312) introduced residual quantisation in a neural codec · [EnCodec](https://arxiv.org/abs/2210.13438) has the clearest one-paragraph definition · [DAC](https://arxiv.org/abs/2306.06546) formalises the frame-by-codebook code matrix

{{< deeper "And how you generate a stack autoregressively" >}}
Flatten it into the sequence, and a second of audio costs eight times as many positions
until the context window becomes the bottleneck.

Delay each codebook one step behind the last, and they can be predicted in parallel while
still conditioning on each other.

Or use two transformers: a large one moving across time at one position per frame, and a
small one running down the stack inside a single frame. The trunk keeps one position per
frame, which is the property everything later depends on.

These are not exclusive. Moshi uses the two-transformer design *and* a one-step delay on
the acoustic codebooks, which is where its 160 ms theoretical latency comes from.

**Sources:** [MusicGen](https://arxiv.org/abs/2306.05284) names and compares the interleaving patterns · [RQ-Transformer](https://arxiv.org/abs/2203.01941) is the temporal-plus-depth design · [Moshi](https://arxiv.org/abs/2410.00037) applies it to audio and adds the delay · [AudioLM](https://arxiv.org/abs/2209.03143) for flattening within a stage
{{< /deeper >}}
{{< /deeper >}}
{{< /deeper >}}

{{< deeper "The kinds of audio model, in one breath" >}}
By what they do: recognise speech, synthesise it, hold a conversation, generate music,
clean up or separate what is already there.

By what they predict: raw waveform, a spectrogram, or discrete codec tokens. That axis
explains more, because it decides which architectures are available at all.

By whether the audio survives the trip: a cascade runs recognition into a text model into
synthesis, and at every boundary throws away what is not words. End to end keeps audio in
the loop, so timing and emphasis can be modelled instead of discarded.

By who may speak: turn-taking models wait for you to finish, full-duplex models keep
listening and speaking at once and can be spoken over at any moment. A tutor gets
interrupted constantly, which is an argument for full duplex long before it is an argument
about speed.

**Sources:** [Whisper](https://arxiv.org/abs/2212.04356) for recognition · [Moshi](https://arxiv.org/abs/2410.00037) states the cascade's costs directly: latency of several seconds, non-linguistic information lost, and a segmentation into turns that cannot represent overlap · [dGSLM](https://aclanthology.org/2023.tacl-1.15/) is the earlier full-duplex system
{{< /deeper >}}

{{< deeper "What makes one checkpoint easier to graft onto than another" >}}
**Is it modular?** A model that keeps a separate embedding per stream and a separate head
per stream has obvious places to add a row. One that fuses everything into a single table
does not, and you end up rebuilding the input path.

**Are the input and output tables tied?** If the embedding and the output head are the
same tensor, you cannot warm-start a new head independently of a new embedding. Untied
checkpoints give you two separate places to start from.

**Warm start or cold?** A new head can be initialised by copying rows the base model
already learned for those very tokens, because pieces like `axes` and `params` are real
words it has seen. The alternative is random rows, learned from scratch, spending a data
budget you may not have.

**Does the vocabulary already reserve what you need?** Unused special tokens can be
repurposed with no vocabulary surgery. Adding new ones means new random rows again.

**Can an adapter library name the layers?** LoRA targets modules by name, and model code
that hides its projections inside a list rather than naming them individually will be
refused. This sounds trivial. It decides whether an experiment takes a day or a week.

**Does the size leave headroom?** On 128 GB of unified memory a 7B trains comfortably with
LoRA while a full fine-tune of the same model sits at the limit. That one fact decides
which experiments exist for the rest of the project.

**Sources:** [LoRA](https://arxiv.org/abs/2106.09685) and [PEFT](https://huggingface.co/docs/peft/index) · [Press & Wolf](https://arxiv.org/abs/1608.05859) on weight tying · [Hewitt on vocabulary expansion](https://www.cs.columbia.edu/~johnhew/vocab-expansion.html), and note that HuggingFace changed `resize_token_embeddings` to mean-initialise new rows by default because random ones were wrong · [Kumar et al.](https://arxiv.org/abs/2202.10054) measured frozen-trunk-plus-head against full fine-tuning: fine-tuning wins in-distribution by 2 points and loses out-of-distribution by 7 · [QLoRA](https://arxiv.org/abs/2305.14314) and [HF's memory anatomy](https://huggingface.co/docs/transformers/main/en/model_memory_anatomy) for the arithmetic

{{< deeper "Four checkpoint details that actually decided things here" >}}
The new draw head copies its rows from the text output table, which is only a real warm
start because that table is a separate tensor rather than a second view of the input
embedding.

The four grid tokens sit at ids the base model already reserves, byte for byte, so the
format needed no vocabulary surgery.

LoRA had to target `in_projs.0` rather than `in_projs`, because the bare name reaches a
list of modules and the adapter library refuses it.

And from the other direction: on one popular tokenizer the id for "this row is short" is
the same integer as the id for "this channel is silent this frame", 151643. That single
collision silently deleted 65% of a training loss mask.

**Sources:** [PEFT matches module names by dotted suffix and rejects anything that is not a supported leaf layer](https://github.com/huggingface/peft/blob/5d602fdbff04c33c1c4de55cda9d4ae1d7cb7e40/src/peft/tuners/lora/model.py#L454) · [`tie_word_embeddings`](https://github.com/huggingface/transformers/blob/v4.44.2/src/transformers/configuration_utils.py#L227)
{{< /deeper >}}
{{< /deeper >}}

{{< deeper "The alternatives, and why each one fails" >}}
**The adapter family**, a text model with a speech encoder and a vocoder bolted on, has no
frame grid at all. You would be building the clock from scratch on a model that does not
think in frames.

**The omni family** is the interesting near-miss: open weights, genuinely multimodal, and
moving away from this design rather than toward it. Successive versions argued in print
that dropping word-level timestamp alignment simplifies training, removed text
representations from the speech decoder, and added machinery specifically to avoid fixed
interleaving rates.

**Closed models** rule themselves out. You cannot add a head to weights you do not have.

**A different codec** breaks the arithmetic rather than the architecture. The 24 kHz
configurations of the common codecs run at 50 to 86 frames a second against this one's
12.5, and EnCodec's 48 kHz stereo model runs at 150. Six times the frames is six times
the data and six times the decode, which the hardware does not have.

**Sources:** [DAC](https://arxiv.org/abs/2306.06546) Table 1 compares the frame rates directly · [Qwen2.5-Omni](https://arxiv.org/abs/2503.20215), [Qwen3-Omni](https://arxiv.org/abs/2509.17765) and [Qwen3.5-Omni](https://arxiv.org/abs/2604.15804) are the three steps of the omni argument
{{< /deeper >}}

## 3. Adding an ability, and designing what it emits

*Freeze what already works, add the smallest possible new part, warm-start it from what the model already knows. Then remember that when position in the sequence is time, your syntax is your timing.*

The mechanical part is smaller than it sounds. There is one transformer position per frame, and every channel is summed into it. The audio embeddings, plus the text embedding, plus the new drawing embedding, added into a single vector. The trunk runs on that sum. A new output head reads the resulting hidden state and predicts the next token of the new channel.

That is the whole graft. Nineteen million trainable parameters against a seven billion parameter trunk.

Three choices in there are worth pulling out, because they generalise to any capability you want to add to a model somebody else trained.

Freeze everything that already works. In my case every trunk parameter has gradients disabled, and what gradients do reach the trunk arrive through a small adapter. The voice cannot degrade, not because I was careful but because there is no path by which it could.

Warm-start the new part from what the model already knows. My drawing language is made of pieces like `axes` and `params`, which are real words the base model has seen thousands of times. So the new embedding table is not random, it is copied row by row from the text tables. Random rows have to be learned from scratch, and that spends a data budget I did not have. This is not a clever trick, it is the default now: HuggingFace changed how new token embeddings are initialised because the naive version was wrong.

And supervise only the new thing. My loss is the drawing loss and nothing else. Text and audio are inputs the model reads and is never scored on.

That last decision is the one I want you to hold on to, because it explains almost everything the finished system cannot do. A model that is never taught to talk does not learn to talk. Four hundred frames of free generation produced zero drawing commands. Four hundred frames of forced narration produced a real scene. The system draws when it hears words, and it does not produce words on its own. That is not a mysterious failure. It is the architecture doing exactly what I told it to.

Now the part I find more interesting, which is what the new channel actually emits.

Time moves in frames, one every 80 milliseconds, twelve and a half of them a second. Three things can happen inside a frame: a slice of voice, a word, a piece of a drawing command. Any of them can be nothing, and nothing is the common case. Silence on the drawing channel is not the absence of data. It is what makes the pause before a figure land.

A command is not written all at once. Its tokens arrive one per frame, so a fifteen-token command occupies fifteen frames, which is 1.2 seconds. You watch it being written, the way you watch a hand.

Which produces the consequence I did not see coming and have thought about ever since. **The grammar is the timing.** Rename a primitive from four characters to eight and the hand takes longer to draw it. Add an optional attribute and every command carrying it slows down. There is no separate place where pacing is configured, because the syntax already decided it. I have never worked on anything else where the language design and the animation timing were the same decision.

On disk a scene is two equal-length arrays, one token each per frame, with the equality enforced by the structure itself so that a malformed row cannot be constructed. Same index means the same moment. No timestamps, no scheduler, nothing to reconcile. That is the whole payoff for all the architectural work: synchronisation stopped being something my code maintains.

The drawing language itself is line-oriented `key=value` text with one rule above all others: the model is not allowed to compute anything the runtime can compute. Every time I was tempted to let the model emit a coordinate, a length, or a slope, that was a place where it could be confidently wrong and nothing would catch it. Push the arithmetic into the renderer and the model's job shrinks to the part it is good at, which is deciding what to draw and when.

{{< deeper "Why summing, and not two positions per frame" >}}
The obvious alternative is to flatten each frame into `[say_t, draw_t]`, two positions,
and let attention sort it out. Measured: 0 of 7 scenes exact, 7 of 7 fail. Summing is what
keeps position equal to time.

The new tables are row-indexed from the text tables, never random. That, plus a dense new
vocabulary of a few hundred pieces instead of the full 32,000, keeps the head at ~2M
parameters instead of 262M.

Worth being accurate about credit: summing parallel streams into one position is how
these models already work, not a choice made here. The new channel simply joins the sum.

One detail that cost an afternoon: the summation order is audio, then text, then draw.
Floating-point addition is not associative at any width, and bf16's eight mantissa bits
make it bite sooner. Text-first failed the equivalence check against the real model.

**Sources:** [RQ-Transformer](https://arxiv.org/abs/2203.01941) states the summation as an equation · [Moshi's `lm.py`](https://github.com/kyutai-labs/moshi/blob/e6a55d2722a65870ef52a6c9f6ecfc0e90f38362/moshi/moshi/models/lm.py#L389) and [AudioCraft's](https://github.com/facebookresearch/audiocraft/blob/896ec7c47f5e5d1e5aa1e4b260c4405328bf009d/audiocraft/models/lm.py#L244) do it in code · [Goldberg 1991](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) and [NVIDIA's floating-point guide](https://docs.nvidia.com/cuda/floating-point/index.html) for non-associativity
{{< /deeper >}}

{{< deeper "The four tokens that carry timing, and the trap underneath them" >}}
Silent this frame. Inside a block, past its tokens. A one-frame commit signal written
immediately before a block's first token. And the terminator, which sits on the frame
*after* the block's last token, not on its last frame.

The expensive part: "silent this frame" is **content**. It means the channel has nothing
to do right now. Every mainstream collator reads its pad id as the opposite, "this row is
short, ignore the tail".

Two scenes through a stock collator masked 366 label positions where the true row padding
was 128. That is 238 content tokens silently dropped, 65% of the mask. A model trained
through it is never taught to stay quiet, which is most of what this format teaches.

Fixed three ways, the last being an assertion that counts label coverage every batch. A
collator that eats them still converges and still reports a believable loss. Only counting
sees it.

**Sources:** the whole bug is [one line](https://github.com/huggingface/transformers/blob/v4.44.2/src/transformers/data/data_collator.py#L823), `labels[labels == self.tokenizer.pad_token_id] = -100`, which is a value comparison and not a position comparison · [issue #23530](https://github.com/huggingface/transformers/issues/23530) reports exactly this failure · [`CrossEntropyLoss`](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) explains why removal is silent: ignored positions leave both the numerator and the denominator · the layout itself follows [Moshi's Inner Monologue](https://arxiv.org/abs/2410.00037)
{{< /deeper >}}

{{< deeper "Designing a language a model can actually learn" >}}
No JSON: braces demand lookahead to know a value has ended, and quotes waste tokens.

The admission rule for a primitive is one hand gesture, one primitive.

Two constraints pull against each other. Being extractable from a screencast pulls the
design *down* toward raw ink. Being learnable pulls it *up*, away from arithmetic.
Mid-level is where they meet.

It has to be prefix-parsable, because the client renders as tokens arrive: every command
must run the moment it closes, with no lookahead. And anchored rather than absolute,
because streaming means you do not know the final composition when you place the first
object.

There is an escape hatch: ink that cannot be classified degrades to a raw polyline instead
of being thrown away. The fraction of a corpus that stays at that level is the language's
own design metric. High means the primitives are wrong.
{{< /deeper >}}

## 4. The data is the program

*Weighting the loss argues with the output. Restructuring the corpus edits the program. Most engineers reach for the first one.*

No corpus exists for the thing you are building. That is normal, and building one turns out to be most of the work.

Start by writing twenty or thirty examples by hand. This feels like a waste of a week and it is not, because you are not making data yet. You are finding out what your format cannot express. Every awkward example is a hole in the language, and it is much cheaper to find those holes with your own hands than to find them in a training run six weeks later.

Then generate, and put a gate in front of every candidate. Mine runs cheapest check first: does it parse, is the geometry correct, is it worth training on, and only then the expensive semantic check. Ordering the gates by cost means the expensive one only ever sees survivors.

And then measure your gates, which is the step almost everybody skips including me. A gate you have not measured is not a gate, it is a feeling. Take your own examples, mutate them into things you know are wrong, and count how many walk straight through. The number will be worse than you expect. I know mine is bad; I also know I no longer have the files that measured it, which is its own lesson about writing down how you got a number.

That is the mechanical half. Here is the half nobody warns you about.

**A corpus that looks right can teach nothing.**

A model can only learn what varies in the data. My drawing channel was busy 97% of the time, because when you author scenes by hand you author interesting ones, and an interesting scene is one where things are happening. So there was almost no silence in the corpus, and I then spent weeks trying to teach a model when to stay quiet. No quantity of additional examples was going to fix that. The behaviour I wanted to teach was not present in the material.

Ratio in the training mix beats raw count. Doubling the proportion of scenes containing a rare construction, from two percent to four, did nothing whatsoever. Repeating the same scenes eight times in the mix worked. Those sound like the same intervention and they are not: the first added examples, the second changed how often the model saw the pattern relative to everything else. It is not a monotone lever either, there is a band of repetition where held-out loss starts climbing again.

There is a floor per pattern, and it is sharper than I expected. Patterns with roughly 35 or more examples came back in free generation. Patterns with 12 examples never appeared once, no matter what else I changed. Below the floor the model does not do the thing badly. It does not do the thing. Worth separating the two kinds of floor, because they are orders of magnitude apart: response format is learnable from very few examples, while knowledge needs vastly more.

Consistency beats volume. The clearest result I got all project came from rewriting thirteen files.

And then the counterexample, because I do not want this to read as a promise. I once restructured 1,471 of 1,486 scenes to add pauses, which tripled the timing signal I could measure in the data. The effect on the model was nothing. p = 0.32, bootstrap interval straight across zero, and the three seeds disagreed on the sign. The data is where the leverage is, and most restructurings still fail. Both halves of that sentence are the lesson.

Why does this go against a software engineer's instincts? Because we are trained to treat data as the fixed input and code as the thing you change. When something is wrong you reach for the loss function, the learning rate, the architecture. But in training, the data is the program. Weighting the loss is arguing with the program's output. Restructuring the corpus is editing the program. I reached for the loss first, every single time, and it did not work once.

{{< deeper "The same goal, attacked twice: once in code, once in data" >}}
The model would not write the equation on the board.

**The engineer's fix.** Weight those tokens six times harder in the loss. Result: 5 of 48
against a bar of 21, and the diagnosis was that weighting taught the model to memorise its
training onsets rather than generalise the rule. On held-out sites, rank-0 accuracy halved
from 18 to 10. In its failures the top pick was the *other* command, at probabilities
around 0.85 to 0.99. It had learned the wrong thing, confidently.

**The data fix.** Turn the weighting off. Rewrite thirteen scenes so the equation always
comes immediately after the curve, matching what 118 of the other 132 already did. Result:
23 of 48, and 49 of 100 on held-out templates, up from 15.

Same objective, two levers. Thirteen files beat a loss function.

One honest qualification. The literature does not say that token weighting causes
memorisation; it says weighting is a weaker lever than people expect, and that narrowing
the loss to output tokens *increases* overfitting rather than reducing it. The diagnosis
above is what happened in this run. The transferable claim is the weaker, better-supported
one: the loss is not where the leverage is.

**Sources:** [Shi et al.](https://arxiv.org/abs/2405.14394) on loss over instructions · [Byrd & Lipton](https://proceedings.mlr.press/v97/byrd19a.html) on importance weighting washing out · [Exploring Format Consistency for Instruction Tuning](https://arxiv.org/abs/2307.15504) is the published version of the thirteen-files result, and [the Flan Collection](https://proceedings.mlr.press/v202/longpre23a.html) is its counterweight: deliberate variation beats consistency where you want a general behaviour
{{< /deeper >}}

{{< deeper "The bigger version of the same lesson" >}}
Same trunk, same 2,578 training rows, same hyperparameters.

One run tried to fix behaviour inside the training procedure, mixing the model's own
predictions into its inputs at the moments that mattered. It got worse, and the mechanism
is worth understanding: at those moments the model's own pick was usually "stay silent",
the label still said "start drawing", so it learned *you were silent here and the command
started anyway*. It became more silent. Verdict: stop.

The other run changed nothing but the corpus, so that the narration announces the ink
before it appears. Zero to 43 of 48 on the target construction, and 64 of 100 drawing on
the control sets every previous run had failed.

The capability was there the whole time. The data was not carrying it.

**Sources:** [Chan et al.](https://arxiv.org/abs/2205.05055) is the closest thing to this article's thesis as a paper: a capability appears or fails to appear from distributional properties alone, architecture and objective fixed · [Udandarao et al.](https://arxiv.org/abs/2404.04125) and [Kandpal et al.](https://proceedings.mlr.press/v202/kandpal23a.html) on performance tracking concept frequency · [GPT-3](https://arxiv.org/abs/2005.14165) Table 2.2 for ratio over count: Wikipedia is 137x smaller than Common Crawl and seen roughly 8x more often · [DoReMi](https://arxiv.org/abs/2305.10429) on mixture proportions · [Kandpal et al. 2022](https://proceedings.mlr.press/v162/kandpal22a.html) for the threshold: ten copies makes a sequence a thousand times more likely to be generated · [LIMA](https://arxiv.org/abs/2305.11206) for format being cheap to teach · [Hernandez et al.](https://arxiv.org/abs/2205.10487) for the repetition ceiling
{{< /deeper >}}

## 5. Knowing whether it worked, and what is still broken

*Build a control you know the answer to before you trust an experiment. A measurement that cannot detect a planted effect cannot detect a real one.*

The single most useful thing I did on this project was also the one that told me my main hypothesis was not supported.

I wanted to know whether the model learns *when* to draw, or only *what* to draw. That is the difference between a tutor and a very fast illustrator, so it mattered. I built a measurement for it, ran it, and got a small positive number that was not statistically significant.

At that point I had two possible conclusions and no way to choose between them. Either timing is not being learned, or my measurement cannot see timing. Those are very different situations, and the number looks identical in both.

So before trusting the result I rebuilt the corpus with the effect planted in it, at a strength I chose, and checked that the measurement could find something I knew was there. It could. Then I ran the real corpus and it found nothing, and because of the planted runs I could call that an answer rather than an ambiguity. Without them I would have had a number I could read either way, and I would probably have read it the way I wanted to.

Everything else in this section is smaller than that, and each one still cost me something.

{{< deeper "What a control actually looks like" >}}
The question was whether the model learns *when* to act, or only *what* to emit.

The test: take each scene, shuffle the thing that should carry the timing, and see whether
the model is more surprised by the shuffled version than the real one. If timing carries
no information, shuffling costs nothing.

The trap is that this only means something if the test can detect timing when timing is
definitely there. So the same corpus was rebuilt with an artificial timing marker planted
at three strengths: none, weak, strong. Strong separated at p = 0.0000, weak at p = 0.001,
none did not separate. The instrument reads.

Then the real corpus: +0.079, p = 0.18, roughly a third of the smallest effect the
instrument had been shown to detect. Not a failed experiment. An answer.

A note on the name: "positive control" is borrowed from experimental science. Machine
learning does the same thing under other names, canaries and sanity checks, so the idea is
well established even though the phrase is not native.

**Sources:** [The Secret Sharer](https://arxiv.org/abs/1802.08232) plants canaries at known frequency and asks whether the metric sees them, which is this design exactly · [Sanity Checks for Saliency Maps](https://arxiv.org/abs/1810.03292) destroys the signal and shows the method reporting it anyway · [With Little Power Comes Great Responsibility](https://aclanthology.org/2020.emnlp-main.745/) on why underpowered experiments produce uninterpretable negatives
{{< /deeper >}}

**Teacher-forced loss is not evidence.** One of my checkpoints posted the best validation loss in its entire lineage while producing zero of the target behaviour on every evaluation set. I wrote "this decides nothing" next to that number four separate times in my own notes, which tells you how strong the pull is to believe a good number. Measure the thing you want, in the mode you will actually run, however much worse the numbers look.

**Freeze the holdout, and generate it fresh rather than carving it out of training.** Overlap is silent, and it inflates everything downstream of it in a way you will not notice.

**Small evaluation sets lie.** I ran twelve-scene gates for several generations before computing a confidence interval on one. The intervals overlapped almost every result I had been making decisions from. I retired those gates as ship criteria the same day. Two seeds of the identical recipe agreed on the aggregates and disagreed on roughly a third of the individual scenes, which is a known phenomenon and still a shock to see in your own runs.

**When you tighten a scorer, every earlier number becomes non-comparable.** I made a scoring rule stricter, correctly, and quietly invalidated a table of results I had been reasoning from. Re-run the old checkpoint under the new rule before claiming anything moved.

{{< deeper "Two mistakes worth copying the fix for" >}}
Early on, arm means were pooled across seeds, which hid a seed spread larger than the
effect being measured. And scene-seed pairs were counted as independent when the same
scene under three seeds is not three observations.

Both were written into the results file as mistakes rather than quietly corrected. That is
the habit worth stealing: the record of what you got wrong is what makes the numbers
beside it believable.

**Sources:** [A Note on the Evaluation of Generative Models](https://arxiv.org/abs/1511.01844) for held-out loss and sample quality being largely independent, and [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) for the vivid version · [scheduled sampling](https://arxiv.org/abs/1506.03099) for the train/generate mismatch · [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640) and [Brown, Cai & DasGupta](https://projecteuclid.org/journals/statistical-science/volume-16/issue-2/Interval-Estimation-for-a-Binomial-Proportion/10.1214/ss/1009213286.full) for intervals on small evals · [Dodge et al.](https://arxiv.org/abs/2002.06305) on seed spread, and [Launch and Iterate](https://proceedings.neurips.cc/paper/2016/hash/dc5c768b5dc76a084531934b34601977-Abstract.html), which names the "same aggregates, different scenes" finding: prediction churn · [Magar & Schwartz](https://aclanthology.org/2022.acl-short.18/) on contamination · [Insights from Negative Results](https://aclanthology.org/venues/insights/) exists as a venue, which is its own argument
{{< /deeper >}}

And then say what is still broken, in the same units you used for the wins. So: the drawing channel works. Given narration, it draws things that are geometrically correct, in time with the words, at a rate that would keep up with a person. The best run went from zero to 43 of 48 on the construction I had been chasing for six generations.

It also draws only when it hears words. It does not produce words on its own. Every number in this article was measured with the narration forced. The half of the system that would make it a tutor rather than an illustrator is the half I have not built, and I know exactly which architectural decision put it there: I supervised only the drawing loss, so the model was never taught to talk.

There is a version of this write-up where that last paragraph does not appear and the article is more impressive. It would also be useless to anybody trying to do this themselves, which is the only reason to write it down.

Stay curious ☕
