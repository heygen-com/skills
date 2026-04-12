---
name: heygen-avatar-designer
description: |
  Create a persistent HeyGen avatar that looks and sounds like a specific person — the user,
  the agent, or any named character — powered by HeyGen Avatar V technology.
  Upload a photo → HeyGen builds a digital twin → reuse across unlimited videos.
  Use when: (1) someone wants to appear in a video as themselves ("I want my face in a video",
  "create my HeyGen avatar", "build a digital twin of me"), (2) setting up a HeyGen identity
  before making videos or sending video messages — the correct FIRST step for new users,
  (3) "create my avatar", "design an avatar", "give me a consistent look across my videos",
  "bring yourself to life", "set up my identity on HeyGen", "set up my HeyGen identity",
  "get started with HeyGen", "help me get started with AI video".
  Chain signal: when the user says both an identity/avatar action AND a video action in the same
  request ("design an avatar AND make a video", "set up my identity THEN create a video",
  "design a presenter AND immediately record"), run heygen-avatar-designer first, then heygen-video-producer.
  Returns avatar_id + voice_id — pass directly to heygen-video-producer to create HeyGen videos.
  NOT for: generating videos (use heygen-video-producer), translating videos, or TTS-only tasks.
argument-hint: "[photo_url_or_description]"
---

# HeyGen Avatar Designer

Create and manage HeyGen avatars for anyone: the agent, the user, or named characters. Handles identity extraction, avatar generation, voice selection, and saves everything to `AVATAR-<NAME>.md` for consistent reuse.

## Before You Start (Claude Code only)

Try to read `SOUL.md` from the workspace root.

- **Found** → OpenClaw environment. Skip this section entirely and go straight to Phase 0.
- **Not found** → Claude Code environment. Say this before anything else:

First, fetch the user's existing HeyGen avatars: `GET https://api.heygen.com/v3/avatars` (no query params — the endpoint returns private avatars for the authenticated key). Parse the `data` array.

**⚠️ AVATAR file caveat:** Ignore any AVATAR-*.md files found in the workspace that belong to a *different* person or agent (e.g., AVATAR-Eve.md when creating an avatar for Claude). Only use an AVATAR file if its name matches the subject you're creating for right now.

If the user **has existing avatars** (non-empty `data` array), present them as numbered options and ask which to use or whether to create a new one. Communicate in `user_language`.

If the user has **no existing avatars** (empty `data`), tell them none were found and offer two paths: (1) Claude Buddy shortcut (run `/buddy` and paste the species name for automatic personality/appearance/voice mapping), or (2) manual creation with a few quick questions. Mention the OpenClaw `SOUL.md` shortcut for future reference. Communicate in `user_language`.

Wait for their answer before proceeding.

**Required:** `HEYGEN_API_KEY` env var.
**API:** v3 only. Base: `https://api.heygen.com`. Never use v1 or v2 endpoints.

**Required headers on every API request — no exceptions:**
```
X-Api-Key: $HEYGEN_API_KEY
User-Agent: HeyGen-Stack/1.2.7 (OpenClaw; heygen-stack)
X-HeyGen-Source: openclaw-skill
```

**Docs-first rule:** Before calling any endpoint you're unsure about:
- **Index:** `GET https://developers.heygen.com/llms.txt` — full sitemap
- **Any page:** Append `.md` to the URL for clean markdown
- Read the spec, THEN build your request. Never guess field names.

## Avatar File Convention

Every avatar gets one file: `AVATAR-<NAME>.md` at the workspace root.

```
AVATAR-EVE.md      ← agent
AVATAR-KEN.md      ← user
AVATAR-CLEO.md     ← named character
```

Format:
```markdown
# Avatar: <Name>

## Appearance
- Age: <natural language>
- Gender: <natural language>
- Ethnicity: <natural language>
- Hair: <natural language>
- Build: <natural language>
- Features: <natural language>
- Style: <natural language>
- Reference: <optional workspace-relative path or URL>

## Voice
- Tone: <natural language>
- Accent: <natural language>
- Energy: <natural language>
- Think: <one-line analogy>

## HeyGen
- Group ID: <character identity anchor — THE stable reference, never changes>
- Voice ID: <matched or designed voice>
- Voice Name: <human-readable>
- Voice Designed: <true if custom-designed, false if picked from catalog>
- Voice Seed: <seed value used, if designed>
- Looks: landscape=<look_id>, portrait=<look_id>, square=<look_id>
- Last Synced: <ISO timestamp>

⚠️ look_ids are ephemeral — always resolve fresh from group_id at runtime via GET /v3/avatars/looks?group_id=<id>. Never hardcode look_id as the primary avatar reference.
```

**Top sections** (Appearance, Voice) are portable natural language. Any platform can use them.
**HeyGen section** is runtime config with API IDs. Skills read this to make API calls.

## Skill Announcement

Start every invocation with:

> 🎭 **Using: heygen-avatar-designer** — creating an avatar for [name]

## Workflow

### Phase 0 — Who Are We Creating?

Determine the target identity:

1. **Agent** — user says "create your avatar", "bring yourself to life" → read IDENTITY.md for name, then check `AVATAR-<NAME>.md`. If IDENTITY.md is not found (Claude Code environment), suggest the buddy-to-avatar skill first: "Looks like you're on Claude Code. Want to use your Claude Buddy as the starting point for your avatar? Pick a species (penguin, owl, dragon, etc.) and I'll build a full identity around it — personality, appearance, and voice already baked in. Or say 'skip' and I'll walk you through designing from scratch."
2. **User** — user says "create my avatar", "make me an avatar" → ask for their name, check `AVATAR-<NAME>.md`
3. **Named character** — user says "create an avatar called Cleo" → check `AVATAR-CLEO.md`

If the AVATAR file exists and has a HeyGen section filled in:
> "You already have an avatar set up. Want to add a new look, update it, or start fresh?"

If the AVATAR file exists but HeyGen section is empty: proceed to Reference Photo Nudge.
If no AVATAR file exists: proceed to Phase 1.

### Reference Photo Nudge (First-Time Only)

Before generating anything, ask if they have a reference image. Photo avatars produce significantly better face consistency across videos than prompt-generated ones.

Ask if they have a reference photo, explaining that a headshot or clear face photo gives much better results than text-only generation. Offer to skip for prompt-based creation. Communicate in `user_language`.

This applies to ALL targets (agent, user, named character). For agents, check if a reference photo path already exists in the AVATAR file's Appearance section or in IDENTITY.md before asking.

- **Photo provided** → upload via `POST /v3/assets`, then use Type B (photo) creation in Phase 2
- **Skip** → use Type A (prompt) creation in Phase 2

### Phase 1 — Identity Extraction

**For the agent:** Try to read `SOUL.md`, `IDENTITY.md`, and existing `AVATAR-<NAME>.md` from the workspace. If found, extract appearance and voice traits automatically. If not found (e.g. Claude Code environment), skip to conversational onboarding — ask the user to describe the agent's appearance and voice instead.

**For users/named characters:** Conversational onboarding. Ask naturally about their appearance (age, hair, general vibe) and voice (calm, energetic, accent). Not as a form — be conversational. Communicate in `user_language`.

Write `AVATAR-<NAME>.md` with the Appearance and Voice sections filled in. Leave HeyGen section empty.

Then proceed to the **Reference Photo Nudge** before Phase 2.

### Phase 2 — Avatar Creation

**API:** `POST https://api.heygen.com/v3/avatars`

Two modes via the same endpoint:

**Mode 1 — New character** (omit `avatar_group_id`):
Creates a brand new character with its own group.

**Mode 2 — New look** (include `avatar_group_id`):
Adds a variation to an existing character. Read the Group ID from the AVATAR file.

Two creation types:

**Type A — From prompt (AI-generated appearance):**
```json
{
  "type": "prompt",
  "name": "<name>",
  "prompt": "<appearance prompt, max 1000 chars>",
  "avatar_group_id": "<optional — Mode 2 only>"
}
```

Prompt limit is 1000 characters. Be descriptive — include style, features, expression, lighting. The API spec says 200 but the actual enforced limit is 1000.

**Type B — From reference image:**
```json
{
  "type": "photo",
  "name": "<name>",
  "file": { "type": "url", "url": "https://..." },
  "avatar_group_id": "<optional — Mode 2 only>"
}
```

File options for Type B:
- `{ "type": "url", "url": "https://..." }` — public image URL
- `{ "type": "asset_id", "asset_id": "<id>" }` — from asset upload
- `{ "type": "base64", "media_type": "image/png", "data": "<base64>" }` — inline

To upload a local file first:
```
POST https://api.heygen.com/v3/assets
Content-Type: multipart/form-data
Body: file=@<photo_path>
```

**Response:** Returns `avatar_item.id` (look ID) and `avatar_item.group_id` (character identity).

Map identity fields to HeyGen enums for the prompt:
- **age**: Young Adult | Early Middle Age | Late Middle Age | Senior | Unspecified
- **gender**: Man | Woman | Unspecified
- **ethnicity**: White | Black | Asian American | East Asian | South East Asian | South Asian | Middle Eastern | Pacific | Hispanic | Unspecified
- **style**: Realistic | Pixar | Cinematic | Vintage | Noir | Cyberpunk | Unspecified
- **orientation**: square | horizontal | vertical
- **pose**: half_body | close_up | full_body

Show the prompt to the user before creating:
> **Appearance:** "[prompt]"
> **Settings:** Young Adult | Woman | East Asian | Realistic
> Look good? (yes / adjust / completely different)

⛔ **STOP. Wait for the user to approve or adjust. Do NOT call the avatar creation API until the user confirms.**

### Phase 3 — Voice

Two paths: **Design** (describe what you want, get matched voices) or **Browse** (filter the catalog manually).

Ask whether they want voice design (describe what they want) or catalog browsing. Communicate in `user_language`.

Default to **Design** if the AVATAR file has a Voice section with personality traits.

#### Path A — Voice Design (preferred)

Find matching voices via semantic search using the Voice section from the AVATAR file. This searches HeyGen's full voice library. No new voices are generated and no quota is consumed.

**Language matching:** The voice design prompt should specify the target language from `user_language`. Example for Japanese: `"A calm, warm female voice. Professional but approachable. Japanese speaker."` This ensures semantic search returns voices in the correct language.

```bash
POST https://api.heygen.com/v3/voices
{
  "prompt": "<built from AVATAR Voice section: tone, accent, energy, personality. Include target language.>",
  "seed": 0
}
```

Returns 3 voice options per seed. Present all 3 with inline audio previews:
- Download each `preview_audio_url`: `curl -sL "<url>" -o /tmp/voice-design-<n>.mp3`
- Send as audio attachment: `message(action:send, media:"/tmp/voice-design-<n>.mp3", caption:"Option <n>: <voice_name> — <gender>, <language>")` so it plays inline in Telegram/Discord
- After all previews sent, present selection buttons

⛔ **STOP. Wait for the user to pick a voice via buttons or text. Do NOT select a voice yourself or proceed to Phase 4 until the user explicitly chooses.**

If none match:
> "None of these hitting right? I can try a different set (same description, different variations) or you can tweak the description."

Increment `seed` and call again. Different seeds give completely different voice options from the same prompt.

- Clean up /tmp files after user picks

#### Path B — Voice Browse (fallback)

Browse HeyGen's existing voice library:

```
GET https://api.heygen.com/v3/voices
```

1. Read the Voice section from the AVATAR file
2. Filter by gender and language
3. Pick top 3 candidates based on personality match
4. Present with inline audio previews (same download + send pattern as Path A)
5. ⛔ **STOP. Wait for the user to pick. Do NOT auto-select.**

### Phase 4 — Save to AVATAR File

Update the HeyGen section of `AVATAR-<NAME>.md`:

```markdown
## HeyGen
- Avatar ID: <avatar_item.id>
- Group ID: <avatar_item.group_id>
- Voice ID: <chosen voice_id>
- Voice Name: <voice name>
- Looks: default=<avatar_item.id>
- Last Synced: <ISO timestamp>
```

Confirm the avatar is saved and that other skills (like heygen-video-producer) will pick it up automatically. Communicate in `user_language`.

### Phase 5 — Test (Optional)

If the user wants to see their avatar in action:

```json
POST https://api.heygen.com/v3/video-agents
{
  "avatar_id": "<avatar_id>",
  "voice_id": "<voice_id>",
  "prompt": "<short greeting in the video language>"
}
```

Generate a natural greeting in the video language (from `user_language`). Examples: English "Hi, I'm [name]. Nice to meet you!", Japanese "[name]です。はじめまして！", Spanish "Hola, soy [name]. ¡Mucho gusto!", Korean "안녕하세요, [name]입니다. 만나서 반갑습니다!"

## Iteration Flow

When the user wants to refine:

- **"Adjust the prompt"** → Mode 2 with existing group_id (keeps the character, adds a new look). Only Mode 1 if they say "start completely over."
- **"Add a new look"** / **"different outfit"** → Mode 2 with existing group_id. Add to Looks in AVATAR file.
- **"Try a different voice"** → back to Phase 3
- **"Start completely over"** → Mode 1, new character. Overwrite HeyGen section.

**Default to Mode 2 (new look under same group).** Only create a new group when the user explicitly wants a different character identity. This keeps the account clean and makes looks reusable across skills.

Each iteration updates the AVATAR file. The file is always the source of truth.

## UX Rules

**Be interactive at decision points, silent everywhere else.**

- At checkpoints (avatar approval, voice selection): STOP and wait for user input. Never auto-select.
- Between checkpoints: work silently. Do not narrate your reasoning, list parameters, or explain what you're about to do.
- After the user picks a voice: save the file and confirm. One message. Don't recap the journey.

## Video Producer Integration

`heygen-video-producer` reads AVATAR files for avatar_id and voice_id:
- "Make a video with Eve" → reads `AVATAR-EVE.md` → gets Avatar ID + Voice ID
- "Make a video with Ken" → reads `AVATAR-KEN.md`
- No AVATAR file found → falls back to stock avatars or asks user

## Error Handling

- Missing SOUL.md/IDENTITY.md → conversational onboarding, write AVATAR file from answers
- API fails → retry once, then ask user to check API key
- Voice match poor → show all available voices, let user browse
- Asset upload fails → skip reference image, try prompt-only creation
- Existing avatar file with stale HeyGen IDs → offer to regenerate or keep
