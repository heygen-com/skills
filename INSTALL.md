# Install HeyGen Skills

Grab an [API key](https://app.heygen.com/api) and set it in your shell. If you're already on a HeyGen plan with MCP connected to your agent, you can skip the key — MCP will be used automatically.

## Option 1 — `gh skill`

If your agent supports `gh skill`, you can install the packaged bundle directly with GitHub CLI.

```bash
gh skill install heygen-com/skills heygen-skills
```

With `gh skill`:

- GitHub CLI handles the destination path automatically
- installs can be pinned to tags or commits
- `gh skill update` gives a standard update path
- GitHub-native release controls are available

This installs the packaged skill bundle from `skills/heygen-skills/`.

Update later with:

```bash
gh skill update heygen-skills
```

## Option 2 — ClawHub

```bash
clawhub install heygen-skills
```

Use this if you already rely on ClawHub as your skill distribution channel.

## Option 3 — Manual copy

For agents without either install path, first clone the repo somewhere local, then copy `skills/heygen-skills/` into the agent's local skills directory.

```bash
git clone --depth 1 https://github.com/heygen-com/skills.git /tmp/heygen-skills
```

**OpenClaw** (default: `~/.openclaw/skills/heygen-skills`, custom installs may differ — check your config):
```bash
cp -R /tmp/heygen-skills/skills/heygen-skills ~/.openclaw/skills/heygen-skills
```

**Claude Code** (default: `~/.claude/skills/heygen-skills`):
```bash
cp -R /tmp/heygen-skills/skills/heygen-skills ~/.claude/skills/heygen-skills
```

## Auth

Two auth modes with explicit priority:

| Priority | Mode | Trigger | Billing |
|----------|------|---------|---------|
| 1 | **CLI (API key)** | `HEYGEN_API_KEY` is set | Direct API usage (separately billed) |
| 2 | **MCP (OAuth)** | MCP tools visible AND no API key | HeyGen plan credits (existing subscription) |
| 3 | **CLI (fallback)** | `heygen auth login` session | Direct API usage |

**CLI with API key (recommended for agents):**
```bash
curl -fsSL https://static.heygen.ai/cli/install.sh | bash
export HEYGEN_API_KEY=<your-key>
heygen --version        # verify binary is on PATH
heygen auth status      # verify auth
```

> If `HEYGEN_API_KEY` is set, the skills use the CLI. This is the most predictable setup for agent workflows.

**MCP (zero-setup if on a HeyGen plan):** connect HeyGen's remote MCP server to your agent — OAuth handles auth, calls use your existing plan credits. See README for agent-specific setup.

## First Run

Paste this prompt to your agent — it will find the right paths automatically:

> Install the HeyGen Skills from https://github.com/heygen-com/skills using either `gh skill install heygen-com/skills heygen-skills` or `clawhub install heygen-skills`. Install the HeyGen CLI via `curl -fsSL https://static.heygen.ai/cli/install.sh | bash` and export HEYGEN_API_KEY=\<your-key\> (get one at https://app.heygen.com/api). Or, if you're on a HeyGen plan and already have MCP connected to your agent, skip the key step — MCP will be used automatically. Then use the heygen-avatar skill to create an avatar for me, and heygen-video to make a 30-60 second intro video, casual tone.
