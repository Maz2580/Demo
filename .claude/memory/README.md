# How to use these memory files on a new machine

These files were authored during the original build session. They mirror the
shape of Claude Code's auto-memory system (one file per fact, `MEMORY.md`
index pointing at each).

## Option A — seed into your personal memory

On the new machine, find your memory folder. Default path:

```
<user-home>/.claude/projects/<slugified-project-path>/memory/
```

For this repo freshly cloned to e.g. `C:\work\Demo`, the slug would be
`C--work-Demo`, giving:

```
C:\Users\<you>\.claude\projects\C--work-Demo\memory\
```

Copy every `*.md` in this directory into that folder. The agent will pick
them up on the next session start and apply them like native memory.

## Option B — just read them

You don't have to formally import. The next agent reads `CLAUDE.md` at the
repo root on session start, which already links here. You can ask it to
"read `.claude/memory/*.md` and absorb" at the start of any session and it
will behave the same way.

## Keeping them in sync

As you add memories in a new session, update both locations (your personal
folder **and** this committed copy) so future clones stay current. The
repo-level copy is the portable source of truth.
