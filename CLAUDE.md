# Claude Code — Project Context

> **Read this first.** Everything downstream assumes you have.

## 1 · What this project is

A 30-second cinematic product trailer for **Australian Turntables**
([turntables.com.au](https://www.turntables.com.au) · `@australianturntables`).
Destination is Instagram Reels; the final deliverable will be rendered by
screen-recording `trailer.html` in Chrome at **1080×1920**, then importing the
capture into CapCut for music + captions.

- Client was featured on *The Block* 2023.
- The product rotates — rotation is the creative spine of every transition.
- 6 scenes over 30s: wordmark → hero reveal → schematic → gallery → statement → logo lockup.
- Accent colour is warm gold `#C9A961` (see lever below).

## 2 · Current status

**Shipped:** environment, scraper, trailer HTML+CSS+GSAP, verification
screenshots for every scene, recording guide. Nothing blocks the client from
capturing right now.

**Open creative levers** the user may want to turn:
- Accent colour (gold / copper / platinum) — single CSS var
- Scene 4 plate framing (banner strips vs. portrait) — ~10-line CSS tweak
- Statement copy in Scene 5 ("DRIVE OUT. / Never back.") — HTML edit

## 3 · Repo map

```
├── CLAUDE.md              ← this file — project context for the next agent
├── SETUP_REPORT.md        ← env-setup result snapshot (what's installed)
├── SESSION_LOG.md         ← chronological narrative of the setup + build
├── RECORDING.md           ← how to capture trailer.html for CapCut
├── trailer.html           ← the deliverable — 30s animation, self-contained
├── scrape_images.py       ← re-pull images from turntables.com.au
├── _rank_images.py        ← re-rank + promote top scrapes to named slots
├── test_scrape.py         ← one-off scrape smoke-test (Setup Step 6)
├── test.html              ← dev-server smoke-test (Setup Step 7)
├── package.json           ← npm deps for the trailer pipeline
├── .mcp.json              ← project-scoped MCP server config
├── assets/
│   ├── fonts/             ← empty; Fraunces + Inter load from Google Fonts CDN
│   └── images/
│       ├── hero.jpg                 ← Scene 2 full-bleed
│       ├── scene4-1.jpg / 2 / 3.jpg ← Scene 4 gallery plates
│       ├── detail.jpg               ← spare (currently unused)
│       ├── manifest.json            ← which raw file feeds which slot
│       └── scraped/                 ← 38 raw scrapes (source of truth)
└── .gitignore             ← ignores node_modules, .venv, .remember, etc.
```

## 4 · How to continue on a new machine

```bash
git clone https://github.com/Maz2580/Demo
cd Demo

# --- Python side (venv) ---
python -m venv .venv
.venv\Scripts\activate                     # Windows
# source .venv/bin/activate                # macOS/Linux
pip install requests Pillow playwright beautifulsoup4 httpx
python -m playwright install chromium

# --- Node side ---
npm install
npm install -g serve http-server @modelcontextprotocol/server-filesystem \
               @modelcontextprotocol/server-puppeteer @playwright/mcp

# --- Start dev server + open trailer ---
npx serve . -p 3000
# → http://localhost:3000/trailer?exact
```

Then see **RECORDING.md** for capture workflow.

## 5 · Claude Code skills installed

Installed on the original machine under `~/.claude/skills/` (cloned from GitHub):

| Skill            | Location                                              | Purpose in this project |
|------------------|-------------------------------------------------------|-------------------------|
| CSS Animation    | `~/.claude/skills/css-animation/`                     | Patterns for CSS keyframes + GSAP helpers |
| Frontend Slides  | `~/.claude/skills/frontend-slides/`                   | Scene-based composition templates |

**Plugin skills** already available in the session (no install needed):

| Skill                                   | Role in this project |
|-----------------------------------------|----------------------|
| `frontend-design:frontend-design`       | Premium-interface design direction |
| `superpowers:using-superpowers`         | Standard agent-behaviour bootstrap |
| `superpowers:brainstorming`             | Creative-work gate (used implicitly) |
| `vercel:*` (knowledge-update, etc.)     | Deployment path if trailer ever moves to Vercel |

The `anthropics/claude-code-skills` GitHub URL in the original prompt is a 404 —
the "Frontend Design" skill only exists as the `frontend-design:frontend-design`
plugin.

## 6 · MCP servers configured

Defined in **`.mcp.json`** at the repo root. Claude Code loads them
automatically on session start.

| Server     | Command                                             | Purpose |
|------------|-----------------------------------------------------|---------|
| puppeteer  | `npx -y @modelcontextprotocol/server-puppeteer`    | Fallback scraper |
| fetch      | `uvx mcp-server-fetch`                              | HTTP fetch (requires `uv` — `pip install uv`) |
| filesystem | `npx -y @modelcontextprotocol/server-filesystem <CWD>` | Scoped file access |
| playwright | `npx @playwright/mcp --headless`                   | Primary browser automation (scrape + screenshot) |

⚠ **The `filesystem` server's allowed path is hard-coded to the original
machine.** On the new machine, change the path in `.mcp.json` to match the
cloned repo location before starting Claude Code, e.g.:

```json
"filesystem": {
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\path\\to\\Demo"]
}
```

`@modelcontextprotocol/server-fetch` does **not** exist on npm — the Fetch MCP
is Python-based (`uvx mcp-server-fetch`). This is why `uv` is a prerequisite.

## 7 · CLI tools to install globally

| Tool         | Version tested | Install on Windows                          |
|--------------|----------------|---------------------------------------------|
| Node.js      | 24.12.0        | https://nodejs.org                          |
| npm          | 11.6.2         | bundled with Node                           |
| Python       | 3.13.5         | https://www.python.org                      |
| pip          | 25.1.1         | bundled with Python                         |
| Git          | any recent     | https://git-scm.com                         |
| ffmpeg       | 8.1            | `winget install Gyan.FFmpeg`                |
| uv           | 0.9.2          | `pip install uv`                            |
| serve        | 14.2.6         | `npm i -g serve`                            |
| http-server  | 14.1.1         | `npm i -g http-server`                      |
| ImageMagick  | *(optional)*   | `winget install ImageMagick.ImageMagick`    |

`sharp` (npm) is installed per-project and handles most raster work without
ImageMagick.

## 8 · Key technical decisions (so you don't re-litigate)

1. **Single-file trailer** — no build step, no bundler. Opens straight from
   `file://` or a static server. GSAP is loaded from cdnjs; if you need
   offline, swap to `assets/gsap.min.js` (download path already in SETUP_REPORT).
2. **GSAP over CSS-only animation** — precise 30s timeline with synchronised
   scene transitions is too brittle in pure CSS keyframes.
3. **SVG rotation pivot fix** — for Scene 3's rotating platform, GSAP bypasses
   CSS `transform-box` for SVG elements and writes to the SVG `transform`
   attribute directly. Use `svgOrigin: '0 0'` in GSAP tweens (viewBox
   coordinates) — **not** CSS `transform-origin`. The wrong fix wasted an
   iteration; this comment is the payoff.
4. **Images from filesize is a poor proxy for quality.** Use
   `_rank_images.py` which ranks by pixel count and assigns slots.
5. **Clean URLs in `serve` strip query strings on redirect.** Always navigate
   to `/trailer` (without `.html`) when using `?exact` or `?seek=N` flags, or
   run `serve` with `--no-clean-urls`.
6. **Chrome background-tab throttling** stretches animations during headless
   screenshot polling. `?seek=N` pauses the timeline at a specific frame — use
   it, don't rely on `wait_for` timing.
7. **Accent colour is one CSS variable.** Don't grep-and-replace — just edit
   `--accent` at the top of `<style>`.

## 9 · Dev-URL flags (live on `trailer.html`)

| Flag         | Effect |
|--------------|--------|
| `?exact`     | Disable fit-to-viewport scale. Renders at native 1080×1920. |
| `?seek=12.5` | Pause the timeline at 12.5s. Perfect for poster-frame review. |
| `R` key      | Reload the page (re-run the trailer). |

## 10 · What *not* to do

- ❌ Don't commit `node_modules/`, `.venv/`, `.remember/`, `.playwright-mcp/`, or
   the per-scene temp screenshots — all in `.gitignore`.
- ❌ Don't replace GSAP with a custom requestAnimationFrame loop. The 30-second
   timing, easing, and scene transitions are finely tuned and well worth the
   47KB of GSAP.
- ❌ Don't convert the trailer to a React/Next app. Single HTML is a deliberate
   constraint — it screen-records cleanly from any browser on any box.
- ❌ Don't push to the `main` branch without re-running the RECORDING.md
   verification loop — tiny CSS tweaks can break scene transitions in subtle
   ways (e.g. `will-change` interactions with `mix-blend-mode`).

## 11 · Handy one-liners

```bash
# refresh scraped assets
python scrape_images.py && python _rank_images.py

# start dev server (background, Windows bash)
npx serve . -p 3000 --no-clipboard &

# kill it
taskkill //F //IM node.exe          # Windows
pkill -f "serve"                     # macOS/Linux

# open the trailer in default browser (Windows)
start "" "http://localhost:3000/trailer?exact"
```
