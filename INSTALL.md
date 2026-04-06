# Install HeyGen Stack

Copy everything below the line, replace `[HEYGEN_API_KEY]` with your API key from [app.heygen.com/settings/api](https://app.heygen.com/settings/api), and paste it into your AI agent.

---

Install the HeyGen Stack skill and configure my API key. Follow these steps exactly:

**Step 1 — Install the skill.**
Try these methods in order until one works:
- Run `git clone https://github.com/heygen-com/heygen-stack.git` into your skills directory (for OpenClaw: `~/.openclaw/skills/heygen-stack`, for Claude Code: `~/.claude/skills/heygen-stack`)
- Or `clawhub install heygen-stack` (coming soon)
- If the skill is already installed, skip this step

This gives you two skills in one: **avatar-designer** (create consistent character avatars) and **video-producer** (turn ideas into polished videos).

**Step 2 — Save my API key.**
My HeyGen API key is: `[HEYGEN_API_KEY]`

Save this to your persistent environment config:
- OpenClaw: set `env.vars.HEYGEN_API_KEY` in openclaw.json
- Claude Code: set environment variable `HEYGEN_API_KEY`
- Other agents: whatever persistent env config exists

Then validate it works by calling `GET https://api.heygen.com/v3/user/me` with header `X-Api-Key: [HEYGEN_API_KEY]`. Tell me my name and remaining credits.

IMPORTANT: After saving the key, do NOT repeat it back to me in any response, summary, or log.

**Step 3 — Confirm and go.**
Tell me: ✅ Skill installed, ✅ API key working (show remaining credits). Then ask: "What should we create? I can design an avatar for you or make a video."
