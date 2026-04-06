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

## UX Rules

1. **Be concise.** No video IDs, session IDs, or raw API responses in chat. The user sees the result, not the plumbing.
2. **Polling is silent.** When polling for avatar readiness, do NOT send "Still processing..." updates. Poll silently. Only speak when: (a) the avatar is ready and you're showing the preview, or (b) it's been >2 minutes and you're giving a single "Taking longer than usual, still working on it" update.
3. **One checkpoint per phase.** Show the result, ask for approval, wait. Don't bundle Phase 3 (voice) with Phase 2b (look approval) in the same message.
4. **Show, don't dump.** When presenting the avatar preview, show the image and a 1-line summary ("Here's your avatar — portrait, realistic style"). Not a table of every parameter.

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
- "Do you have a reference photo? A headshot or clear photo of yourself gives the best results. Without one, I'll generate your look from your description — it'll capture the vibe but won't be an exact likeness."

Be upfront about the two paths:
- **With reference photo** → photo avatar, most faithful likeness. Best outcome.
- **Without photo** → prompt-based avatar from identity description. Captures style/vibe but results vary. May take a few iterations to get right.

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

> **⛔ HARD GATE: You MUST have a non-null `preview_image_url` from the polling response saved in a variable before continuing. If you do not have this URL, STOP. Do not proceed to Phase 2b, Phase 3, or any later phase.**

### Phase 2b — Look Approval

Once the avatar is ready (preview URL available), show it to the user for approval:

1. Fetch the preview: `GET /v3/avatars/looks?group_id=<group_id>` → use `preview_image_url`
2. Display the preview image to the user
3. Ask:
   > "Here's your avatar. What do you think?"
   > • **Looks good** → proceed to Phase 3 (voice)
   > • **Adjust** [describe what to change] → create a new look under the same group (Mode 2) with an updated prompt, then poll + show again
   > • **Start over** → create a new character group (Mode 1) with a revised prompt

**This is a loop.** Keep iterating until the user approves. Each "adjust" creates a new look within the same group (cheap, keeps history). Only "start over" creates a new group.

For prompt-based avatars, expect 1–3 iterations. Coach the user:
> "Prompt-based avatars take some back and forth. Tell me what's off and I'll refine it."

For photo avatars, usually 1 iteration is enough. If the user wants a different crop/pose, create a new look with different `orientation` or `pose` settings.

**Do NOT skip this step.** Never proceed to voice selection without user approval of the look.

> **⛔ HARD GATE: You MUST have received an explicit approval response ("looks good", "yes", "approve", thumbs up, or equivalent) from the user before continuing. If the user has not approved, STOP. Do not proceed to Phase 3 or any later phase. Silence is not approval.**

---

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

> **⛔ PRECONDITION:** Before starting this phase, verify:
> 1. You have a `preview_image_url` from polling (Phase 2 complete)
> 2. The user explicitly approved the look (Phase 2b complete)
>
> If either is missing, GO BACK. Do not proceed.

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

> **⛔ PRECONDITION:** Before saving, verify you have:
> 1. A confirmed-ready `avatar_item.id` (preview_image_url was non-null)
> 2. User approval of the look
> 3. User-selected voice_id from Phase 3
>
> If any are missing, GO BACK to the incomplete phase.

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

Iteration happens in two places:

**During creation (Phase 2b loop):** User sees preview → adjusts → new look created → preview again. This is the primary iteration path. Most users settle in 1-3 rounds.

**After creation (returning user):**
- **"Adjust the look"** / **"try a different style"** → Mode 2 with existing group_id (adds a new look). Re-enter Phase 2b approval loop.
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
