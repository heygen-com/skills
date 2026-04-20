# HeyGen Skills

AI agent skills for creating avatar videos. Your agent gets a face, a voice, and the ability to send video like a message.

Works with Claude Code, OpenClaw, Codex, Cursor, and other AI coding agents.

```
"Bring yourself to life — create your own avatar and make a 30-second intro video of yourself. Use heygen-avatar and heygen-video, ask me anything before you start."
→ reads your agent's identity files → asks only what's missing → builds the agent's avatar → picks the best style → generates the video → delivers the share link
```

## Install

Paste this into your agent to get started:

```
Install HeyGen Skills from https://github.com/heygen-com/skills with gh skill install heygen-com/skills heygen-skills. Install the HeyGen CLI from https://static.heygen.ai/cli/install.sh and export HEYGEN_API_KEY=<your-key> (get one at https://app.heygen.com/api). Or, if you're on a HeyGen plan and already have MCP connected to your agent, skip the key step — MCP will be used automatically. Then use heygen-avatar and heygen-video to bring yourself to life — create your own avatar and make a short cinematic intro video of yourself introducing who you are. Ask me what you need before starting.
```

Or follow the steps below manually.

### Step 1 — Install with `gh skill`

If your agent supports `gh skill`, this is the preferred install path.

```bash
gh skill install heygen-com/skills heygen-skills
```

Why this is the preferred path for supported agents:

- GitHub CLI handles the correct install directory for Claude Code, Codex, Cursor, and other supported agents
- installs can be pinned to tags or commits
- `gh skill update` gives a standard update path
- GitHub-native release controls such as immutable releases and provenance are a better fit for enterprise environments

This installs the packaged skill bundle from `skills/heygen-skills/`.

Update later with:

```bash
gh skill update heygen-skills
```

### Step 1b — Alternate install paths

If you already use ClawHub, you can install from there instead:

```bash
clawhub install heygen-skills
```

If your agent does not support `gh skill`, use a manual copy by placing `skills/heygen-skills/` into whatever directory that agent uses for local skills.

### Step 2 — Get your HeyGen API key

1. Go to **[app.heygen.com/api](https://app.heygen.com/api)** (Settings → API)
2. Generate a new API key
3. Save it somewhere safe — you can't view it again after the modal closes

### Step 3 — Install the HeyGen CLI

One-line install (macOS / Linux):

```bash
curl -fsSL https://static.heygen.ai/cli/install.sh | bash
```

Then set your API key:

```bash
export HEYGEN_API_KEY=<your-key>
```

That's ephemeral (current shell only). To persist across sessions, add `export HEYGEN_API_KEY=<your-key>` to your shell profile (`~/.zshrc`, `~/.bashrc`, or equivalent).

Verify:

```bash
heygen --version
heygen auth status
```

The [HeyGen CLI](https://github.com/heygen-com/heygen-cli) is a single static binary. No runtime deps.

### Alternative: MCP (OAuth, no API key)

If you prefer OAuth and already have a HeyGen plan with credits, connect the remote MCP server instead of setting an API key. The skills will auto-detect MCP when no `HEYGEN_API_KEY` is set.

Claude Code:
```bash
claude mcp add --transport http heygen https://mcp.heygen.com/mcp/v1/
```

OpenClaw: add to `~/.openclaw/openclaw.json`:
```json
{
  "mcp": {
    "servers": {
      "heygen": { "url": "https://mcp.heygen.com/mcp/v1/" }
    }
  }
}
```

The first call triggers an OAuth consent flow in your browser.

> **Priority:** If `HEYGEN_API_KEY` is set, the skills use the CLI. Otherwise they look for MCP tools. Set the key only if you want direct API access; otherwise use MCP.

### Step 4 — Create your avatar

Ask the user for a photo (URL or file), then use the **heygen-avatar** skill:

> Create my HeyGen avatar from this photo: [user's photo]

The skill uploads the photo, creates a persistent digital twin with a voice, and saves an `AVATAR-<NAME>.md` file for future use.

### Step 5 — Make your first video

Use the **heygen-video** skill to generate an intro video with the avatar you just created:

> Make a 30-60 second video of me introducing myself, casual tone.

The skill picks up the avatar automatically, writes a script, generates the video, and returns a share link.

**That's it. You're set up.** The avatar persists — every future video reuses it automatically.

---

## What's Included

Two skills that work standalone or chain together:

| Skill | What it does | Invoke |
|-------|-------------|--------|
| **heygen-avatar** | Photo → persistent digital twin (face + voice). Reusable across every video. | `/heygen-avatar` |
| **heygen-video** | Idea → script → prompt-engineered video with your avatar delivering the message. | `/heygen-video` |

**heygen-avatar** creates the identity. **heygen-video** uses it.

## How It Works

```
Photo / Description          Avatar File              Finished Video
       ↓                        ↓                        ↓
  heygen-avatar    →    AVATAR-NAME.md       →    heygen-video
  (identity + voice)    (reusable state)          (script + video)
```

Skills communicate through `AVATAR-<NAME>.md` files. heygen-avatar writes them, heygen-video reads them. Human-readable and machine-readable.

## Authentication

The skills support two auth modes with explicit priority:

| Priority | Mode | Trigger | Billing | Best for |
|----------|------|---------|---------|----------|
| 1 | **CLI (API key)** | `HEYGEN_API_KEY` is set | Direct API usage ($, separately billed) | Agents, CI, scripts |
| 2 | **MCP (OAuth)** | MCP tools visible AND no API key | HeyGen plan credits (no extra billing) | Users on a HeyGen plan |
| 3 | **CLI (fallback)** | `heygen auth login` session | Direct API usage ($) | Interactive CLI users |

**Billing tradeoff:** CLI mode bills against your HeyGen API usage (separately metered). MCP mode consumes your existing HeyGen plan credits — no extra API billing. Pick the mode that matches how you want to be charged.

### CLI with API key (recommended for agents)

Get a key at **[app.heygen.com/api](https://app.heygen.com/api)**, then:

```bash
export HEYGEN_API_KEY=your-key-here
```

If `HEYGEN_API_KEY` is set, the skills use the CLI directly. No MCP probing. This is the most predictable setup for agent workflows.

The [HeyGen CLI](https://github.com/heygen-com/heygen-cli) pattern is `heygen <noun> <verb>`. Output is JSON on stdout with stable exit codes.

- **Verify**: `heygen auth status`
- **Alternative login**: `heygen auth login` — interactive browser flow, persists to `~/.heygen/credentials`

### MCP (OAuth, no API key)

If you don't set an API key and HeyGen's remote MCP server is connected to your agent, the skills use MCP via OAuth. Calls run against your existing HeyGen plan credits.

- Endpoint: `https://mcp.heygen.com/mcp/v1/`
- Tool namespace: `mcp__heygen__*`
- [MCP docs](https://developers.heygen.com/docs/mcp-remote)

You can have both configured — if `HEYGEN_API_KEY` is set, CLI wins.

## Things to Try

After setup, try these prompts with your agent:

| Prompt | What happens |
|--------|-------------|
| "Use heygen-avatar and heygen-video to make a 30-second cinematic intro of me as a founder. Ask me what you need." | Full pipeline: avatar → style recommendation → video. The wow moment. |
| "I want to make a product launch video. Use heygen-video and suggest the best style for it." | Skill recommends from 20 curated styles (A24, editorial, clean tech, etc.) |
| "Use heygen-avatar — I have a headshot. What kind of look would work best for a founder intro?" | Skill asks questions, recommends setting and tone before creating |
| "Use heygen-video to summarize this article as a 60-second explainer from my avatar: [URL]" | Fetches content, extracts key points, scripts and generates the video |
| "Use heygen-video to turn the key points from this PDF into a video update for my team: [file]" | PDF → script → avatar video. Any content becomes a video message. |
| "Use heygen-video for my team's weekly update. Ask me what shipped before writing the script." | Skill interviews you first, then writes and generates |
| "Use heygen-video to make a 20-second outreach video to a potential investor. What should I include?" | Skill guides the message, you approve the script, avatar delivers it |
| "Use heygen-avatar to give me a new look — ask me what vibe I'm going for." | Discovery flow: skill suggests options (outdoor, studio, casual, cinematic) before committing |

## Requirements

- A HeyGen account — sign in via MCP (OAuth) or with an [API key](https://app.heygen.com/api) if you use the CLI fallback
- An AI agent that supports skills (Claude Code, OpenClaw, Codex, Cursor, or similar)
- No runtime dependencies. No packages. No build step.

## Packaging Notes

The canonical installable package now lives at `skills/heygen-skills/`.

- `gh skill install heygen-com/skills heygen-skills` installs that package directly
- relative references stay intact because the package preserves the existing internal layout:
  `heygen-avatar/`, `heygen-video/`, `references/`, `scripts/`, and platform-specific skill files
- the repo root is now documentation and release plumbing, not the install target

## Security

One optional shell script:

- **`skills/heygen-skills/scripts/update-check.sh`** — compares your local `VERSION` against the latest on GitHub. Read-only, opt-in, no data transmitted.

Data only leaves your machine through MCP / the `heygen` CLI (video generation) and optionally `raw.githubusercontent.com` (version check).

## Looking for the v1 skills?

The previous version of this repo had individual skills for TTS, video translation, faceswap, video editing, and more. Those skills are preserved at [heygen-com/skills-legacy](https://github.com/heygen-com/skills-legacy).

## Links

- [HeyGen API Docs](https://developers.heygen.com/docs/quick-start)
- [Repository](https://github.com/heygen-com/skills)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

MIT
