# Model Profile: phi4:14b

Generated: 2026-04-30
Model tag: `phi4:14b`
Context: Ollama on Windows 11, no system prompt, default temperature

---

## TL;DR

phi4:14b is a clean, well-structured model from Microsoft's reasoning lineage.
It defaults to Python for code tasks but reached for Bash on T05 (same as
qwen2.5-coder). Like all three profiled models it claims JSON but naturally
produces prose. Format persistence is strong — 5/5 JSON turns maintained.
The most notable finding is a serious word counting failure: it said "The
quick brown fox jumped" has 4 words by excluding "jumped" with a fabricated
justification. This is a confident hallucination, not a miscounting.
Constraint following is also unreliable. Strong for reasoning and explanation
tasks; unreliable for counting, strict constraints, and any task requiring
precise literal reading.

---

## Natural Behavior (Stage 1 Findings)

| Signal | Observed default |
|---|---|
| Code language | Python — every task except T05 |
| T05 exception | Bash for pip install step, Python for app code |
| Config/markup | Apache only — single option, no Nginx alternative |
| Fence label | Domain-accurate (apache, python, bash) |
| Prose wrapping | Always present |
| Structured data format | Prose with numbered lists and bold headers |
| Planning style | Numbered steps, headers per step |
| Path convention | Prose with OS-specific paths (Windows and Linux shown) |
| Multi-option tendency | Low — single option per task |
| Response length | Moderate — less verbose than gemma3, similar to qwen |


---

## Stated Preferences (Stage 2 Findings)

| Preference | What the model claims |
|---|---|
| Structured format | JSON — same reasoning as other models |
| Fence label | Language name matching the code |
| Prose wrapping | Context-dependent — adjusts for audience |
| Path convention | Explicit paths with OS-specific variants |
| Planning style | Hybrid — plan first then adapt (same claim as others) |
| Uncertainty signal | Hedging phrases, qualifiers, invite feedback |
| Format persistence | Will try but warns of possible drift due to complexity |

---

## Stated vs. Observed — Verdict

| Signal | Stage 1 Observed | Stage 2 Stated | Match? | Verdict |
|---|---|---|---|---|
| Structured data format | Prose + numbered lists | JSON | Differs | Ride observed — prose with headers is the natural unit |
| Fence label | Domain-accurate | Language name | Match | High confidence |
| Prose wrapping | Always present | Context-dependent | Partial | Always wraps in practice — stated nuance does not appear |
| Path convention | OS-specific prose | OS-specific prose | Match | High confidence |
| Planning style | Numbered steps with headers | Hybrid plan-first | Match | High confidence |
| Uncertainty signal | Hedging phrases | Hedging phrases | Match | High confidence |
| Format persistence | 5/5 JSON turns | Will try, may drift | Better than stated | Strongest persistence of all three models tested |

### Key Findings

**JSON vs prose:** Same mismatch as both other models — all three claim JSON,
none reach for it naturally.

**Word count hallucination:** P01 returned 4 words for "The quick brown fox
jumped" and fabricated a justification ("jumped is not included because it
does not appear after fox within the given text"). This is not a counting
error — it is a confident confabulation. The model invented a reason for
a wrong answer rather than simply miscounting. Flag for any task requiring
precise literal text processing.

**Format persistence strongest of three:** Maintained JSON cleanly across
all 5 turns including the meta-question turn 5, where both other models
showed weakness.


---

## Capability Summary

| Capability | Rating | Notes |
|---|---|---|
| Word counting | Unreliable | Returned 4 for a 5-word sentence with fabricated justification — confabulation, not miscounting |
| List counting | Reliable | Correct: 6 items |
| Arithmetic | Reliable | 221 correct with working shown |
| Multi-constraint following | Unreliable | Contains adjectives ("nearby", "joyfully"), word count unverified |
| Format persistence (JSON) | Reliable | 5/5 turns including meta-question — best of three models |
| Self-awareness | Reliable | Honest categorised list of failure modes |
| Transitive logic | Reliable | Correct with LaTeX notation and formal property named |
| Code debugging | Reliable | Found bug and explained the name vs operation mismatch |

---

## Recommended Prompt Patterns

**For structured output:**
```
Respond only with a JSON object. No prose before or after. No markdown.
```
Same requirement as all three models — stated JSON preference is not behavioral.

**For format persistence:**
phi4 is the most reliable of the three tested models for maintaining a
requested format. System prompt enforcement still recommended, but turn-1
instruction is more likely to hold than with gemma3 or qwen.

**For precise literal tasks (counting, exact text):**
```
Count each word individually. List them numbered before giving the total.
```
Force the model to enumerate before concluding. The P01 failure was a
confident wrong answer — enumeration catches this before the conclusion.

**For code tasks:**
```
Write this in Python only.
```
Specify language. Like qwen, phi4 may reach for Bash in ambiguous scripting
contexts.

**For concise output:**
```
Return only the code. No explanation.
```
Always wrap in prose by default — suppress explicitly for pipelines.

---

## Known Failure Modes

**Confident confabulation on literal tasks.** P01 did not just miscount —
it invented a grammatical justification for excluding "jumped" from the
sentence. This is a hallucination pattern, not a counting weakness. Any
task requiring precise literal reading of text should be treated with
suspicion and verified. Force enumeration before conclusion.

**Silent constraint dropping.** P04 produced sentences containing adjectives
("nearby", "joyfully") despite explicit instruction. Like qwen, no apology
or flag — confident wrong output.

**JSON claim vs prose reality.** All three models share this mismatch.
Trained answer, not behavioral truth.

**Prose always present.** Despite claiming audience-adaptive wrapping,
every Stage 1 response included prose. Do not rely on self-adjustment.

---

## Comparison Notes vs Other Profiled Models

| Dimension | phi4:14b | qwen2.5-coder:7b | gemma3:12b |
|---|---|---|---|
| Speed | Slow | Fast | Slow |
| Verbosity | Moderate | Moderate | Extreme |
| Multi-option flooding | Rare | Rare | Every response |
| Trailing questions | Rare | Rare | Every response |
| Bash default | Partial (T05) | Yes (T07) | No |
| Word counting | Unreliable (confabulation) | Reliable | Reliable |
| Format persistence | Reliable (5/5) | Inconsistent (4/5) | Reliable (5/5) |
| Constraint following | Unreliable | Unreliable | Unreliable |
| Reasoning style | Formal, LaTeX notation | Direct | Verbose explanation |

---

## Raw Observation Notes

- Word count confabulation in P01 is the standout finding — qualitatively
  different from a simple counting error
- Format persistence across meta-question (P05 turn 5) is notably stronger
  than both other models
- Uses LaTeX math notation like qwen — both are more formally oriented than gemma3
- T05 bash label was for the pip install step only — Python for the app itself
- Stage 2 answers were the most structured and hedged of all three models
- Constraint following failures were silent and confident across all three
  models — this appears to be a universal pattern worth noting in the README
