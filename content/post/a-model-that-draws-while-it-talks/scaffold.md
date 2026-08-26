<!-- Previous bullet scaffold. Page resource, does not render. -->


## 1. Start from the behaviour, not the model

*Describe what the thing has to do, in human terms, before you look at any architecture. That description is what rules models out later.*

- Khan at a board: talks, draws under the words, pauses. Unedited screencast, live ink, one take.
- A tutor runs three channels at once, and the drawing arrives *while* the sentence does.
- Text model: has the knowledge, no delivery. Speech model: has a voice, nothing to say. Image model: draws, off the clock, often wrong.
- Tool use stitches them together and gets decent results. What it cannot give you: the ink cannot start until the whole drawing has been decided, because a tool call is one block.
- And sync becomes a scheduler you maintain forever. Two clocks, audio playback and generation, reconciled by your code.
- The question that survives: can one model produce all three on one clock, so that sync is structural instead of scheduled.

{{< deeper "Why a page can teach you less than a person, even a very good page" >}}
Learning research has a name for the difference between reading something and doing
something with it. Chi and Wylie's ICAP framework ranks four modes of engagement by what
the learner visibly does: **Passive**, receiving and producing nothing; **Active**,
manipulating without adding anything, underlining, replaying, dragging a slider;
**Constructive**, producing something that was not in the material, explaining it to
yourself, predicting what happens next; and **Interactive**, dialogue in which both
partners build on each other. Outcomes are predicted to rank in that order, and two
things follow for anything built to teach. The jump that matters most is from Active to
Constructive, and it is cheap: asking a reader to predict what a control will do before
they touch it moves the same widget up a rung, at the cost of one sentence. And
Interactive carries a strict condition, that both sides contribute, which no article can
meet, because a page cannot respond to what you in particular got wrong. That last rung
is the entire argument for a tutor, and it is a better one than anything about speed.

**Sources:** [Chi & Wylie 2014](https://doi.org/10.1080/00461520.2014.965823) is the canonical statement of the framework · [Chi 2009](https://doi.org/10.1111/j.1756-8765.2008.01005.x) is the earlier version, before the Passive rung was added · [Freeman et al. 2014](https://www.pnas.org/doi/10.1073/pnas.1319030111) is the meta-analysis, 225 studies, for the underlying claim that engagement beats lecture · [Mayer & Moreno 2003](https://www.uky.edu/~gmswan3/544/9_ways_to_reduce_CL.pdf) for the separate finding that narration and picture presented together beat one after the other, which is the case for the whole design here
{{< /deeper >}}


## 2. How a talking model works, and which one to build on

*Audio only became modellable when someone made it discrete. And when you intend to modify a model, quality is what it does, room is what you can do to it, and the two are not correlated.*

- Say a sentence out loud. You are not reading it. You are deciding it while your mouth is already moving, and neither half waits for the other.
- Machines usually split that in two: one model settles the words, a second reads them aloud. The reader has no opinion about what was said. The writer has no idea how long it takes to say.
- You can hear the seam. A cascade cannot slow down because an idea is hard, and cannot stop when you interrupt, because the sentence was finished a second before you heard it.
- The trick that fixes it is an inner monologue: the model writes and speaks at once, the writing running a little ahead. The written stream is the thought, the spoken stream is the delivery, and the text is what keeps the audio from drifting into fluent nonsense.
- Once a model holds two channels on one clock, a third stops being strange. Thought, voice, hand.
- So the filter for a base model was never "which is the best one". It was **which one has a slot I can add to**.
- Five things were needed: open weights, a fixed frame rate, several parallel streams already, a trunk that advances one position per frame rather than flattening, and a text stream already aligned to the audio. Almost nothing has all five.

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

- One transformer position per frame. Every channel is summed into it: the audio embeddings, plus text, plus the new one, added into a single vector. The trunk runs on the sum.
- A new head reads that hidden state and predicts the next token of the new channel.
- Only the new loss is supervised. The trunk is frozen, gradients reach it only through the adapter, and the existing channels are inputs that are never trained on.
- Which means the model is never taught to do the old thing better, or at all on its own. That one choice explains most of what the finished system cannot do.
- Time moves in frames, one every 80 ms. Three things can happen in a frame: a slice of voice, a word, a piece of a drawing command. Any of them can be nothing, and nothing is the common case.
- A command is not written at once. Its tokens land one per frame, so a fifteen-token command takes fifteen frames, 1.2 seconds. You watch it being written.
- **So the grammar is the timing.** Rename a primitive and you change how long the hand takes.
- On disk it is two equal-length arrays, one token each per frame, with equality enforced in the structure itself so a corrupt row cannot be built. Same index, same moment. No timestamps, no scheduler.
- The language itself is line-oriented `key=value`, with one rule above all others: the model is not allowed to compute anything the runtime can compute.

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

- No corpus exists for the thing you are building. Building one is most of the work.
- Write the first twenty or thirty examples by hand. You are not making data yet, you are finding out what your format cannot express.
- Then generate, with a gate in front of every candidate: does it parse, is it correct, is it worth training on. Cheapest check first, so the expensive one only sees survivors.
- A gate you have not measured is not a gate. Mutate your own examples and count how many defects walk straight through. The number will be worse than you expect.
- Now the part nobody warns you about. **A corpus that looks right can teach nothing.**
- A model can only learn what varies in the data. A channel busy 97% of the time cannot teach when to stay quiet, however many examples you add.
- Ratio in the training mix beats raw count. Doubling how many scenes contained the rare construction did nothing. Repeating the same scenes eight times in the mix worked. It is not a monotone lever, though: there is a band of repetition that makes held-out loss climb again.
- There is a floor per pattern. Patterns with roughly 35 or more examples came back in free generation. Patterns with 12 never appeared once, under any other change. Worth separating the two kinds of floor: response *format* is learnable from very few examples, while *knowledge* needs orders of magnitude more.
- Consistency beats volume. Thirteen files rewritten so one element always followed another recovered a capability that a loss-function change had destroyed.
- And the counterexample, so this does not read as a promise: adding pauses to 1,471 of 1,486 scenes, tripling the measured timing signal, changed nothing. p = 0.32, bootstrap interval straight across zero. The data is where the leverage is, and most restructurings still fail.

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

- Before trusting a result, build a version of the input where you already know the answer. Plant the effect you are hoping to detect, at a strength you choose.
- If the measurement cannot see the planted effect, every negative result you have is uninterpretable rather than informative.
- **Teacher-forced loss is not evidence.** A model can post the best validation number in its lineage while producing zero of the target behaviour when it runs free.
- Measure the thing you want, in the mode you will ship, however much worse the numbers look.
- Freeze the holdout and generate it fresh rather than carving it out of training. Overlap is silent and it inflates everything downstream.
- Small evals lie. Twelve-scene gates had intervals overlapping almost every result that mattered. Compute the interval once and you will retire them.
- When you tighten a scorer, every earlier number becomes non-comparable. Re-run the old checkpoint under the new rule before claiming anything moved.
- Then say what is still broken, in the same units you used for the wins. Here: it draws when it hears words, and it does not produce words on its own.

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

{{< deeper "Two mistakes worth copying the fix for" >}}
Early on, arm means were pooled across seeds, which hid a seed spread larger than the
effect being measured. And scene-seed pairs were counted as independent when the same
scene under three seeds is not three observations.

Both were written into the results file as mistakes rather than quietly corrected. That is
the habit worth stealing: the record of what you got wrong is what makes the numbers
beside it believable.

**Sources:** [A Note on the Evaluation of Generative Models](https://arxiv.org/abs/1511.01844) for held-out loss and sample quality being largely independent, and [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) for the vivid version · [scheduled sampling](https://arxiv.org/abs/1506.03099) for the train/generate mismatch · [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640) and [Brown, Cai & DasGupta](https://projecteuclid.org/journals/statistical-science/volume-16/issue-2/Interval-Estimation-for-a-Binomial-Proportion/10.1214/ss/1009213286.full) for intervals on small evals · [Dodge et al.](https://arxiv.org/abs/2002.06305) on seed spread, and [Launch and Iterate](https://proceedings.neurips.cc/paper/2016/hash/dc5c768b5dc76a084531934b34601977-Abstract.html), which names your "same aggregates, different scenes" finding: prediction churn · [Magar & Schwartz](https://aclanthology.org/2022.acl-short.18/) on contamination · [Insights from Negative Results](https://aclanthology.org/venues/insights/) exists as a venue, which is its own argument
{{< /deeper >}}
