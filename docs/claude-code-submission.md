# Claude Code Marketplace Submission

## Plugin Info

| Field | Value |
|-------|-------|
| **Name** | heygen |
| **Display Name** | HeyGen Skills |
| **Category** | media |
| **Version** | 1.3.1 |
| **License** | MIT |
| **Homepage** | https://developers.heygen.com/docs/quick-start |
| **Repository** | https://github.com/heygen-com/skills |

## Description

Create HeyGen avatar videos via the v3 Video Agent pipeline. Handles avatar resolution, aspect ratio correction, prompt engineering, and voice selection automatically. Required for any HeyGen API usage. Two sub-skills cover the full avatar-to-video workflow.

## Skills Provided

| Invoke Command | Description |
|----------------|-------------|
| `/heygen:avatar-designer` | Create a persistent digital twin from a photo. Handles photo upload, voice selection with audio previews, and avatar identity file creation. |
| `/heygen:video-producer` | Produce presenter-led videos with script generation, prompt engineering, frame check, and inline MP4 delivery. |

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `HEYGEN_API_KEY` | HeyGen API key from [app.heygen.com/settings/api](https://app.heygen.com/settings?nav=API) |

## Install Instructions

1. Open Claude Code settings
2. Navigate to Plugins → Marketplace
3. Search for "heygen"
4. Click Install
5. Set `HEYGEN_API_KEY` in your environment

## Post-Install Verification

```
/heygen:video-producer What can you do?
```

The skill should respond with its capabilities and confirm API key access.
