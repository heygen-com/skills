---
name: heygen-avatar
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
  "design a presenter AND immediately record"), run heygen-avatar first, then heygen-video.
  Returns avatar_id + voice_id — pass directly to heygen-video to create HeyGen videos.
  NOT for: generating videos (use heygen-video), translating videos, or TTS-only tasks.
argument-hint: "[photo_url_or_description]"
allowed-tools: Bash, WebFetch, Read, Write, mcp__heygen__*
---

# HeyGen Avatar Designer

Create and manage HeyGen avatars for anyone: the agent, the user, or named characters. Handles identity extraction, avatar generation, voice selection, and saves everything to `AVATAR-<NAME>.md` for consistent reuse.

## Start Here (Critical)

**Do NOT batch-ask questions.** Do not fire "give me a photo, voice preference, duration, target platform, tone, key message" all at once. Walk phases in order. Each phase asks at most one or two things at a time.

**When creating for the agent itself** ("create your avatar", "bring yourself to life"), do NOT ask the user for a photo or appearance details first. Read `SOUL.md` and `IDENTITY.md` from the workspace root. The agent's identity lives there. Only ask the user for traits that are genuinely missing from those files.

**Photo is a nudge, not a gate.** Prompt-based avatars work. Offer photo as an optional upgrade for face consistency across videos, not as a required input.

## Before You Start (Claude Code only)

Try to read `SOUL.md` from the workspace root.

- **Found** → OpenClaw environment. Skip this section entirely and go straight to Phase 0.
- **Not found** → Claude Code environment. Say this before anything else:

First, fetch the user's existing HeyGen avatars.

**MCP:** `list_avatar_groups(ownership=private)` — returns the user's private avatar groups.
**CLI:** `heygen avatar list --ownership private`

Parse the `data` array.

**⚠️ AVATAR file caveat:** Ignore any AVATAR-*.md files found in the workspace that belong to a *different* person or agent (e.g., AVATAR-Eve.md when creating an avatar for Claude). Only use an AVATAR file if its name matches the subject you're creating for right now.

If the user **has existing avatars** (non-empty `data` array), present them as numbered options and ask which to use or whether to create a new one. Communicate in `user_language`.

If the user has **no existing avatars** (empty `data`), tell them none were found and offer to create one with a few quick questions. Mention the OpenClaw `SOUL.md` shortcut for future reference. Communicate in `user_language`.

Wait for their answer before proceeding.

## API Mode Detection

**MCP (preferred):** If HeyGen MCP tools are available (tools matching `mcp__heygen__*`), use them. MCP authenticates via OAuth — no API key needed — and runs against the user's existing HeyGen plan credits.

**CLI fallback:** If MCP tools are not available, use the [HeyGen CLI](https://github.com/heygen-com/heygen-cli) (`heygen` binary). Auth: set `HEYGEN_API_KEY` in the env OR run `heygen auth login` (persists to `~/.heygen/credentials`). Verify with `heygen auth status`. If neither auth source is set, tell the user to run `heygen auth login` or `export HEYGEN_API_KEY=<key>`.

**API:** v3 only. Never call v1 or v2 endpoints.

**Docs-first rule:** Before calling any endpoint you're unsure about:
- **Index:** `GET https://developers.heygen.com/llms.txt` — full sitemap
- **Any page:** Append `.md` to the URL for clean markdown
- Or run `heygen <noun> <verb> --help`
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

⚠️ look_ids are ephemeral — always resolve fresh from group_id at runtime via `heygen avatar looks list --group-id <id>` (or MCP `list_avatar_looks`). Never hardcode look_id as the primary avatar reference.
```

**Top sections** (Appearance, Voice) are portable natural language. Any platform can use them.
**HeyGen section** is runtime config with API IDs. Skills read this to make API calls.

## Skill Announcement

Start every invocation with:

> 🎭 **Using: heygen-avatar** — creating an avatar for [name]

## Workflow

**DO NOT batch-ask questions upfront.** Walk phases in order. Each phase asks at most one thing at a time, and only if needed.

### Phase 0 — Who Are We Creating?

Determine the target identity from the request. Do NOT ask the user "whose avatar?" if it's clear from phrasing:

1. **Agent** — "create your avatar", "bring yourself to life", "design an avatar for you" → this is for the agent (Adam, Eve, Claude, etc.). Read `IDENTITY.md` for name.
2. **User** — "create my avatar", "make me an avatar", "I want my face in a video" → for the user. Ask for their name if not obvious.
3. **Named character** — "create an avatar called Cleo", "design a character named X" → use the given name.

Then check `AVATAR-<NAME>.md` at the workspace root:

- **AVATAR file exists + HeyGen section filled in** → "You already have an avatar set up. Want to add a new look, update it, or start fresh?" Wait for answer.
- **AVATAR file exists but HeyGen section empty** → skip to Phase 2.
- **No AVATAR file** → proceed to Phase 1.

### Phase 1 — Identity Extraction

**Order matters. Files first, questions second.**

**For the agent** (Phase 0 target = agent):
1. Read `SOUL.md`, `IDENTITY.md`, and any existing `AVATAR-<NAME>.md` from the workspace root.
2. If SOUL.md or IDENTITY.md is found → extract appearance and voice traits silently. Do NOT ask the user "describe your appearance" — the agent IS the subject, and its identity lives in those files. **If the files describe only personality / values with no physical description, do NOT hallucinate traits.** Ask the user conversationally for the missing appearance traits only.
3. If neither file is found (e.g., Claude Code environment with no workspace identity) → ask the user to describe the agent's appearance and voice conversationally.

**For users/named characters** (Phase 0 target = user or named):
- Conversational onboarding. Ask naturally about appearance (age, hair, general vibe) and voice (calm/energetic, accent). Not as a form — one or two questions at a time. Communicate in `user_language`.

Write `AVATAR-<NAME>.md` with the Appearance and Voice sections filled in. Leave the HeyGen section empty until Phase 2 succeeds.

Then proceed to Phase 2 via the Reference Photo Nudge.

### Reference Photo Nudge (Phase 2 entry)

Ask if they have a reference photo. A photo produces better face consistency across videos, but prompt-based avatars work well when no photo is available. **This is a nudge, not a gate — offer to skip.**

Check first:
- **For agents:** look at the AVATAR file's Appearance → Reference field, or IDENTITY.md for a photo path. If found, skip asking and use it.
- **For users:** ask. Keep it one sentence: "Got a headshot? It gives better face consistency, but I can also generate from your description — just say 'skip.'"

Branch:
- **Photo provided** → upload via MCP `upload_asset` or `heygen asset create --file <path>`, then Type B (photo) creation in Phase 2.
- **Skip** → Type A (prompt) creation in Phase 2.


### Phase 2 — Avatar Creation

Two modes:

**Mode 1 — New character** (omit `avatar_group_id`):
Creates a brand new character with its own group.

**Mode 2 — New look** (include `avatar_group_id`):
Adds a variation to an existing character. Read the Group ID from the AVATAR file.

Two creation types:

**Type A — From prompt (AI-generated appearance):**

**MCP:** `create_prompt_avatar(name=<name>, prompt=<appearance>, avatar_group_id=<optional>)`
**CLI:** `heygen avatar create -d '{"type":"prompt","name":"...","prompt":"...","avatar_group_id":"..."}'` (accepts inline JSON, a file path, or `-` for stdin)

Prompt limit is 1000 characters. Be descriptive — include style, features, expression, lighting. The API spec says 200 but the actual enforced limit is 1000.

**Type B — From reference image:**

**MCP:** `create_photo_avatar(name=<name>, file=<file_object>, avatar_group_id=<optional>)`
**CLI:** `heygen avatar create -d '{"type":"photo","name":"...","file":{"type":"url","url":"..."},"avatar_group_id":"..."}'`

File options for Type B:
- `{ "type": "url", "url": "https://..." }` — public image URL
- `{ "type": "asset_id", "asset_id": "<id>" }` — from `heygen asset create --file <path>`
- `{ "type": "base64", "media_type": "image/png", "data": "<base64>" }` — inline

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

**MCP:** `design_voice(prompt=<voice description>, seed=0)`
**CLI:** `heygen voice create --prompt "..." --seed 0` (also accepts `--gender`, `--locale`)

Returns 3 voice options per seed. Present all 3 with inline audio previews:
- Download each `preview_audio_url` to a temp path (any standard download method works — no HeyGen auth needed, these are public S3 URLs)
- Send as audio attachment: `message(action:send, media:"<path>", caption:"Option <n>: <voice_name> — <gender>, <language>")` so it plays inline in Telegram/Discord
- After all previews sent, present selection buttons

⛔ **STOP. Wait for the user to pick a voice via buttons or text. Do NOT select a voice yourself or proceed to Phase 4 until the user explicitly chooses.**

If none match:
> "None of these hitting right? I can try a different set (same description, different variations) or you can tweak the description."

Increment `seed` and call again. Different seeds give completely different voice options from the same prompt.

- Clean up /tmp files after user picks

#### Path B — Voice Browse (fallback)

Browse HeyGen's existing voice library:

**MCP:** `list_voices(type=private)` then `list_voices(type=public, language=<lang>, gender=<gender>)`
**CLI:** `heygen voice list --type private` / `heygen voice list --type public --language <lang> --gender <gender>`

1. Read the Voice section from the AVATAR file
2. Filter by gender and language
3. Pick top 3 candidates based on personality match
4. Present with inline audio previews (same download + send pattern as Path A)
5. ⛔ **STOP. Wait for the user to pick. Do NOT auto-select.**

### Phase 4 — Save to AVATAR File

Update the HeyGen section of `AVATAR-<NAME>.md` to match the canonical format:

```markdown
## HeyGen
- Group ID: <avatar_item.group_id — THE stable reference, never changes>
- Voice ID: <chosen voice_id>
- Voice Name: <voice name>
- Voice Designed: <true if custom-designed, false if picked from catalog>
- Voice Seed: <seed value used, if designed>
- Looks: <orientation>=<avatar_item.id> (e.g., landscape=<look_id>, portrait=<look_id>)
- Last Synced: <ISO timestamp>

⚠️ look_ids are ephemeral — always resolve fresh from group_id at runtime via `heygen avatar looks list --group-id <id>` (or MCP `list_avatar_looks`). Never hardcode look_id as the primary avatar reference.
```

Confirm the avatar is saved and that other skills (like heygen-video) will pick it up automatically. Communicate in `user_language`.

### Phase 5 — Test (Optional)

If the user wants to see their avatar in action:

**MCP:** `create_video_agent(avatar_id=<avatar_id>, voice_id=<voice_id>, prompt=<greeting>)`
**CLI:** `heygen video-agent create --avatar-id <id> --voice-id <id> --prompt "..." --wait`

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

**Be interactive at checkpoints, silent everywhere else.** Stop and wait at avatar approval and voice selection. Between checkpoints, work silently — don't narrate reasoning or explain next steps. After voice pick: save + confirm in one message.

## Video Producer Integration

`heygen-video` reads AVATAR files for group_id and voice_id. "Make a video with Eve" → reads `AVATAR-EVE.md` → gets Group ID + Voice ID → resolves fresh look_id at runtime. No AVATAR file → falls back to stock avatars or asks user.

## Error Handling

- Missing SOUL.md/IDENTITY.md → conversational onboarding, write AVATAR file from answers
- API fails → retry once, then ask user to check API key
- Voice match poor → show all available voices, let user browse
- Asset upload fails → skip reference image, try prompt-only creation
- Existing avatar file with stale HeyGen IDs → offer to regenerate or keep
