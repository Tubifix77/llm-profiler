# Model Profile: qwen2.5-coder:7b

Generated: 2026-04-30
Model tag: `qwen2.5-coder:7b`
Context: Ollama on Windows 11, no system prompt, default temperature

---

## TL;DR

qwen2.5-coder:7b is a compact, fast, code-oriented model. It defaults to
Python for code tasks but reached for Bash unprompted on T07 — the only
model so far to do so. It always wraps output in prose but is notably more
concise than gemma3:12b. Like gemma3, it claims JSON as preferred structured
format but produces prose naturally. Format persistence broke on the final
turn of P05 — it answered in plain English instead of JSON. Multi-constraint
following failed silently: sentences were too short and contained adjectives.
Word counting is accurate. Good fit for code generation tasks with explicit
language instructions; unreliable for strict format pipelines without
enforcement.

---

## Natural Behavior (Stage 1 Findings)

| Signal | Observed default |
|---|---|
| Code language | Python — every code task except T07 |
| T07 exception | Bash — when asked to "write a script" with no domain hint |
| Config/markup | Apache only (not Apache+Nginx like gemma3) |
| Fence label | Domain-appropriate (apache, python, sh, bash) |
| Prose wrapping | Always present |
| Structured data format | Prose with bold headers and numbered lists |
| Planning style | Step-by-step numbered instructions |
| Path convention | Prose instructions, mentions specific filenames |
| Multi-option tendency | Lower than gemma3 — gave one option for most tasks |
| Response length | Moderate — noticeably shorter than gemma3:12b |


---

## Stated Preferences (Stage 2 Findings)

| Preference | What the model claims |
|---|---|
| Structured format | JSON — same reasoning as gemma3 (readability, interoperable) |
| Fence label | Language name matching the code (python, bash, html etc.) |
| Prose wrapping | Context-dependent — beginner gets explanation, expert gets bare block |
| Path convention | Explicit folder names and full filenames in prose |
| Planning style | Hybrid — plan first then iterate (same claim as gemma3) |
| Uncertainty signal | Hedging phrases, ask for confirmation |
| Format persistence | Claims it will maintain format throughout if asked |

---

## Stated vs. Observed — Verdict

| Signal | Stage 1 Observed | Stage 2 Stated | Match? | Verdict |
|---|---|---|---|---|
| Structured data format | Prose + bold headers | JSON | Differs | Ride observed: prose with headers is the natural unit |
| Fence label | Domain-accurate | Language name | Match | High confidence — labels reliable |
| Prose wrapping | Always present | Context-dependent | Partial | In practice always wraps — stated nuance does not appear in behavior |
| Path convention | Prose with filenames | Explicit paths in prose | Match | High confidence |
| Planning style | Numbered steps | Plan-first hybrid | Match | High confidence |
| Uncertainty signal | Hedging phrases | Hedging phrases | Match | High confidence |
| Format persistence | Broke on turn 5 | Will maintain | Differs | Unreliable — drifted to plain English on final turn of P05 |

### Key Findings

**JSON vs prose:** Same mismatch as gemma3 — claims JSON, produces prose.
The natural structured output unit is bold-header numbered lists, not JSON.

**Bash default on T07:** When the task was "write a script" with no domain
context, it chose Bash over Python. This is the coder model's domain
awareness showing — a "script" without context means shell script. This
is the natural behavior to ride for generic scripting tasks.

**Format persistence failure:** Passed 4/5 JSON turns then broke on turn 5
("Are you still in JSON?") and answered in plain English. The question
phrasing may have triggered a conversational response. Treat as unreliable
without system prompt enforcement.


---

## Capability Summary

| Capability | Rating | Notes |
|---|---|---|
| Word counting | Reliable | Correct: 5 words in "The quick brown fox jumped" |
| List counting | Reliable | Correct: 6 items |
| Arithmetic | Reliable | 17x13=221 correct |
| Multi-constraint following | Unreliable | Sentences too short (3-4 words not 8), contains adjectives ("joyful") |
| Format persistence (JSON) | Inconsistent | 4/5 turns correct, broke on turn 5 |
| Self-awareness | Reliable | Honest list of failure modes |
| Transitive logic | Reliable | Correct with LaTeX notation and transitivity named |
| Code debugging | Reliable | Found subtraction bug immediately |

---

## Recommended Prompt Patterns

**For structured output:**
```
Respond only with a JSON object. No prose before or after. No markdown.
```
Same as gemma3 — must be explicit, stated preference does not match behavior.

**For shell scripting:**
```
Write a bash script that...
```
The model naturally reaches for Bash when the domain is unspecified scripting.
Ride this default — do not fight it by asking for "a script in Python" unless
you specifically need Python.

**For Python specifically:**
```
Write a Python script that...
```
Specify explicitly. "Write a script" alone may produce Bash.

**For concise output:**
```
Return only the code. No explanation.
```
Less necessary than with gemma3 but still recommended for pipelines.

**For format persistence:**
Set format rule in system prompt. Turn-1 instruction is insufficient —
demonstrated failure on turn 5 even after clean turns 1-4.

**For multi-constraint tasks:**
Break constraints into separate instructions or verify output programmatically.
The model silently fails constraints rather than flagging inability.

---

## Known Failure Modes

**Silent constraint dropping.** On P04 it produced sentences of 3-4 words
when asked for exactly 8, and used adjectives when told not to. It did not
flag the failure or apologise — it just returned wrong output confidently.
Always verify constraint-heavy outputs programmatically.

**Format persistence fragile on meta-questions.** A question about format
("Are you still in JSON?") triggered a plain English answer. The model
treated the meta-question as a conversational prompt rather than staying
in the requested format. Avoid meta-questions in format-constrained sessions.

**JSON claim vs prose reality.** Same as gemma3 — trained answer, not
behavioral truth.

**Prose always present.** Despite claiming it adjusts for expert audiences,
every Stage 1 response included prose wrapping. Do not rely on the model
self-adjusting — always specify if you want bare output.

---

## Comparison Notes vs gemma3:12b

| Dimension | qwen2.5-coder:7b | gemma3:12b |
|---|---|---|
| Speed | Much faster | Slow |
| Verbosity | Moderate | Extreme |
| Multi-option flooding | Rare | Every response |
| Trailing questions | Rare | Every response |
| Bash default | Yes (T07) | No — always Python |
| Word counting | Reliable | Reliable |
| Format persistence | Inconsistent (4/5) | Reliable (5/5) |
| Constraint following | Unreliable | Unreliable |
| Code quality | Clean, minimal | Verbose with comments |

---

## Raw Observation Notes

- Noticeably faster than gemma3:12b — practical for interactive use
- T07 Bash default is the most interesting behavioral finding
- Used LaTeX notation in P07 logic proof — gemma3 used plain text
- Stage 2 answers were more concise and direct than gemma3
- P05 turn 5 failure is a useful reminder that meta-questions break format
- Coder-tuned model shows in code quality: clean, minimal, no unnecessary comments
