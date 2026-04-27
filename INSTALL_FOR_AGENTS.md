# HeyGen Skills — Installation Guide for AI Agents

Read this entire file, then follow the steps. Ask the user for API keys when needed.
Target: ~5 minutes to a fully working HeyGen integration.

This file is the agent-facing companion to [`INSTALL.md`](./INSTALL.md) (human-facing).
Where they overlap, this file is canonical for agent-driven installs.

## Step 0: If you are not Claude Code

Read [`CLAUDE.md`](./CLAUDE.md) at the repo root first. It describes the
runtime contract for these skills (mode detection, hard rules,
transport-only-once). Claude Code reads it automatically; other agents
should fetch it explicitly.

If you fetched this file by URL without cloning yet, the companion files
live at:

- `https://raw.githubusercontent.com/heygen-com/skills/master/CLAUDE.md` — runtime contract for the skills
- `https://raw.githubusercontent.com/heygen-com/skills/master/heygen-avatar/SKILL.md` — avatar creation skill (mode detection ladder, hard rules, full creation workflow)
- `https://raw.githubusercontent.com/heygen-com/skills/master/heygen-video/SKILL.md` — video generation skill (mode detection ladder, hard rules, full producer pipeline)
- `https://raw.githubusercontent.com/heygen-com/skills/master/INSTALL.md` — human-facing install doc

## Step 1: Detect the agent host and pick the install path

Detect which agent is running before cloning. Each host expects skills at a
different path. If you are not sure, ask the user "which AI coding agent are
you running this from?"

| Agent host    | Default install path                          |
|---------------|-----------------------------------------------|
| Claude Code   | `~/.claude/skills/heygen-skills`              |
| OpenClaw      | `~/.openclaw/skills/heygen-skills`            |
| Codex         | `~/.codex/skills/heygen-skills`               |
| Cursor        | `~/.cursor/skills/heygen-skills`              |
| Hermes        | `~/.hermes/skills/heygen-skills`              |
| Other         | Whatever path the host loads skills from. Ask the user. |

OpenClaw users running a workspace-scoped install may have skills under
`~/.openclaw/workspace/skills/heygen-skills` instead — check the value of the
host's `--dir` / `workdir` config. The default above is canonical for
non-workspace installs and matches [`INSTALL.md`](./INSTALL.md).

```bash
# Replace <install-path> with the row from the table above:
git clone --single-branch --depth 1 \
  https://github.com/heygen-com/skills.git \
  <install-path>
```

For OpenClaw users, the **fastest install path is ClawHub** — it short-circuits
Steps 1, 3, and 4 below (clones to the right path, registers with the host, and
sets up the install metadata in one command):

```bash
clawhub install heygen-skills
```

After ClawHub install, jump straight to **Step 2** (API key) and then
**Step 5** (avatar creation).

## Step 2: Get the user's HeyGen API key (or detect MCP)

**First, detect whether the user already has the HeyGen MCP server connected.**
If `mcp__heygen__*` tools are visible in the toolset, MCP is the path of least
resistance — OAuth, no key handling, consumes the user's HeyGen plan credits.

If MCP is detected and the user is happy with it, **skip to Step 5 (avatar creation)**.
But before you do, warn them:

> If you set `HEYGEN_API_KEY` later for any reason, the skill will short-circuit
> MCP detection (per the mode-detection ladder in `heygen-video/SKILL.md` or `heygen-avatar/SKILL.md`) and use the CLI /
> direct-API route instead. MCP plan credits won't be touched. To switch back to
> MCP, unset `HEYGEN_API_KEY`.

**If MCP is not connected**, ask the user for their HeyGen API key. They get
it from [app.heygen.com/api](https://app.heygen.com/api) (Settings → API → New
Key). Tell them: *the key is shown once, copy it before closing the modal.*

The HeyGen API is currently pay-as-you-go in credits — no free tier. Avatar V
costs roughly 6 credits per minute of generated video. Make sure the user has
credits or is on a paid plan before proceeding. Pricing changes; if the user
asks for current rates, point them at
[help.heygen.com/api-pricing](https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained).

## Step 3: Save the API key in the standard location

The key needs to be available to whichever transport the user picks in Step 4.
The safe default is to set it as an environment variable in the user's shell
profile.

```bash
# In ~/.zshrc, ~/.bashrc, or wherever the user's shell loads env vars:
export HEYGEN_API_KEY=hg_...
```

Then ask the user to either restart their shell or `source` the file. The
agent's process inherits the parent shell's env — if the agent runs in a
separate process from the user's terminal, they'll need to restart the agent
host, not just re-source the shell.

If the user prefers a project-local key, drop it in `.env` and tell the user
to never commit it. The `.env.example` file shows the expected variable name.

For the OpenClaw plugin path (Step 4 Option A), the key is read from the same
`HEYGEN_API_KEY` env var. The plugin does not require a separate config step.

## Step 4: Pick a transport

These skills route the actual HeyGen API call through one of three transports.
The skill auto-detects which transport is available at runtime via the
mode-detection ladder in each skill's SKILL.md (e.g. [`heygen-video/SKILL.md`](./heygen-video/SKILL.md) or [`heygen-avatar/SKILL.md`](./heygen-avatar/SKILL.md)):

> 1. **OpenClaw plugin** if `video_generate` exposes `heygen/video_agent_v3`
> 2. **CLI (API-key override)** if `HEYGEN_API_KEY` is set AND `heygen --version` exits 0
> 3. **MCP** if no API key set AND `mcp__heygen__*` tools visible
> 4. **CLI (fallback)** if MCP unavailable AND `heygen --version` exits 0

The critical rule: **setting `HEYGEN_API_KEY` short-circuits MCP detection**.
If the user wants MCP-credit billing, do not set the key.

Pick a transport based on the user's host and preferences:

### Option A: OpenClaw plugin (preferred for OpenClaw users)

Ships HeyGen as a first-class provider for OpenClaw's `video_generate` tool.
Auth, polling, and error handling are native. Cleanest integration.

```bash
openclaw plugins install openclaw-plugin-heygen
```

The plugin reads `HEYGEN_API_KEY` from the environment (set in Step 3).
Restart the gateway to pick up the new provider registration:

```bash
openclaw gateway restart
```

Verify the plugin loaded:

```bash
openclaw plugins list | grep heygen
```

The skill detects the plugin by checking whether `video_generate` exposes
`heygen/video_agent_v3` as a model. When detected, the `heygen-video`
sub-skill routes the final video-generate call through `video_generate(...)`
instead of spawning a CLI process.

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

### Option C: HeyGen MCP server (Claude Desktop, Claude Code with MCP, OpenClaw with MCP)

If MCP is already wired up, the skill detects `mcp__heygen__*` tools and uses
them. No CLI install needed. Auth is OAuth; consumes the user's HeyGen plan
credits (not API credits).

To wire MCP from scratch, follow your agent's MCP setup docs and point it at
`https://mcp.heygen.com/mcp/v1/`. We can not configure that from inside this
skill. See [`INSTALL.md`](./INSTALL.md) for example configs.

## Step 5: Give the agent a face (canonical install outcome)

This is the step the install is actually for. Until now we've installed
files and wired auth. Now we make the thing the user came here for: an
avatar the agent can use to present videos.

**Default subject is the agent, not the user.** The `heygen-avatar`
sub-skill is built around the agent getting a face by default. Route to a
user-avatar only on explicit "my avatar" / "me" / "my photo" language. When
in doubt, make the agent's avatar.

### If you are running in an OpenClaw workspace with `SOUL.md` and `IDENTITY.md`

This is the canonical path. The agent has documented identity files; the
skill reads them and designs a presenter that matches.

Read [`heygen-avatar/SKILL.md`](./heygen-avatar/SKILL.md) and follow Phase 0.
The skill will:

1. Read `SOUL.md` and `IDENTITY.md` from the workspace root.
2. Ask one or two clarifying questions about design direction (not a
   batch form — walk the phases in order, one or two questions at a time).
3. Generate the avatar via the Avatar V pipeline (prompt-based by default;
   photo opt-in only for real-person digital twins).
4. Save `AVATAR-<AGENT-NAME>.md` at the workspace root for future reuse.
5. Maintain the `AVATAR-AGENT.md` symlink (or `AVATAR-USER.md` for
   user-target installs) pointing at the named file, so generic
   self-reference requests ("make a video of yourself" / "my video
   update") resolve without name lookup.
6. Return `avatar_id` + `voice_id` for use in Step 7 (defaults).

On the happy path, this step ends with both a named file (e.g.
`AVATAR-EVE.md`, `AVATAR-ADAM.md`, `AVATAR-CLEO.md`) and a role-based
symlink (`AVATAR-AGENT.md` for agent target, `AVATAR-USER.md` for user
target) at the workspace root. Named files are canonical; symlinks are
pointers that consumer skills (heygen-video) can read for generic
self-reference. Note that the heygen-avatar skill has a Phase 2 STOP gate
before generation; if the user aborts there, no file is written and no
credits are spent. That's the correct behavior — it's a confirmation gate,
not a bug. Resume by re-invoking the sub-skill.

### If you are running outside an OpenClaw workspace (no `SOUL.md`)

Claude Code, Codex, Cursor, and Hermes don't have workspace identity files.
The avatar still gets created, but the skill asks the user for the design
direction directly instead of reading from `SOUL.md`.

Same entry point: read [`heygen-avatar/SKILL.md`](./heygen-avatar/SKILL.md)
and follow Phase 0. The skill detects the missing `SOUL.md` and switches
to Phase 1 conversational onboarding — it asks the user about appearance,
voice, and presenter persona one or two traits at a time, not as a single
batch prompt.

### Skip conditions (rare)

Skip Step 5 only if:

- The user has explicitly said "I already have an avatar, just make a video"
  (they have an existing `avatar_id` / `voice_id` they want to reuse).
- The install is purely scoped to video generation with stock avatars (the
  user picks from HeyGen's catalog per-call).

In either case, jump to Step 6. Otherwise, the install is incomplete
without this step.

## Step 6: Verify the install (opt-in)

Ask the user: **"Want to run a 5-second smoke test? It generates a real
video, costs roughly half a credit, and confirms the integration works
end-to-end."**

If yes, branch on whether Step 5 ran:

**If Step 5 created an avatar:**

```
Use heygen-video to generate a 5-second test clip with the avatar from
AVATAR-<NAME>.md saying "HeyGen install working, ready to ship." Save
the file locally and tell me the path.
```

**If Step 5 was skipped (user has an existing `avatar_id` they want to reuse,
or scoped install to stock avatars):**

```
Use heygen-video to generate a 5-second test clip with avatar_id
<the user's avatar_id> and voice_id <the user's voice_id> saying
"HeyGen install working, ready to ship." Save the file locally and tell
me the path.
```

Expected outcome: a `.mp4` file roughly 1-3 MB, 5 seconds long, with the
avatar speaking the test line.

If the user declines, skip to Step 7. The skill works either way; the smoke
test just removes uncertainty about whether everything is wired correctly.

If the smoke test fails, the most common causes (in order):

1. **`HEYGEN_API_KEY` not in current shell.** Re-source the shell profile or
   restart the terminal / agent host.
2. **No credits on the account.** Tell the user, then point them at
   [app.heygen.com/billing](https://app.heygen.com/billing).
3. **Transport not detected.** Run `heygen --version` (Option B) or check
   `openclaw plugins list` (Option A) to confirm the path exists.
4. **`waiting_for_input` state from the Video Agent.** The skill set
   `mode` incorrectly — see the heygen-video sub-skill's review-checkpoint
   handler. Re-read the sub-skill SKILL.md.

## Step 7: Set agent-wide defaults

This step only applies if **Step 5 ran** (the user has a new
`AVATAR-<NAME>.md`) OR if **the user already has an `avatar_id` / `voice_id`**
they want to reuse on every call. If neither, skip to Step 8.

When it applies, save the ids as defaults so the user doesn't repeat them
per-call.

For the **OpenClaw plugin path** (Option A), use `openclaw config set`:

```bash
openclaw config set plugins.entries.heygen.config.defaultAvatarId "<avatar_id>"
openclaw config set plugins.entries.heygen.config.defaultVoiceId  "<voice_id>"
openclaw config set plugins.entries.heygen.config.defaultStyleId  "<style_id>"
```

For the **CLI path** (Option B), defaults live in `~/.heygen/config` — the
CLI will prompt on first use, or you can run `heygen config set` directly.

For the **MCP path** (Option C), there are no per-skill defaults; the agent
passes avatar / voice ids per call. If Step 5 ran, the `AVATAR-<NAME>.md`
file is the source of truth and the agent reads it on each video
generation. If Step 5 was skipped, the user provides ids per call directly.

## Step 8: Make HeyGen the default video provider (OpenClaw plugin path only)

If the user wants `video_generate(...)` to default to HeyGen when no model is
specified:

```bash
openclaw config set agents.defaults.videoGenerationModel.primary "heygen/video_agent_v3"
```

This is purely an OpenClaw concern and does not affect Claude Code, Codex, or
Cursor users.

## Step 9: Done

The skills now have everything they need: a transport, an authenticated
account, an avatar identity, and (optionally) defaults for repeated use.
Tell the user:

> HeyGen Skills are installed. Your agent now has a face: `AVATAR-<NAME>.md`.
> Try:
> - "Make a 30-second video of yourself introducing what we're working on this week"
> - "Send a video update to the team about today's progress"
> - "Generate a 60-second product walkthrough using my avatar"

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

Re-read the active skill's SKILL.md (`heygen-avatar/SKILL.md` or `heygen-video/SKILL.md`) after the upgrade if the version bumped — the
mode detection ladder occasionally adds new transports (e.g. when MCP support
shipped, when the OpenClaw plugin shipped).

## Troubleshooting

**The agent says HEYGEN_API_KEY is not set, but the user already exported
it.** The export only applies to the shell that ran it. If the agent is in a
separate process (most agents are), the export needs to be in `~/.zshrc` or
`~/.bashrc` and either re-sourced or used in a fresh shell.

**The CLI works in the terminal but the agent says it can't find it.** The
agent's PATH is different from the user's interactive shell. Tell the user
to add `~/.local/bin` (or wherever the CLI lands) to a PATH that the agent
inherits.

**`waiting_for_input` from the Video Agent.** The skill is calling the Video
Agent in chat mode by accident. Re-read the heygen-video sub-skill — it
should always pass `mode: "generate"` for one-shot video creation. If you
patched the sub-skill, you may have introduced this regression.

**MCP tools listed but the skill is using the CLI / plugin instead.** The
skill follows the mode-detection ladder in its SKILL.md (heygen-avatar or heygen-video): plugin → CLI
(API-key override) → MCP → CLI (fallback). **`HEYGEN_API_KEY` being set
short-circuits MCP detection.** If the user wants MCP to be the chosen
transport, unset the env var (`unset HEYGEN_API_KEY`) and re-detect. If the
plugin is also installed, uninstall it (`openclaw plugins uninstall
openclaw-plugin-heygen`) so MCP wins detection.

## What this skill does NOT do

- It does not handle account creation. The user must already have a HeyGen
  account with API access.
- It does not bill or upgrade the user's HeyGen plan. If they run out of
  credits, point them at [app.heygen.com/billing](https://app.heygen.com/billing).
- It does not store or transmit the API key anywhere outside the local agent
  environment. The key stays in the user's shell or in the agent host's
  config; the skill never logs it.
