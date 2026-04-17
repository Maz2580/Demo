# Environment Setup Report
Date: 2026-04-17
Project: Australian Turntables — AI Trailer
Platform: Windows 11 (bash shell)
Project root: `C:\Users\maz.ghasemi\Downloads\Maz - 2 July 2025\python\demo\`

## CLI Tools
| Tool        | Status | Version                |
|-------------|--------|------------------------|
| Node.js     | ✓      | v24.12.0               |
| npm         | ✓      | 11.6.2                 |
| Python 3    | ✓      | 3.13.5 (via `.venv`)   |
| pip         | ✓      | 25.1.1                 |
| ffmpeg      | ✓      | 8.1-full_build (Gyan)  |
| uv          | ✓      | 0.9.2                  |
| ImageMagick | ✗      | MISSING (optional)     |
| curl        | ✓      | Windows built-in       |
| Git         | ✓      | available              |

Notes:
- Python runs from the user-provided venv at `.venv\`. The `python3` alias is hijacked by the Microsoft Store shim; use `python` or the venv path.
- ffmpeg was installed via `winget install Gyan.FFmpeg` (version 8.1). The binary is at `C:\Users\maz.ghasemi\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe` and verified working. The new PATH entry is only active after opening a fresh shell.
- `uv` was installed via `pip install uv` (0.9.2) — unlocks the Fetch MCP.
- ImageMagick is still missing but `sharp` covers most raster work, so it is optional.

## Claude Code Skills Installed
| Skill           | Status | Path                                                 |
|-----------------|--------|------------------------------------------------------|
| Frontend Design | ✓      | already available as plugin skill `frontend-design:frontend-design` (no git clone needed; the `anthropics/claude-code-skills` URL does not exist) |
| CSS Animation   | ✓      | `C:\Users\maz.ghasemi\.claude\skills\css-animation\` |
| Frontend Slides | ✓      | `C:\Users\maz.ghasemi\.claude\skills\frontend-slides\` |

## MCP Servers Configured
Config written to project-level `.mcp.json` in the working directory (valid JSON verified).

| Server     | Status | Notes                                                                                   |
|------------|--------|-----------------------------------------------------------------------------------------|
| Puppeteer  | ✓      | `@modelcontextprotocol/server-puppeteer@2025.5.12` installed globally                   |
| Fetch      | ✓      | `uvx mcp-server-fetch` (Python). `uv 0.9.2` installed — will resolve and cache the package on first MCP launch. |
| Filesystem | ✓      | `@modelcontextprotocol/server-filesystem@2026.1.14` installed globally, scoped to this folder |
| Playwright | ✓      | `@playwright/mcp@0.0.70` installed globally + chromium browser installed in venv        |

MCPs load after a Claude Code restart.

## Project npm packages
Dev dependencies in `package.json`: `serve`, `http-server`, `puppeteer`, `playwright`, `sharp`, `axios`, `cheerio` — all present in `node_modules/`.
Global CLIs: `serve@14.2.6`, `http-server@14.1.1`.

## Python venv packages
Installed in `.venv`: `requests`, `Pillow`, `playwright`, `beautifulsoup4`, `httpx`. Playwright chromium installed via `python -m playwright install chromium`.

## Tests
| Test              | Status | Evidence                                                                                |
|-------------------|--------|-----------------------------------------------------------------------------------------|
| Image scraping    | ✓      | `test_scrape.py` downloaded `picsum.photos/800/600` → `assets/images/test.jpg` (55,079 B, valid JPEG 800×600) |
| Local dev server  | ✓      | `npx serve` responded HTTP 200 on port 3000                                             |
| GSAP CDN          | ✓      | `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js` → HTTP 200             |

## Project folder
```
C:\Users\maz.ghasemi\Downloads\Maz - 2 July 2025\python\demo\
├── .mcp.json
├── .venv\                  (pre-existing, user-provided)
├── .remember\              (pre-existing)
├── SETUP_REPORT.md
├── SESSION_LOG.md
├── package.json
├── package-lock.json
├── node_modules\
├── assets\
│   ├── fonts\
│   └── images\
│       └── test.jpg
├── test.html
└── test_scrape.py
```
Structure created: ✓

## Ready to proceed?
**YES — for web/HTML/CSS/JS trailer work.**
The full web stack (Node, browsers, scrapers, dev server, animation CDN, image processing via sharp + Pillow) is ready. Creative build can begin.

**Video encoding is also ready** — ffmpeg 8.1 installed and verified.

## Anything needing manual action
1. **Open a fresh terminal** — winget updated the `PATH` for ffmpeg but existing shells still have the old environment. New bash/PowerShell sessions will resolve `ffmpeg` on PATH directly. Until then, use the absolute path `C:\Users\maz.ghasemi\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe`.
2. **Restart Claude Code** once so `.mcp.json` servers are loaded (Puppeteer, Fetch, Filesystem, Playwright).
3. **ImageMagick (optional)** — only if you hit a raster task `sharp` can't handle: `winget install ImageMagick.ImageMagick`.
4. **Frontend Design skill** — no action: already available as the `frontend-design:frontend-design` plugin skill. The prompt's GitHub URL (`anthropics/claude-code-skills`) returned 404 and is not needed.
5. **Old staging folder** — `C:\Users\maz.ghasemi\projects\at-trailer\` is now a duplicate of the working directory. Safe to delete: `rm -rf /c/Users/maz.ghasemi/projects/at-trailer`.
