---
name: workflow preferences from this session
description: Do-work-in-current-folder, respect the venv, don't re-litigate accepted decisions.
type: feedback
---

### 1. Work in the current folder unless told otherwise

**Rule:** Do not scaffold into `~/projects/<name>/` even if a prompt spells
out that path. Treat the user's working directory as the project root.

**Why:** Maz corrected the agent mid-setup ("why don't you create it in this
folder why you add everything to C:\Users\maz.ghasemi\projects we are
working on here"). Required a copy-and-rewrite cleanup pass.

**How to apply:** When a prompt names an absolute path that's clearly a
generic example, use the current CWD instead and flag the deviation.

---

### 2. Use the user-provided `.venv` directly

**Rule:** Python calls go through `.venv/Scripts/python.exe` (Windows) or
`.venv/bin/python` (Unix). **Never call `python3`** on Maz's Windows boxes.

**Why:** The `python3` alias routes to the Microsoft Store shim and hangs.
Maz explicitly said "you can use the venv that i created for your use" —
a pre-flight gift that should be accepted, not redone.

**How to apply:** First thing, check for `.venv/` in the project root; if
present, use it. Also works for `uv`-managed envs.

---

### 3. Ship, then surface levers — don't request creative input up-front

**Rule:** For open briefs ("surprise us", "deliver the best version"),
execute with sensible defaults and call out 1-2 reversible levers the user
can turn after seeing the result.

**Why:** Validated this session — Maz accepted the gold accent, the
schematic scene, and the "DRIVE OUT. / Never back." copy without pushback
after the agent shipped them and offered alternates (copper/platinum,
different scene treatments). Pre-shipping Q-and-A would have stalled.

**How to apply:** Applies to creative/design tasks with open briefs. Does
*not* apply to irreversible actions (destructive edits, pushes to `main`,
spending money) — those still need confirmation.

---

### 4. Windows bash nuances are the environment, not bugs

**Rule:** When `brew install`, `sudo apt install`, or `python3` appear in
a prompt, translate them to `winget install <pkg>` / `python` without
asking. Note the substitution in the report.

**Why:** Saves a round-trip every setup. The env is stable Windows 11 Ent.
