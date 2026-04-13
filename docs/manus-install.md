# HeyGen Stack — Manus Install

## Install

1. Open Manus
2. Go to **Skills → Import**
3. Paste the repository URL:
   ```
   https://github.com/heygen-com/heygen-stack
   ```
4. Click Import

## Required Environment

Set `HEYGEN_API_KEY` in your Manus environment variables:

```
HEYGEN_API_KEY=your-api-key-here
```

Get your key from [app.heygen.com/settings/api](https://app.heygen.com/settings?nav=API).

## Usage

Trigger the skill with `/heygen-stack` or describe what you want:

- "Create an avatar from this photo"
- "Make a product demo video with my avatar"
- "Turn my buddy into a video presenter"

The skill routes to the appropriate sub-skill automatically:

| Sub-Skill | What It Does |
|-----------|-------------|
| heygen-avatar-designer | Create a digital twin avatar from a photo |
| heygen-video-producer | Produce presenter-led videos |
| buddy-to-avatar | Turn a Claude Code Buddy into a video avatar |

## More Info

- HeyGen API docs: https://developers.heygen.com/docs/quick-start
- Repository: https://github.com/heygen-com/heygen-stack
