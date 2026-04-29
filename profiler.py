"""
LLM Profiler — Session conductor
Drives a local Ollama model through the 3-stage profiling protocol
and writes a filled worksheet + final profile.
"""
import json, requests, datetime, pathlib, sys

OLLAMA_URL = "http://localhost:11434/api/chat"
BASE = pathlib.Path(__file__).parent
TASKS_FILE     = BASE / "tasks.json"
QUESTIONS_FILE = BASE / "questions.json"
PROBES_FILE    = BASE / "probes.json"
PROFILES_DIR   = BASE / "profiles"
PROFILES_DIR.mkdir(exist_ok=True)

# ── Ollama helpers ────────────────────────────────────────────────

def chat(model, messages):
    """Stream response from Ollama — prints a dot per token, returns full text."""
    print("    ", end="", flush=True)
    payload = {"model": model, "messages": messages, "stream": True}
    full = []
    with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            token = chunk.get("message", {}).get("content", "")
            if token:
                print(".", end="", flush=True)
                full.append(token)
            if chunk.get("done"):
                break
    print(" done", flush=True)
    return "".join(full)

def single(model, prompt):
    """One-shot prompt in a fresh context."""
    return chat(model, [{"role": "user", "content": prompt}])


# ── Observation helpers ───────────────────────────────────────────

def detect_fence_label(text):
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```") and len(s) > 3:
            return s[3:].strip() or "bare"
    return "none"

def detect_format(text):
    t = text.strip()
    if t.startswith("{") or t.startswith("["): return "json"
    if "```" in t:                              return "fenced_code"
    if t.startswith("- ") or t.startswith("*"): return "bullet_list"
    if t.startswith("# "):                      return "markdown"
    return "prose"

def has_prose_wrap(text):
    lines = text.splitlines()
    outside, in_fence = [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence:
            outside.append(ln.strip())
    return any(outside)

def observe(text, signals):
    obs = {}
    if "format"      in signals: obs["format"]      = detect_format(text)
    if "fence_label" in signals: obs["fence_label"] = detect_fence_label(text)
    if "prose_wrap"  in signals: obs["prose_wrap"]  = has_prose_wrap(text)
    return obs


# ── Stage runners ─────────────────────────────────────────────────

def run_stage1(model, tasks):
    print("\n── STAGE 1: Behavioral Observation ──")
    results = []
    for t in tasks:
        print(f"\n  [{t['id']}] {t['category']}")
        print(f"  Prompt: {t['prompt']}")
        resp = single(model, t["prompt"])
        obs  = observe(resp, t.get("observe", []))
        print(f"  Observed: {obs}")
        results.append({"id": t["id"], "prompt": t["prompt"],
                        "response": resp, "observed": obs})
    return results

def run_stage2(model, questions):
    print("\n── STAGE 2: Preference Elicitation ──")
    history, results = [], []
    for q in questions:
        print(f"\n  [{q['id']}] {q['topic']}")
        history.append({"role": "user", "content": q["prompt"]})
        resp = chat(model, history)
        history.append({"role": "assistant", "content": resp})
        print(f"  → {resp[:120]}")
        results.append({"id": q["id"], "topic": q["topic"],
                        "prompt": q["prompt"], "response": resp})
    return results


def run_stage3(model, probes):
    print("\n── STAGE 3: Capability Probing ──")
    results = []
    for p in probes:
        print(f"\n  [{p['id']}] {p['category']}")
        if p["category"] == "format_persistence":
            history = [{"role": "user", "content": p["prompt"]}]
            resp0 = chat(model, history)
            history.append({"role": "assistant", "content": resp0})
            turn_results = [resp0]
            for fu in p.get("followups", []):
                history.append({"role": "user", "content": fu})
                r = chat(model, history)
                history.append({"role": "assistant", "content": r})
                turn_results.append(r)
            results.append({"id": p["id"], "category": p["category"],
                            "expected": p["expected"], "turns": turn_results})
        else:
            resp = single(model, p["prompt"])
            print(f"  Expected : {p['expected']}")
            print(f"  Got      : {resp[:120]}")
            results.append({"id": p["id"], "category": p["category"],
                            "expected": p["expected"], "response": resp})
    return results


# ── Worksheet writer ─────────────────────────────────────────────

def write_worksheet(model, s1, s2, s3, path):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# LLM Profiler Worksheet", "",
        f"Model: `{model}`  |  Date: {ts}", "",
        "---", "",
        "## Stage 1 — Behavioral Observation", "",
    ]
    for r in s1:
        lines += [
            f"### {r['id']}",
            f"**Prompt:** {r['prompt']}", "",
            f"**Observed:** {r['observed']}", "",
            "**Raw response:**", "```",
            r["response"], "```", "",
        ]
    lines += ["---", "", "## Stage 2 — Preference Elicitation", ""]
    for r in s2:
        lines += [
            f"### {r['id']} — {r['topic']}",
            f"**Q:** {r['prompt']}", "",
            f"**A:** {r['response']}", "",
        ]
    lines += ["---", "", "## Stage 3 — Capability Probes", ""]
    for r in s3:
        lines += [f"### {r['id']} — {r['category']}"]
        if "turns" in r:
            lines += [f"**Expected:** {r['expected']}", ""]
            for i, t in enumerate(r["turns"]):
                lines += [f"**Turn {i+1}:** {t[:300]}", ""]
        else:
            lines += [
                f"**Expected:** {r['expected']}",
                f"**Got:** {r['response'][:400]}", "",
            ]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWorksheet → {path}")


# ── Main ─────────────────────────────────────────────────────────

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "gemma3:12b"
    print(f"LLM Profiler  |  model: {model}\n")

    tasks     = json.loads(TASKS_FILE.read_text())["tasks"]
    questions = json.loads(QUESTIONS_FILE.read_text())["questions"]
    probes    = json.loads(PROBES_FILE.read_text())["probes"]

    s1 = run_stage1(model, tasks)
    s2 = run_stage2(model, questions)
    s3 = run_stage3(model, probes)

    slug = model.replace(":", "-").replace("/", "-")
    ts   = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    ws   = PROFILES_DIR / f"{slug}-{ts}-worksheet.md"
    raw  = PROFILES_DIR / f"{slug}-{ts}-raw.json"

    write_worksheet(model, s1, s2, s3, ws)
    raw.write_text(json.dumps(
        {"model": model, "s1": s1, "s2": s2, "s3": s3},
        indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Raw JSON   → {raw}")
    print("\nDone. Hand the worksheet to Claude for profile synthesis.")

if __name__ == "__main__":
    main()
