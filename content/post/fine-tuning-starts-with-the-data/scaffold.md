<!-- Bullet scaffold. Page resource, does not render. Every bbm number is from a results doc in the bbm repo, named in brackets so it can be checked before it goes into prose. -->


## 0. What this is

*Over forty training runs on one DGX Spark, on three models, for a model that talks and draws at the same time. The order below is the one I would follow now, and each step names the run that taught it.*

- Three model families: a 2B text model (helium, runs gen2 to gen13), a 7B speech model with a drawing head grafted on (moshi, moshi1 to moshi22), a 12B LLM with a LoRA adapter that writes training data (gemma, lora1 to lora8).
- Almost every change that moved a model was a change to the data, and almost every wrong call I made came from reading an eval that could not see what I thought it saw.
- So the article starts with data, and the eval is the first piece of data you build.
- Not covered: pretraining, RL beyond rejection sampling, anything multi-GPU.


## 1. Write down what the model will be asked, before you make any data

*Your training example has to look exactly like the moment the model is used. Every difference between the two trains a slightly different model from the one you run.*

- The training row and the live prompt are built by two different pieces of code, and they drift apart without anyone noticing.
- `dlg-run44`: the live teacher saw its own earlier turns as assistant messages. The training rows never carried them. 12 of the first 21 failures at turn 4 drew the axes again over the ones already on the board, and 11 of those repeated the exact phrase from their own turn 2. [lora7-the-cut-ends-on-ink.md]
- moshi22 drew in 45 of 48 rows through the offline sampler and on 0 of 400 frames in the live harness. Same weights. The harness laid the narration in without the pauses every corpus scene has, and the pause is where the ink lands. [harness-prefix-rest.md]
- The first frame of a row was never a training target, because the loss pairs each position with the next one. 1,381 of 2,078 scenes opened by drawing axes at frame 0, so the model was handed the opening and never asked for it. Probability of the right first draw: 0.0006 on those scenes, 0.999 on scenes with a spoken lead-in. Same checkpoint. [moshi13-scene-openings.md]
- Recipe: print one training row and one live prompt as plain text and diff them. Do it again every time either side changes.

{{< deeper "Why the template and the system prompt stay in the training row" >}}
- Tempting move: strip the long rules out of the training prompt to save tokens (78% of the teacher prompt was rules and examples).
- Every source I read agrees you train with the same chat template and the same system prompt you serve with. Shortening the prompt is a separate experiment you run after a working adapter exists.
- Sources: the bbm plan `2026-09-09-the-dsl-goes-into-the-weights.md` collects them.
{{< /deeper >}}


## 2. Build the holdout first, and make it big enough to see a difference

*The eval set is the first data you make. If it cannot tell two models apart, nothing you conclude from it holds.*

- 12 examples: one example flipping moves the score by 8 points. gen11 trained again with only the seed changed, and one score moved by 4 of 18 examples. [parameter-motion-measure.md]
- 48 examples is better and still coarse. Four prompt fixes on the base model scored 7, 7, 11 and 7 of 48 on the same turn. With 95% intervals, 7/48 is anywhere from 7% to 27% and 11/48 from 13% to 37%. None of the four is distinguishable from the others, and I read each one as a result. [lora7-the-cut-ends-on-ink.md]
- lora8 at 30/48 is 48% to 75%, clear of every base probe. That jump is outside the noise.
- Rough sizes to keep in your head: at 48 examples you can only see differences of about 30 points. To tell 40% from 50% with independent samples you need about 380 examples a side. Scoring both models on the same examples, several samples each, cuts that a lot.
- The holdout has to ask the question the product asks. moshi21, one checkpoint: family matched on 22 of 48 scenes in `motionc` and 0 of 48 in `motions2`. `motionc` announces the drawing before it lands in 81% of rows and `motions2` almost never does. The checkpoint was the same, so the gap was measuring the holdout. [moshi21-the-corpus-never-taught-an-uncued-pen.md]
- A metric can reward the bug you are trying to remove. In the old corpus 87.6% of scenes sat on an axis window used by exactly one curve family, so matching the window meant memorising which window goes with which curve. moshi17b's 27/48 on window match was the defect scoring well. [moshi18-19-the-window-metric-was-scoring-the-defect.md]
- Validation loss is not an eval. The decision of when to start drawing was at most 23% of the draw loss. moshi10's validation loss fell from 0.24 to 0.13 and kept falling, and left to run on its own it drew nothing: 5,962 frames of silence. [the-loss-cannot-see-the-onset memory, moshi10]
- Freeze the holdout and keep it disjoint. bbm's `eval/motion` and `corpus/motion` share a naming scheme and not one filename, and the holdout's count is the one number that should never change.
- Write the decision rule before the run, the way the moshi4 doc opens with "Decision rule (do not invent another)". A rule written after the numbers arrive bends to fit them.

{{< deeper "Error bars on an eval" >}}
- Evan Miller at Anthropic wrote the statistics down for LLM evals in 2024: treat your eval questions as a sample from a bigger population, report a standard error, compare two models on the same questions (paired differences), decide how many questions you need before you run (power analysis), and sample several answers per question to shrink the noise.
- The Wilson interval is the one to use for a pass rate on a small set, because the simple formula breaks near 0% and 100%.
- Sources: [Miller 2024, Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640).
{{< /deeper >}}


## 3. What one example has to look like

*Every example teaches every rule you grade, including the ones you did not think of as rules.*

- lora7 trained on 1,216 corpus cuts beside 384 dialogue turns, 76 to 24. The gate ends a teacher turn on a question. Every corpus cut ended on a drawing, by the way the cutter was written. The adapter passed 2 of 48 against the base model's 8 to 11. The row check had read only the 384 dialogue rows and printed 100%. [lora7-the-cut-ends-on-ink.md]
- The cuts were included "for their DSL, not their shape". You cannot include an example for one of its properties. The model learns all of them, and the most common shape wins.
- The positions that carry the decision have to carry loss. The format marks silence with a pad token on every frame. A standard Hugging Face collator treated that token as row padding and dropped it from the loss: 238 of 366 masked positions, 65% of the mask. A model trained through it is never taught to stay quiet, which is most of what the format teaches. [bbm docs/frame-grid.md]
- Completion-only loss is the same trap in LLM form. In TRL, `assistant_only_loss=True` was silently ignored when `use_liger_kernel=True`, and the model trained on the prompt too. Check the mask on a real batch rather than trusting the flag.
- A model learns what is correlated in the data, not what you meant. E0 trained on scenes with the drawing's timing shuffled against the words. Planted timing separated by 0.83 nats and the real corpus by 0.05 to 0.08, because in the real corpus the timing was not tied to what was being said. There was nothing to learn. [e0.md]
- The fix is to put the relationship in the example. moshi4 trained on a corpus where 19% of scenes said what was about to be drawn, and it learned to draw only after an announcement. moshi5 trained on the same scenes with almost all of them announcing, and drew more even on holdouts that never announce: 19 to 64 of 100 on `motionv`. [moshi4-cue-corpus.md, moshi5-full-cue.md]
- Recipe: write every rule as a checker, run it over every row the job will train, and refuse the file when too few pass. A sample of the rows is how lora7 got through.


## 4. How many examples you need

*The format and the style show up after a few hundred examples. Getting the content right takes more, and more copies of the same thing stop helping early.*

- Chunting Zhou's group at Meta fine-tuned LLaMa 65B on 1,000 curated examples (LIMA) and people rated its answers equal to or better than GPT-4's in 43% of cases. In their own ablation, going from 2,000 to 32,000 Stack Exchange examples did not improve quality. They say it depends on "prompt diversity while maintaining high quality responses", not on quantity.
- Lichang Chen's group filtered the 52,000 Alpaca examples down to the best 9,000 with an LLM grader (AlpaGasus). The 9,000 beat the 52,000 and trained in 14 minutes instead of 80.
- Guanting Dong's group at Alibaba measured separate skills: general instruction following flattened after about a thousand examples, math and code kept improving as data grew. Zheng Yuan's group, also at Alibaba, found math accuracy grows with the log of the data amount.
- The LIMO group reached 63.3% on AIME24 with about 800 hard, hand-picked reasoning examples, about 1% of the data earlier fine-tunes used.
- bbm, small end: lora8 trained on 576 hand-written teacher turns. First-try pass went from 0.16 to 0.60, and full dialogues kept went from 4 of 48 to 48 of 48. [lora8-the-seeds-teach-the-turn.md]
- moshi18 trained on 348 rows and peaked at epoch 2. It picked up the new corpus's style, seven draws a scene instead of five, while its verify rate fell. [moshi18-19]
- bbm, larger end: family matched on `motionc` went 12, 17, 22 of 48 at 435, 746 and 5,501 scenes. Caveat for the prose: the first two warm-started and the third did not.
- A rare feature needs more than a few percent of examples. Coefficient curves (`params=`) sat in 2%, then 4%, then 7% of scenes, and across 30 eval scenes the model wrote one once. Repeating those scenes 8 times moved it from 0 to 1 of 12. [parameter-motion-density.md, parameter-motion-upsample.md]
- More variety of the wrong kind makes it worse. moshi15 added 452 new wordings of the same curve families. The first curve was right in about 4 of 12 scenes before and 2 of 9 after. The new wordings changed the words and left the window-to-family shortcut in place. [moshi15-variation-did-not-bind.md]
- Recipe: before you generate more, train on 25%, 50% and 100% of what you have and plot the eval. If it is flat, more of the same data will not help, and you have to change what the data covers.

{{< deeper "Is a LoRA adapter big enough for your data" >}}
- John Schulman at Thinking Machines measured LoRA against full fine-tuning in 2025. LoRA matched it when the adapter's trainable parameters hold more information than the dataset carries, and fell behind, gradually, when the dataset was bigger than that.
- A rough rule from the same work: count about 2 bits a parameter for the adapter. For bbm, rank 32 on all layers of the 12B is about 114M parameters. The corpus was on the order of 10M tokens. The adapter was never the limit.
- Sources: [LIMA, Zhou et al. 2023](https://arxiv.org/abs/2305.11206) · [AlpaGasus, Chen et al. 2023](https://arxiv.org/abs/2307.08701) · [Dong et al. 2023](https://arxiv.org/abs/2310.05492) · [Yuan et al. 2023](https://arxiv.org/abs/2308.01825) · [LIMO 2025](https://arxiv.org/abs/2502.03387) · [LoRA Without Regret, Schulman 2025](https://thinkingmachines.ai/blog/lora/)
{{< /deeper >}}


## 5. Read the whole dataset, not one example at a time

*A check that passes every example tells you nothing about the set.*

- Per-scene gates passed while the share of scenes drawing one command at a time drifted from 77% to 90%, and while 440 of 550 scenes ended on their last drawing. Every scene was fine and the set had drifted. [AGENTS.md, Testing]
- Count the same things in what the model writes. On the announced holdout moshi5 wrote the same gaussian for 25 of its 45 curves. [moshi5-full-cue.md]
- An accidental correlation becomes the lesson. With 87.6% of scenes on a window that belongs to one family, the model decided the family when it wrote the axis ranges, before any curve existed, and recited the rest. [moshi15-variation-did-not-bind.md]
- The model inherits the set's narrowness. lora8's passing turns use 0.14 distinct words per word against the base model's 0.32, and 31 distinct expressions in 58 turns. [lora8-the-seeds-teach-the-turn.md]
- Generated data repeats itself. Fifteen generated dialogues repeated 10 to 23 of their roughly 30 spoken lines from an earlier turn. The one hand-written dialogue repeated none. Every per-scene gate passed all fifteen. [lora7-the-cut-ends-on-ink.md]
- Whoever writes the data is part of the distribution. Of the twelve seed writers, writer 01 had none of eight dialogues contradicted by the judge and writer 10 had all eight. [dialogue-judge-panel.md]
- Mixing sources: Dong's group found mixing skills helps when data is scarce and makes them fight when data is plentiful.
- Recipe: run a census over the whole set on every change. Histograms of length and of commands per example, how each example ends, the most repeated lines and expressions, distinct words, a breakdown per source or per writer, and the same histograms over the holdout next to them.

{{< deeper "What training on generated data does to the tails" >}}
- Ilia Shumailov's group trained models on the output of earlier models, generation after generation. The rare cases disappeared first, and the output narrowed until it had almost no variance.
- Katherine Lee's group at Google found a single 61-word sentence repeated over 60,000 times in C4. Removing duplicates cut memorised output by ten times and reached the same accuracy in fewer steps.
- Sources: [Shumailov et al., Nature 2024](https://www.nature.com/articles/s41586-024-07566-y) · [Lee et al. 2021](https://arxiv.org/abs/2107.06499)
{{< /deeper >}}


## 6. Where examples come from: generators, hand-written seeds, gates and judges

*A gate checks the shape of an example and never whether what it says is true, and the model learns whatever the gate cannot see.*

- If an LLM writes your examples, ask for one rich example per call. Scenes kept: 0% at 8 per call, 43% at 3, 100% at 1. [AGENTS.md, Testing]
- Prompting a base model has a ceiling. After four prompt fixes the first-try pass stayed under a quarter of turns, and retries are not independent tries: one run gave up on 71 turns after 24 attempts each. [lora7-the-cut-ends-on-ink.md]
- Hand-written seeds got past it: 96 dialogues from twelve writers, 576 turns, and a LoRA trained on them. [lora8-the-seeds-teach-the-turn.md]
- The seeds passed every gate and were still wrong half the time. `verify` could not see 83.6% of 2,185 single-edit mutations of known-good scenes. A judge contradicted the arithmetic in 48 of 94 seed dialogues, and in 47 of 48 dialogues the adapter wrote, because it learned the false claims along with the shape. [docs/gate-misses/README.md, dialogue-judge-panel.md]
- A judge model is weak on facts. Two of the judge's contradictions were wrong, and only recomputing the drawing caught them. Sijun Tan's group built JudgeBench and found strong models judging objective correctness only slightly better than a coin. Compute every claim you can compute, and keep the judge for the questions arithmetic cannot answer.
- If you filter the model's own outputs and train on them (rejection sampling), the gain follows how many distinct correct examples you collect, not how many in total. Avi Singh's group at Google DeepMind got most of the coding gain from the first round, and later rounds made it worse. Restart from the base model each round.
- Recipe: generate fifty, read them, train a short run, and only then generate thousands. moshi18's corpus met all five of its acceptance targets and the model trained on it got worse on every axis. [moshi18-19]

{{< deeper "Sources for this section" >}}
- [JudgeBench, Tan et al. 2024](https://arxiv.org/abs/2410.12784) · [RFT, Yuan et al. 2023](https://arxiv.org/abs/2308.01825) · [ReST-EM, Singh et al. 2023](https://arxiv.org/abs/2312.06585)
{{< /deeper >}}


## 7. The run itself

*With the data right, the default settings work. Most of what goes wrong in the run is a part of the model training that nobody chose to train.*

- Print the names of the parameters that train, every time. In peft, `target_modules=["in_projs.0", "out_projs.0"]` matched by suffix and also wrapped Moshi's audio generator: 24 tensors, 589,824 parameters, in three checkpoints. The working explanation had been "LoRA broke the voice". [road-to-the-product plan]
- Loss weights and training tricks tend to move the wrong half. Weighting the formula tokens more (gen12) dropped formula-on-board from 14 to 18 of 48 down to 5. Feeding the model its own picks during training (moshi3) made it start drawing less often. [parameter-motion-formula-weighting.md, moshi-mix-own-picks.md]
- Undoing the weight and fixing it in the data worked: gen13 dropped the weighting, wrote the equation in the same place in every example, and formula-on-board went from 5 to 23 of 48. [parameter-motion-canonical-order.md]
- Start cold when the data is new. moshi17b, warm-started from the whole earlier lineage, scored 35/48 and moshi21, cold on the new corpus, 22/48. The gap cannot be attributed to anything, because two things changed.
- One change per run.
- Smoke-test on 16 rows and 3 steps before a long run. It costs minutes and catches the failures in section 8.
- LoRA defaults from Schulman 2025: adapters on all linear layers with the MLP ones mattering most, a learning rate about 10 times what full fine-tuning would use, and a small effective batch.
- What bbm added: rank 16 to 32 is plenty at this data size, one to three epochs, and stop on the eval, never on validation loss.


## 8. On a DGX Spark

*121 GB of memory shared by CPU and GPU changes how a job fails. It slows down instead of crashing.*

- There is no out-of-memory error. A 12B LoRA without gradient checkpointing on two rows of 4,183 tokens stayed alive for 26 minutes, never finished one forward pass, and was killed by the kernel with exit 137. [lora-author-first-steps.md]
- Look at watts before you look at loss. lora5 ran 9 hours at 53 W with one CPU core pinned and finished fewer than 10 optimizer steps. A job that draws little power is waiting on something other than the GPU.
- Measure the cost of a step and size the dataset from it. 12B LoRA with checkpointing: 30.1 s a micro-batch, 7.8 s forward and 22.3 s backward. 1,600 rows is 6.7 hours and 100 optimizer steps. All 15,466 rows would have been 64 hours. On this box you choose hundreds to low thousands of examples on purpose.
- Run the forward under bf16 autocast. Without it peft runs the LoRA path in fp32 and moves roughly a terabyte of extra data per forward pass over a 243 GB/s memory bus. That is the likely cause of lora5, and it is a guess.
- Left padding forces the slow attention path: memory-efficient attention took 28% of GPU time where flash would not run.
- NVFP4 checkpoints serve fast and cannot be trained. Train on the bf16 weights and serve the adapter over them. The base model repeated itself the same way in both formats, so quantisation was not the cause.
- Wheels built for cu128 have no kernels for the GB10 and fall back to the CPU while looking healthy. cu130 runs at full speed: 95.4 TFLOPS in the job image, 95.5 in the venv.
- A bigger batch made epochs slower, because padding dominated once the host syncs were gone. [throughput.md]
- Use the Spark for smoke runs and short runs, and rent 8×H100 for the long one. MoshiVis's schedule is about a day, roughly $600 to $800.


## 9. The recipe, in order

1. Write the live prompt and one training row, and diff them.
2. Build a frozen, disjoint holdout that asks the product's question, big enough for the difference you care about.
3. Score the base model on it, and score the gold data through the same scorer. That gives you a floor and a ceiling.
4. Write the rules as checkers and run them over every row.
5. Pilot fifty examples and read them.
6. Census the whole set against the holdout.
7. Train on 25%, 50% and 100% before making more.
8. Smoke-run 16 rows, print what trains, check the loss mask on a real batch.
9. One change per run, cold start on new data, decision rule written first.
10. Read the outputs yourself, then score them with intervals.

Stay curious ☕
