---
name: tooling map — skills, MCP, CLI, assets
description: Where installed tools live and how to reach the canonical sources for this project.
type: reference
---

## Claude Code skills (non-plugin, user-cloned)

| Skill           | Repo                                                     | On-disk                              |
|-----------------|----------------------------------------------------------|--------------------------------------|
| CSS Animation   | https://github.com/neonwatty/css-animation-skill         | `~/.claude/skills/css-animation/`    |
| Frontend Slides | https://github.com/zarazhangrui/frontend-slides          | `~/.claude/skills/frontend-slides/`  |

Re-install after a new-machine clone:
```bash
git clone --depth 1 https://github.com/neonwatty/css-animation-skill ~/.claude/skills/css-animation
git clone --depth 1 https://github.com/zarazhangrui/frontend-slides ~/.claude/skills/frontend-slides
```

**Plugin skills** (no install — already bundled in Claude Code):
`frontend-design:frontend-design`, `superpowers:using-superpowers`,
`superpowers:brainstorming`, `vercel:knowledge-update`.

The `anthropics/claude-code-skills` GitHub URL in the original setup brief
is a 404; there is no external "Frontend Design" skill — use the plugin.

## MCP servers (project-scoped in `.mcp.json`)

| Name       | Command                                          | Notes |
|------------|--------------------------------------------------|-------|
| puppeteer  | `@modelcontextprotocol/server-puppeteer`        | npm global install |
| fetch      | `uvx mcp-server-fetch`                           | Python, needs `uv` |
| filesystem | `@modelcontextprotocol/server-filesystem <cwd>`  | Path is HARD-CODED — rewrite on new machine |
| playwright | `@playwright/mcp --headless`                     | Primary screenshot tool |

**`@modelcontextprotocol/server-fetch` does NOT exist on npm** — only
`mcp-server-fetch` for Python via `uvx`. Do not try to install the npm one.

## CLI tools installed (original Windows box)

| Tool        | Version | Location / install            |
|-------------|---------|-------------------------------|
| Node.js     | 24.12.0 | nodejs.org                    |
| Python      | 3.13.5  | python.org                    |
| ffmpeg      | 8.1     | `winget install Gyan.FFmpeg`  |
| uv          | 0.9.2   | `pip install uv`              |
| serve       | 14.2.6  | `npm i -g serve`              |
| http-server | 14.1.1  | `npm i -g http-server`        |
| ImageMagick | —       | not installed; `sharp` covers it |

## Asset sources

- Product images scraped from **turntables.com.au** via `scrape_images.py`.
- `_rank_images.py` re-ranks by pixel count (NOT filesize — PNGs trick
  filesize ranking) and promotes top landscape/portrait to named slots.
- Fresh-scrape: `python scrape_images.py && python _rank_images.py`.
- Raw scrapes live in `assets/images/scraped/` (kept in git as backup).

## External deps loaded at runtime (no install)

- GSAP 3.12.5 — `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js`
- Fraunces + Inter — Google Fonts CDN (`fonts.googleapis.com`)
- Picsum (fallback test image) — `picsum.photos/800/600`

## GitHub repo

Source of truth: **https://github.com/Maz2580/Demo**
