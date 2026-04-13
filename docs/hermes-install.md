# HeyGen Stack — Hermes Agent Install

## Install

```bash
hermes skills install heygen-com/heygen-stack
```

## Required Environment

Set your HeyGen API key before using the skill:

```bash
export HEYGEN_API_KEY="your-api-key-here"
```

Get your key from [app.heygen.com/settings/api](https://app.heygen.com/settings?nav=API).

## Usage

Once installed, invoke the skills via slash commands:

| Command | What It Does |
|---------|-------------|
| `/heygen:avatar-designer` | Create a digital twin avatar from a photo |
| `/heygen:video-producer` | Produce a presenter-led video with script, prompt engineering, and delivery |
| `/heygen:buddy-to-avatar` | Turn a Claude Code Buddy into a video avatar |

### Examples

```
/heygen:avatar-designer Create an avatar from this photo
/heygen:video-producer Make a 30-second product demo video
/heygen:buddy-to-avatar Bring my buddy Sparky to life
```

## What Gets Installed

- Root skill: HeyGen Stack (routing and shared config)
- Sub-skill: heygen-avatar-designer (avatar creation pipeline)
- Sub-skill: heygen-video-producer (video production pipeline)
- Sub-skill: buddy-to-avatar (Buddy personification pipeline)

## Tags

`heygen` `avatar` `video` `identity` `digital-twin` `video-message` `presenter` `talking-head`

## More Info

- HeyGen API docs: https://developers.heygen.com/docs/quick-start
- Repository: https://github.com/heygen-com/heygen-stack
