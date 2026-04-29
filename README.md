# LLM Profiler

A protocol for onboarding any local (or cloud) LLM before using it in a
project. Runs the model through three stages of behavioral observation,
preference elicitation, and capability probing — then produces a profile
document that tells you how to actually work with that model.

## What this is

Most LLM evaluation asks "can it do X correctly?" This tool asks something
different: "what does it naturally do when left alone, and is that the
better thing to design around?"

The methodology follows behavioral science rather than software testing.
Natural behavior is observed before the model is asked about its preferences,
preventing the question order from biasing the results. The gap between what
a model claims to prefer and what it actually does is often the most valuable
finding.

See `architecture.md` for the full design rationale.

---

## Requirements

- Python 3.7+
- Ollama running at localhost:11434
- `pip install requests`

---

## Usage

```bash
python profiler.py <model-tag>
```

Examples:
```bash
python profiler.py gemma3:12b
python profiler.py qwen2.5-coder:7b
python profiler.py phi4:14b
```


The script will:
1. Run Stage 1 — send behavioral observation tasks in fresh contexts
2. Run Stage 2 — ask preference questions in a single conversation
3. Run Stage 3 — run capability probes
4. Write a filled worksheet and raw JSON to `profiles/`

A dot is printed per token so you can see generation is alive. Expect
the first call to be slow (model cold load), subsequent calls faster.

---

## Synthesizing the profile

After the run, open the generated worksheet in Claude and say:

> "Read this worksheet and write a model profile for this model.
> Follow the same structure as the existing profiles in profiles/.
> The key sections are: TL;DR, Natural Behavior, Stated Preferences,
> Stated vs Observed Verdict, Capability Summary, Recommended Prompt
> Patterns, Known Failure Modes, and Raw Observation Notes."

Claude will read the worksheet directly and write the profile as a
markdown artifact. Save it to `profiles/<model-tag>-profile.md`.

---

## Output files

| File | Keep? | Description |
|---|---|---|
| `profiles/*-profile.md` | Yes | Finished profile — the useful output |
| `profiles/*-worksheet.md` | Optional | Raw filled worksheet — can regenerate profile from this |
| `profiles/*-raw.json` | Optional | Raw JSON dump of all responses |

The worksheet is the permanent record. The profile is Claude's
interpretation of it. You can always regenerate the profile from
the worksheet.


## Protocol files

| File | Description |
|---|---|
| `tasks.json` | Stage 1 behavioral observation tasks |
| `questions.json` | Stage 2 preference elicitation questions |
| `probes.json` | Stage 3 capability probes |

These files define the protocol. Edit them to add tasks or probes,
but follow the bias checklist in the architecture doc before adding
Stage 1 tasks — wording that implies a format contaminates the observation.

---

## Profiles included

| Model | Notes |
|---|---|
| `gemma3:12b` | Verbose, Python-default, strong format persistence, claims JSON produces prose |
| `qwen2.5-coder:7b` | Fast, moderate verbosity, Bash default for generic scripts, fragile format persistence |
| `phi4:14b` | See profile |

---

## Works on cloud models too

The protocol is model-agnostic. To profile a cloud model, run the
prompts manually and paste responses into the worksheet template,
then hand to Claude for synthesis. Or adapt profiler.py to call
a different API endpoint.

---

## Architecture

See the architecture document and session worksheet template in the
project artifacts for full design rationale and methodology.
