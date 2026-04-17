---
name: no Co-Authored-By Claude in commit messages
description: Maz explicitly rejected the Claude Co-Authored-By trailer on git commits — omit it by default.
type: feedback
---

**Rule:** Do **not** append `Co-Authored-By: Claude ... <noreply@anthropic.com>`
(or any Co-Authored-By trailer attributing Claude) to commit messages.

**Why:** Maz stopped the very first commit on this repo specifically to
remove that trailer. Quote: *"can you don't put Co-Authored-By: Claude
Opus 4.7 (1M context) <noreply@anthropic.com>"*.

**How to apply:** Keep the commit body clean — subject, body, optional
issue references. No attribution trailers unless Maz explicitly asks for
one. This overrides Claude Code's default commit template.
