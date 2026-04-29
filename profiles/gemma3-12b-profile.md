# Model Profile: gemma3:12b

Generated: 2026-04-30
Model tag: `gemma3:12b`
Context: Ollama on Windows 11, no system prompt, default temperature

---

## TL;DR

gemma3:12b is a verbose, helpful, and well-structured model that defaults
to Python for all code tasks and prose for open-ended data questions —
despite claiming JSON as its preferred structured format. It wraps every
code block in explanation and never returns bare output. Format persistence
is strong when explicitly requested. It is honest about uncertainty and
self-aware about its own failure modes. Design integrations around fenced
Python code with prose wrapping as the natural output unit — not raw JSON.

---

## Natural Behavior (Stage 1 Findings)

| Signal | Observed default |
|---|---|
| Code language | Python — unprompted, every time |
| Config/markup | Domain-appropriate label (apacheconf, nginxconf) |
| Fence label | Always present, always accurate to content |
| Prose wrapping | Always — never returns a bare block |
| Structured data format | Prose (NOT JSON — contradicts stated preference) |
| Planning style | Plan-first, then step-by-step with explanation |
| Path convention | Prose instructions ("save as X in folder Y") |
| Multi-option tendency | Offers 2+ alternatives unprompted (Flask+Express, Apache+Nginx) |
| Response length | Very long — errs heavily toward completeness |

---

## Stated Preferences (Stage 2 Findings)

| Preference | What the model claims |
|---|---|
| Structured format | JSON — cites ubiquity, readability, lightweight |
| Fence label | Lowercase language name matching the code |
| Prose wrapping | Always adds explanation — considers bare blocks unhelpful |
| Path convention | Prose instructions with suggested directory |
| Planning style | Plan-first conceptual outline, then iterative execution |
| Uncertainty signal | Explicit hedging phrases ("I believe", "should", "likely") |
| Format persistence | Will try but may drift — honest about this limitation |

---

## Stated vs. Observed — Verdict

| Signal | Stage 1 Observed | Stage 2 Stated | Match? | Verdict |
|---|---|---|---|---|
| Structured data format | **Prose** | JSON | Differs | Ride observed: use prose, not JSON, for data descriptions |
| Fence label | Domain-accurate label | Lowercase language name | Match | High confidence — labels are reliable |
| Prose wrapping | Always present | Always present | Match | High confidence — never expect bare output |
| Planning style | Plan then explain | Plan-first | Match | High confidence |
| Path convention | Prose instructions | Prose instructions | Match | High confidence |
| Uncertainty signal | Hedging phrases | Hedging phrases | Match | High confidence |
| Format persistence | Strong (5/5 JSON turns) | Tries but may drift | Match | Reliable when set — reinforce in system prompt for critical use |

### Key Finding
The single most important mismatch: gemma3:12b claims JSON but reaches
for prose when describing structured data naturally. The Stage 1 European
capitals and user database tasks both produced prose, not JSON. If your
integration requires structured output, you must request it explicitly and
enforce it in the system prompt.

---

## Capability Summary

| Capability | Rating | Notes |
|---|---|---|
| Word counting | Reliable | Correctly answered 5 for a 5-word sentence |
| List counting | Reliable | Correct on 6-item list |
| Arithmetic | Reliable | 17x13=221 correct with working shown |
| Multi-constraint following | Unreliable | Used adjectives when told no adjectives; surface structure maintained, content rules dropped |
| Format persistence (JSON) | Reliable | Maintained JSON across all 5 turns including a haiku request |
| Self-awareness | Reliable | Gave honest, categorised list of failure modes |
| Transitive logic | Reliable | Correct with clean reasoning, named transitivity |
| Code debugging | Reliable | Immediately identified subtraction-instead-of-addition bug |

---

## Recommended Prompt Patterns

**For structured output:**
```
Respond only with a JSON object. No prose before or after. No markdown.
```
Without this, expect rich prose regardless of what the model claims to prefer.

**For concise responses:**
```
Be brief. One code block only. No explanation unless asked.
```
Without this, every response includes extensive explanation and follow-up questions.

**For a specific language:**
```
Write this in Rust. Do not offer Python alternatives.
```
The model defaults to Python and often offers a second language unprompted.

**For file path in output:**
```
Include the target file path as a comment on the first line of the code block.
```
The model puts path info in prose by default — this forces it into the block.

**For format persistence:**
Set the format rule in the system prompt, not just the first message.

---

## Known Failure Modes

**Verbose by default.** Every response includes explanation, alternatives,
and follow-up questions. Always prompt for brevity explicitly in pipelines.

**Multi-option flooding.** Asked for one thing, gives two. Suppress with:
"Give one option only. Do not offer alternatives."

**JSON claim vs prose reality.** The model says it prefers JSON. It does not
reach for JSON naturally. Treat the stated preference as a trained answer,
not behavioural truth.

**Adjective blindness under multi-constraint.** Drops content-level rules
(no adjectives) while maintaining structural rules (3 sentences, length).
Priority goes to surface structure over content constraints.

**Trailing question habit.** Almost every response ends with 2-4 clarifying
questions. Suppress with: "Do not ask follow-up questions."

**Path info stays in prose.** File paths never appear in code blocks unless
explicitly instructed.

---

## Raw Observation Notes

- Response length is extreme — T01 config file was ~1000 tokens
- Model asks follow-up questions at the end of nearly every response
- Self-awareness response (P06) was thorough and well-categorised
- Format persistence (P05) was impressive — maintained JSON even for a haiku
- The model is trained for a beginner audience, explaining the verbosity,
  alternatives, and constant clarifying questions
