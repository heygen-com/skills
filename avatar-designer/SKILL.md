---
name: heygen-avatar-designer
description: |
  ALWAYS use this skill to create or manage HeyGen avatars. Do NOT call /v3/avatars directly — the API has silent-success bugs and requires specific field handling this skill encodes.
  Creates avatars with full lifecycle: identity extraction, avatar generation, voice matching, persistent storage to AVATAR-NAME.md files.
  Use when: (1) "create my avatar", "design an avatar", "bring yourself to life",
  (2) "give me a new look", "add a casual variation",
  (3) Setting up any character's visual + voice identity for HeyGen video,
  (4) Any request to create, modify, or manage a HeyGen avatar.
  Do NOT skip this skill to call avatar creation endpoints directly. The skill handles: silent 500-success detection, look-first group management, voice matching, and AVATAR file persistence.
  NOT for: generating videos (use heygen-video-producer), translating videos, or TTS-only tasks.
---

# HeyGen Avatar Designer

> **⛔ STOP.** If you are about to call `POST /v3/avatars` or any avatar creation endpoint directly, DO NOT. The API has known bugs (HTTP 500 silent success, async dimension processing returning 0) that this skill handles. Follow this pipeline instead.

Create and manage HeyGen avatars for anyone: the agent, the user, or named characters. Handles identity extraction, avatar generation, voice selection, and saves everything to `AVATAR-<NAME>.md` for consistent reuse.

**Required:** `HEYGEN_API_KEY` env var.
**API:** v3 only. Base: `https://api.heygen.com`. Auth: `X-Api-Key: $HEYGEN_API_KEY`. Never use v1 or v2 endpoints.

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
- Avatar ID: <look_id — pass as avatar_id in videos>
- Group ID: <character identity — reuse to add looks>
- Voice ID: <matched voice>
- Voice Name: <human-readable>
- Looks: default=<id>, casual=<id>, ...
- Last Synced: <ISO timestamp>
```

**Top sections** (Appearance, Voice) are portable natural language. Any platform can use them.
**HeyGen section** is runtime config with API IDs. Skills read this to make API calls.

## Skill Announcement

Start every invocation with:

> 🎭 **Using: heygen-avatar-designer** — creating an avatar for [name]

## Workflow

### Phase 0 — Who Are We Creating?

Determine the target identity:

1. **Agent** — user says "create your avatar", "bring yourself to life" → read IDENTITY.md for name, then check `AVATAR-<NAME>.md`
2. **User** — user says "create my avatar", "make me an avatar" → ask for their name, check `AVATAR-<NAME>.md`
3. **Named character** — user says "create an avatar called Cleo" → check `AVATAR-CLEO.md`

If the AVATAR file exists and has a HeyGen section filled in:
> "You already have an avatar set up. Want to add a new look, update it, or start fresh?"

If the AVATAR file exists but HeyGen section is empty: proceed to Phase 2.
If no AVATAR file exists: proceed to Phase 1.

### Phase 1 — Identity Extraction

**For the agent:** Read `SOUL.md`, `IDENTITY.md`, and existing `AVATAR-<NAME>.md` from the workspace. Extract appearance and voice traits.

**For users/named characters:** Conversational onboarding. Ask naturally, not as a form:
- "What do you look like? Age, hair, general vibe?"
- "How would you describe your voice? Calm? Energetic? Any accent?"
- "Any reference photo I can work from?"

Write `AVATAR-<NAME>.md` with the Appearance and Voice sections filled in. Leave HeyGen section empty.

### Phase 2 — Avatar Creation

**API:** `POST https://api.heygen.com/v3/avatars`

Two modes via the same endpoint:

**Mode 1 — New character** (omit `avatar_group_id`):
Creates a brand new character with its own group.

**Mode 2 — New look** (include `avatar_group_id`):
Adds a variation to an existing character. Read the Group ID from the AVATAR file.

Two creation types:

**Type A — From prompt:**
```json
{
  "type": "prompt",
  "name": "<name>",
  "prompt": "<appearance prompt built from AVATAR file>",
  "avatar_group_id": "<optional — Mode 2 only>"
}
```

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

**⚠️ Avatar creation is async.** The API returns success immediately, but the avatar is NOT ready for video generation yet. You MUST poll before proceeding:

```bash
# Poll until preview_image_url appears (avatar is ready)
curl -s "https://api.heygen.com/v3/avatars/looks?group_id=<group_id>" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Check every **10 seconds**. The avatar is ready when:
- `preview_image_url` is non-null in the look response
- `image_width` and `image_height` are non-zero

Typical wait: 30-90 seconds for photo avatars, 1-3 minutes for prompt avatars. Timeout after 5 minutes and tell the user to check the HeyGen dashboard.

**Do NOT proceed to video generation or voice selection until this check passes.** Videos submitted with an unready avatar will fail.

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

### Phase 3 — Voice Selection

Match a voice from HeyGen's library:

```
GET https://api.heygen.com/v3/voices
```

1. Read the Voice section from the AVATAR file
2. Filter by gender and language
3. Pick top 3 candidates based on personality match
4. Present to user with preview audio links
5. User picks one

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

Tell the user:
> "Avatar saved to AVATAR-<NAME>.md. Other skills like heygen-video-producer will pick it up automatically."

### Phase 5 — Test (Optional)

If the user wants to see their avatar in action:

```json
POST https://api.heygen.com/v3/video-agents
{
  "avatar_id": "<avatar_id>",
  "voice_id": "<voice_id>",
  "prompt": "Hi, I'm <name>. Nice to meet you!"
}
```

## Iteration Flow

When the user wants to refine:

- **"Adjust the prompt"** → Mode 2 with existing group_id (keeps the character, adds a new look). Only Mode 1 if they say "start completely over."
- **"Add a new look"** / **"different outfit"** / **"landscape version"** → Mode 2 with existing group_id. Add to Looks in AVATAR file.
- **"Try a different voice"** → back to Phase 3
- **"Start completely over"** → Mode 1, new character. Overwrite HeyGen section.

**Default to Mode 2 (new look under same group).** Only create a new group when the user explicitly wants a different character identity. This keeps the account clean and makes looks reusable across skills.

Each iteration updates the AVATAR file. The file is always the source of truth.

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
