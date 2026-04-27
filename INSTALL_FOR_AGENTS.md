# HeyGen Skills — Installation Guide for AI Agents

Read this entire file, then follow the steps. Ask the user for API keys when needed.
Target: ~5 minutes to a fully working HeyGen integration.

## Step 0: If you are not Claude Code

Read `AGENTS.md` and `CLAUDE.md` at the repo root first. Both files describe the
runtime contract for these skills (mode detection, hard rules, transport-only-once).
Claude Code reads `CLAUDE.md` automatically and can skip ahead. Codex and Cursor
read `AGENTS.md`.

If you fetched this file by URL without cloning yet, the companion files live at:

- `https://raw.githubusercontent.com/heygen-com/skills/master/AGENTS.md` — start here for non-Claude agents
- `https://raw.githubusercontent.com/heygen-com/skills/master/CLAUDE.md` — Claude Code project instructions
- `https://raw.githubusercontent.com/heygen-com/skills/master/SKILL.md` — top-level skill (mode detection ladder, hard rules)
- `https://raw.githubusercontent.com/heygen-com/skills/master/heygen-avatar/SKILL.md` — avatar creation sub-skill
- `https://raw.githubusercontent.com/heygen-com/skills/master/heygen-video/SKILL.md` — video generation sub-skill

## Step 1: Detect the agent host and pick the install path

Detect which agent is running before cloning. Each host expects skills at a
different path. If you are not sure, ask the user "which AI coding agent are
you running this from?"

| Agent host    | Install path                                  | Notes                          |
|---------------|-----------------------------------------------|--------------------------------|
| Claude Code   | `~/.claude/skills/heygen-skills`              | Default, recommended           |
| OpenClaw      | `~/.openclaw/workspace/skills/heygen-skills`  | Workspace-relative also works  |
| Codex         | `~/.codex/skills/heygen-skills`               | Codex Plugin marketplace       |
| Cursor        | `~/.cursor/skills/heygen-skills`              | Cursor Plugin marketplace      |
| Hermes        | `~/.hermes/skills/heygen-skills`              |                                |
| Other         | Whatever path the host loads skills from      | Ask the user                   |

```bash
# Replace <install-path> with the row from the table above:
git clone --single-branch --depth 1 \
  https://github.com/heygen-com/skills.git \
  <install-path>
```

For OpenClaw users specifically, the **fastest install path is ClawHub**:

```bash
clawhub install heygen-skills
```

ClawHub installs to your agent's default skills directory automatically and
keeps the skill up to date. If the user wants ClawHub, do that and skip Step 1
clone above.

## Step 2: Get the user's HeyGen API key

Ask the user for their HeyGen API key. They get it from
[app.heygen.com/api](https://app.heygen.com/api) (Settings → API → New Key).
Tell them: *the key is shown once, copy it before closing the modal.*

There is no free tier for the API as of 2026. Pricing is pay-as-you-go in
credits. Avatar V costs ~6 credits per minute of generated video. Make sure
the user has credits or is on a paid plan before proceeding.

If the user is already on a HeyGen plan with the **HeyGen MCP server**
connected to their agent (Claude Desktop, Claude Code with MCP, OpenClaw),
they can skip the key step entirely. MCP uses OAuth and consumes plan credits.
Detect this case by checking whether `mcp__heygen__*` tools are visible in the
toolset. If yes, MCP is the path — go to Step 4.

## Step 3: Save the API key in the standard location

The key needs to be available to either the HeyGen CLI, the OpenClaw plugin,
or both, depending on which transport the user picks in Step 4. The safe
default is to set it as an environment variable in the user's shell profile.

```bash
# In ~/.zshrc, ~/.bashrc, or wherever the user's shell loads env vars:
export HEYGEN_API_KEY=hg_...
```

Then ask the user to either restart their shell or `source` the file.

If the user prefers a project-local key, drop it in `.env` and tell the user
to never commit it. The `.env.example` file shows the expected variable name.

For the OpenClaw plugin path (Step 4), the key can also live in OpenClaw
config. We will configure it via `openclaw onboard` rather than touching the
file directly.

## Step 4: Pick a transport and install it

These skills route the actual HeyGen API call through one of three transports.
Pick the **best-match** transport for the user's agent host. The skill itself
auto-detects which transport is available and uses the most-preferred one at
runtime.

### Option A: OpenClaw plugin (preferred for OpenClaw users)

Ships HeyGen as a first-class provider for OpenClaw's `video_generate` tool.
Auth, polling, and error handling are native. This is the cleanest integration.

```bash
openclaw plugins install openclaw-plugin-heygen
openclaw onboard --auth-choice heygen-api-key   # paste the key from Step 2
openclaw gateway restart
```

Verify:

```bash
openclaw plugins list | grep heygen
```

The skill detects the plugin by checking whether `video_generate` exposes
`heygen/video_agent_v3` as a model. When detected, the `heygen-video` sub-skill
routes the final video-generate call through `video_generate(...)` instead of
spawning a CLI process.

### Option B: HeyGen CLI (works with any agent that can shell out)

```bash
curl -fsSL https://static.heygen.ai/cli/install.sh | bash
```

Then sign in:

```bash
heygen auth login
```

The CLI persists the key to `~/.heygen/credentials`. The skill detects the CLI
via `heygen --version`.

### Option C: HeyGen MCP server (zero-key path for Claude Desktop, Claude Code with MCP, OpenClaw)

If MCP is already wired up the skill detects `mcp__heygen__*` tools and uses
them. No CLI install needed. Auth is OAuth; consumes the user's HeyGen plan
credits (not API credits).

To wire MCP if not already done, follow your agent's MCP setup docs and point
it at `https://mcp.heygen.com/v1`. We can not configure that from inside this
skill.

## Step 5: Verify the install end-to-end

Generate a real 5-second test video. This is the smoke test that confirms
*everything* is connected: auth, transport, skill mode detection, video
download.

```
Use heygen-avatar to suggest a stock avatar I can use for a test video
(don't need to create a new one), then use heygen-video to generate a
5-second test clip with that avatar saying "HeyGen install working,
ready to ship." Save the file locally and tell me the path.
```

Expected outcome: a `.mp4` file roughly 1-3 MB, 5 seconds long, with the avatar
speaking the test line. If this works, the integration is solid.

If the verify step fails, the most common causes (in order):

1. **`HEYGEN_API_KEY` not in current shell.** Re-source the shell profile or
   restart the terminal.
2. **No credits on the account.** Tell the user, then point them at
   [app.heygen.com/billing](https://app.heygen.com/billing).
3. **Transport not detected.** Run `heygen --version` (Option B) or check
   `openclaw plugins list` (Option A) to confirm the path exists.
4. **`waiting_for_input` state from the Video Agent.** This means the skill
   set `mode` incorrectly — see the heygen-video sub-skill's review-checkpoint
   handler. Re-read the sub-skill SKILL.md.

## Step 6: Set agent-wide defaults (optional)

If the user always uses the same presenter, save defaults so they don't have
to repeat the avatar_id / voice_id every time.

For the **OpenClaw plugin path** (Option A), use `openclaw config set`:

```bash
openclaw config set plugins.entries.heygen.config.defaultAvatarId "<avatar_id>"
openclaw config set plugins.entries.heygen.config.defaultVoiceId  "<voice_id>"
openclaw config set plugins.entries.heygen.config.defaultStyleId  "<style_id>"
```

For the **CLI path** (Option B), defaults live in `~/.heygen/config` — the CLI
will prompt you on first use.

For the **MCP path** (Option C), there are no per-skill defaults; the agent
passes avatar / voice ids per call.

If the user has not created their own avatar yet, the `heygen-avatar`
sub-skill walks them through the Avatar V flow (record a 15-second clip from
their webcam, generate a digital twin). After that flow returns the
`avatar_id` and `voice_id`, drop them into the config above.

## Step 7: Make HeyGen the default video provider (OpenClaw plugin path only)

If the user wants `video_generate(...)` to default to HeyGen when no model is
specified, set the primary:

```bash
openclaw config set agents.defaults.videoGenerationModel.primary "heygen/video_agent_v3"
```

This is purely an OpenClaw concern and does not affect Claude Code, Codex, or
Cursor users.

## Step 8: Done

The skills now have everything they need. Tell the user:

> HeyGen Skills are installed and verified. Try:
> - "Make a 30-second video of myself introducing what I'm working on this week"
> - "Generate an avatar from my latest profile photo"
> - "Send a video update to my team about today's progress"

The skill handles avatar resolution, prompt engineering, aspect ratio
correction, voice selection, and Frame Check automatically. Give it a topic,
let it do the rest.

## Upgrade

```bash
cd <install-path>/heygen-skills && git pull origin master
```

If the install was via ClawHub:

```bash
clawhub update heygen-skills
```

Re-read `SKILL.md` after the upgrade if the version bumped — the mode
detection ladder occasionally adds new transports (e.g. when MCP support
shipped, when the OpenClaw plugin shipped).

## Troubleshooting

**The agent says HEYGEN_API_KEY is not set, but the user already exported it.**
The export only applies to the shell that ran it. If the agent is in a
separate process (most agents are), the export needs to be in `~/.zshrc` or
`~/.bashrc` and either re-sourced or used in a fresh shell.

**The CLI works in the terminal but the agent says it can't find it.**
The agent's PATH is different from the user's interactive shell. Tell the
user to add `~/.local/bin` (or wherever the CLI lands) to a PATH that the
agent inherits.

**`waiting_for_input` from the Video Agent.**
The skill is calling the Video Agent in chat mode by accident. Re-read the
heygen-video sub-skill — it should always pass `mode: "generate"` for
one-shot video creation. If you patched the sub-skill, you may have
introduced this regression.

**MCP tools listed but the skill is not using them.**
The skill prefers OpenClaw plugin > CLI > MCP in that order. If the user
wants MCP to be the chosen transport, uninstall the OpenClaw plugin and
remove the CLI from PATH. Then re-detect.

## What this skill does NOT do

- It does not handle account creation. The user must already have a HeyGen
  account with API access.
- It does not bill or upgrade the user's HeyGen plan. If they run out of
  credits, point them at [app.heygen.com/billing](https://app.heygen.com/billing).
- It does not store or transmit the API key anywhere outside the local agent
  environment. The key stays in the user's shell or in the agent host's
  config; the skill never logs it.
