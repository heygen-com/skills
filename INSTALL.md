# Install HeyGen Video Producer

Copy everything below the line and paste it into your AI agent (OpenClaw, Claude Code, Codex, or any agent that supports skills).

---

Install the HeyGen Video Producer skill and set up my API key. Follow these steps exactly:

**Step 1 — Install the skill.**
Try these methods in order until one works:
- Run `clawhub install heygen-video-producer`
- If clawhub is not available, run `git clone https://github.com/heygen-com/heygen-video-producer.git` into your skills directory (for OpenClaw: `~/.openclaw/skills/heygen-video-producer`, for Claude Code: `~/.claude/skills/heygen-video-producer`)
- If the skill is already installed, skip this step

**Step 2 — Check for API key.**
Check if the environment variable `HEYGEN_API_KEY` is already set.
- If it IS set, validate it by calling `GET https://api.heygen.com/v2/user/remaining_quota` with header `X-Api-Key: <key>`. If valid, skip to Step 4.
- If it is NOT set or validation fails, continue to Step 3.

**Step 3 — Get my API key.**
Ask me to go to https://app.heygen.com/settings/api, copy my API key, and paste it here. When I paste it:
- Validate it with `GET https://api.heygen.com/v2/user/remaining_quota` (header `X-Api-Key: <key>`)
- If valid, save it to the agent's environment config (for OpenClaw: `env.vars.HEYGEN_API_KEY` in openclaw.json; for Claude Code: environment variable; for others: whatever persistent env config exists)
- If invalid, tell me and ask me to try again
- IMPORTANT: After saving, do NOT repeat my API key back to me, do not log it, do not include it in any summary or memory

**Step 4 — Confirm and go.**
Tell me:
- ✅ Skill installed
- ✅ API key working (show my remaining credits)
- Then ask: "What video should we make?"
