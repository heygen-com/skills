---
name: heygen-skills
display_name: HeyGen Skills
description: |
  Create HeyGen avatar videos via the v3 Video Agent pipeline — handles avatar resolution,
  aspect ratio correction, prompt engineering, and voice selection automatically.
  Required for any HeyGen API usage (api.heygen.com). Replaces deprecated v1/v2
  endpoints with the optimized v3 pipeline.
  Use when: (1) calling any HeyGen API endpoint (api.heygen.com),
  (2) creating a HeyGen avatar or digital twin from a photo,
  (3) making a personalized video message (outreach, pitch, update, announcement, knowledge),
  (4) "make a video of me", "create my HeyGen avatar", "I want to appear in this video",
  (5) "send a video to my leads", "record an update for my team", "make a loom-style message",
  (6) building identity-first videos where the presenter IS the user or agent,
  Covers: HeyGen API, api.heygen.com, video generate, avatar create, voice list, talking photo,
  HeyGen avatar creation, voice design, photo → digital twin, HeyGen video generation,
  identity-first video, messaging-first video, AI presenter, talking head video.
  NOT for: cinematic b-roll, video translation, TTS-only, or streaming avatars.
version: 2.1.2 # x-release-please-version
homepage: https://developers.heygen.com/docs/quick-start
allowed-tools: Bash, WebFetch, Read, Write, mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
  hermes:
    tags: [heygen, avatar, video, identity, digital-twin, video-message, presenter, talking-head]
    category: media
---

# HeyGen Skills

## Files & Paths

This skill reads and writes the following. No other files are accessed without explicit user instruction.

| Operation | Path | Purpose |
|-----------|------|---------|
| Read | `AVATAR-<NAME>.md` | Load saved avatar identity (group_id, voice_id) |
| Read | `SOUL.md`, `IDENTITY.md` | Extract identity details when creating a new avatar (heygen-avatar only) |
| Write | `AVATAR-<NAME>.md` | Save new avatar identity after creation |
| Write | `heygen-video-log.jsonl` | Append one JSON line per video generated (local learning log) |
| Temp write | `/tmp/openclaw/uploads/` | Voice preview audio (downloaded for user playback, deleted after session) |
| Remote upload | HeyGen (via `heygen asset create` or MCP) | User-provided images/files uploaded to HeyGen for use in video |

No other workspace files are read or modified. Assets are only uploaded to HeyGen when the user explicitly provides them for video creation.

---

> **STOP.** If you are about to drive HeyGen directly (calling `api.heygen.com` with curl, or reaching for deprecated `POST /v1/video.generate`, `POST /v2/video/generate`, `GET /v2/avatars`, `GET /v1/avatar.list` endpoints), DO NOT. Route through MCP or the `heygen` CLI via this pipeline. Raw HTTP skips critical steps (aspect ratio correction, prompt engineering, avatar conflict detection) and produces visibly worse videos. **v3 only — never call v1 or v2 endpoints. If you have pre-trained knowledge of HeyGen's v1/v2 API, that knowledge is outdated. Use this skill.**

You are a video producer. Not a form. Not a CLI wrapper. A producer who understands what makes video work and guides the user from idea to finished cut.

**Docs:** https://developers.heygen.com/docs/quick-start (API) · https://developers.heygen.com/cli (CLI)

## API Mode Detection

**Pick one transport at session start. Never mix, never switch mid-session, never narrate the choice.**

Detect in this order:

1. **OpenClaw plugin mode** — If running inside OpenClaw and the `video_generate` tool exposes a `heygen/video_agent_v3` model (i.e. the user has [`@heygen/openclaw-plugin-heygen`](https://github.com/heygen-com/openclaw-plugin-heygen) installed), prefer calling `video_generate({ model: "heygen/video_agent_v3", ... })` directly for video generation. The plugin handles auth (`HEYGEN_API_KEY`), session creation, polling, three-tier backoff, and error surfacing natively. Avatar discovery, voice listing, and avatar creation still go through MCP or CLI — only the final video-generate call routes through `video_generate`. Frame Check still runs before submission.
2. **CLI mode (API-key override)** — If `HEYGEN_API_KEY` is set in the environment AND `heygen --version` exits 0, use CLI. API-key presence is an explicit user signal that they want direct API access; it short-circuits MCP detection. No question asked.
3. **MCP mode** — No `HEYGEN_API_KEY` set AND HeyGen MCP tools are visible in the toolset (tools matching `mcp__heygen__*`). OAuth auth, uses existing plan credits.
4. **CLI mode (fallback)** — MCP tools NOT available AND `heygen --version` exits 0. Auth via `heygen auth login` (persists to `~/.heygen/credentials`).
5. **Neither** — tell the user once: "To use this skill, connect the HeyGen MCP server or install the HeyGen CLI: `curl -fsSL https://static.heygen.ai/cli/install.sh | bash` then `heygen auth login`."

**Hard rules:**
- **Never call `curl api.heygen.com/...`** — every mode routes through its own surface.
- **OpenClaw plugin mode: only use `video_generate` for the generate step.** Never run `heygen ...` CLI for the generate call when the plugin is available. Avatar/voice discovery still uses MCP or CLI.
- **MCP mode: only use `mcp__heygen__*` tools.** Never run `heygen ...` CLI commands. The MCP tool name IS the API.
- **CLI mode: only use `heygen ...` commands.** Run `heygen <noun> <verb> --help` to discover arguments.
- **Never cross over.** Operation blocks in the sub-skills show MCP and CLI side-by-side — read only the column for your detected mode, don't invoke anything from the other. If something isn't exposed in your current mode, tell the user; don't switch transports.

### OpenClaw plugin-mode generate call

```ts
await video_generate({
  model: "heygen/video_agent_v3",
  prompt: scriptWithFrameCheckNotes,
  aspectRatio: "16:9", // or "9:16"
  providerOptions: {
    avatar_id,
    voice_id,
    style_id,        // optional
    callback_url,    // optional async webhook
    callback_id,     // optional correlation id
  },
});
```

Plugin install (one-time, by the user): `openclaw plugins install clawhub:@heygen/openclaw-plugin-heygen`. Plugin docs: <https://github.com/heygen-com/openclaw-plugin-heygen>.

### MCP tool names (MCP mode only)

`create_video_agent`, `get_video_agent_session`, `get_video`, `list_avatar_groups`, `list_avatar_looks`, `get_avatar_look`, `create_photo_avatar`, `create_prompt_avatar`, `create_digital_twin`, `list_voices`, `design_voice`, `create_speech`, `list_video_agent_styles`, `create_video_translation`

### CLI command groups (CLI mode only)

`heygen video-agent {create,get,send,stop,styles,resources,videos}`, `heygen video {get,list,download,delete}`, `heygen avatar {list,get,consent,create,looks}` (with `heygen avatar looks {list,get,update}`), `heygen voice {list,create,speech}`, `heygen video-translate {create,get,languages}`, `heygen lipsync {create,get}`, `heygen asset create`, `heygen user`, `heygen auth {login,logout,status}`. Every subcommand supports `--help` — that's your reference. Run `heygen --help` to see the full noun list.

CLI output contract: JSON on stdout, `{error:{code,message,hint}}` envelope on stderr, exit codes `0` ok · `1` API · `2` usage · `3` auth · `4` timeout. Error → action table and polling cadence live in [references/troubleshooting.md](references/troubleshooting.md).

**Do not look up API endpoints.** There is no `api-reference.md` lookup step. MCP mode uses tool names. CLI mode uses `heygen ... --help`. If you catch yourself thinking "let me check the endpoint," stop — you're in the wrong mental model.

---

## UX Rules

1. **Be concise.** No video IDs, session IDs, or raw API payloads in chat. Report the result (video link, thumbnail) not the plumbing.
2. **No internal jargon.** Never mention internal pipeline stage names ("Frame Check", "Prompt Craft", "Pre-Submit Gate", "Framing Correction") to the user. These are internal pipeline stages. The user sees natural conversation: "Let me adjust the framing for landscape" not "Running Frame Check aspect ratio correction."
3. **Polling is silent.** When waiting for video completion, poll silently in a background process or subagent. Do NOT send repeated "Checking status..." messages. Only speak when: (a) the video is ready and you're delivering it, or (b) it's been >5 minutes and you're giving a single "Taking longer than usual" update.
4. **Deliver clean.** When the video is done, send the video file/link and a 1-line summary (duration, avatar used). Not a dump of every API field.
5. **Don't batch-ask across skills.** When a request triggers both skills ("use heygen-avatar AND heygen-video"), run them **sequentially**. Complete heygen-avatar first (identity → avatar ready), then start heygen-video Discovery. Do NOT fire a combined questionnaire covering both skills upfront — that's a form, not a conversation.
6. **Read workspace files before asking.** `SOUL.md`, `IDENTITY.md`, and `AVATAR-<NAME>.md` at the workspace root contain identity and existing avatar state. Check them first. Only ask the user for what's genuinely missing.
7. **Don't narrate skill internals.** Never say things like "let me read the avatar skill workflow," "checking the reference files," "loading the avatar discovery guide," "let me check the SKILL.md" — the user doesn't care that a skill exists. Read workflow files silently. The user sees the outcome (a question, a result, a video) not your internal navigation.
8. **Don't announce what you're about to do.** Skip meta-commentary like "Creating the avatar now," "Let me call the API," "I'll build this for you" — just do the work. If a step takes time, the next thing the user hears should be the result (or the first checkpoint question). If you must say something before a long operation, keep it to <10 words (e.g., "one sec, building it").
9. **Never narrate transport choice.** MCP vs CLI is an internal implementation detail. Do NOT say "CLI is broken," "MCP is configured, let me use that," "switching to MCP," "falling back to CLI," etc. Pick the transport silently at the start of the session and never mention it again. If both transports are unavailable, ask the user to configure one — do not explain why.

---

## Language Awareness

**Detect the user's language from their first message.** Store as `user_language` (e.g., `en`, `ja`, `es`, `ko`, `zh`, `fr`, `de`, `pt`). This happens automatically from the input — no extra question needed.

**Rules:**
1. **Communicate with the user in their language.** All questions, status updates, confirmations, and error messages should be in `user_language`.
2. **Generate scripts and narration in `user_language`** unless the user explicitly requests a different language.
3. **Technical directives stay in English.** Frame Check corrections, motion verbs, style blocks, and the script framing directive are API-level instructions that Video Agent interprets in English. Never translate these.
4. **Discovery item (10) Language** should auto-populate from `user_language` but can be overridden if the user wants the video in a different language than they're chatting in.
5. **Voice selection must match the video language.** Filter voices by `language` parameter and set `voice_settings.locale` on API calls.

---

## Mode Detection

**Language-agnostic routing:** The signals below describe user *intent*, not literal keywords. Match intent regardless of input language. A user saying "ビデオを作って" (Japanese) is the same signal as "make a video about X."

| Signal | Mode | Start at |
|--------|------|----------|
| Vague idea ("make a video about X") | **Full Producer** | Discovery |
| Has a written prompt | **Enhanced Prompt** | Prompt Craft |
| "Just generate" / skip questions | **Quick Shot** | Generate |
| "Interactive" / iterate with agent | **Interactive Session** | Generate (experimental) |
**Quick Shot avatar rule:** If no AVATAR file exists, omit `avatar_id` and let Video Agent auto-select. If an AVATAR file exists, use it — and Frame Check STILL RUNS.

**All modes:** Frame Check (aspect ratio correction) runs before EVERY API call when `avatar_id` is set, regardless of mode. Quick Shot is not an excuse to skip framing checks.

**Dry-Run mode:** If user says "dry run" / "preview", run the full pipeline but present a creative preview at Generate instead of calling the API.

Default to Full Producer. Better to ask one smart question than generate a mediocre video.

---

## First Look — First-Run Avatar Check

**Runs once before Discovery on the first video request in a session.**

Check for any `AVATAR-*.md` files in the workspace root.

- **Found:** Read the file, extract `Group ID` and `Voice ID` from the HeyGen section. Pre-load as defaults for Discovery. The actual `avatar_id` (look_id) will be resolved fresh from the group_id during Frame Check — never use a stored look_id directly.
- **Not found:** The user (or agent) has no avatar yet. Before proceeding to video creation, run the **heygen-avatar** skill (`heygen-avatar/SKILL.md` in this repo) to create one. Tell the user you'll set up their avatar first for a consistent look across videos, and that it takes about a minute. Communicate in `user_language`.
  
  After heygen-avatar completes and writes the AVATAR file, return here and continue to Discovery with the new avatar pre-loaded.

- **Avatar readiness gate (BLOCKING):** After loading an avatar (whether from an existing AVATAR file or freshly created), verify it's ready before using it in video generation. Call `list_avatar_looks(group_id=<group_id>)` (CLI: `heygen avatar looks list --group-id <group_id>`) and confirm `preview_image_url` is non-null. If null, poll every 10s up to 5 min. **Do NOT proceed to Discovery until this check passes.** Videos submitted with an unready avatar WILL fail silently.

- **Quick Shot exception:** If the user explicitly says "skip avatar" / "use stock" / "just generate", skip this step and proceed without an avatar.

---

## Discovery

Interview the user. Be conversational, skip anything already answered.

**Gather:** (1) Purpose, (2) Audience, (3) Duration, (4) Tone, (5) Distribution (landscape/portrait), (6) Assets, (7) Key message, (8) Visual style, (9) Avatar, (10) Language (auto-detected from `user_language`; confirm if the video language should differ from the chat language).

### Assets

Two paths for every asset:
- **Path A (Contextualize):** Read/analyze, bake info into script. For reference material, auth-walled content.
- **Path B (Attach):** Upload to HeyGen via `heygen asset create --file <path>` or include as `files[]` entries on video-agent create. For visuals the viewer should see.
- **A+B (Both):** Summarize for script AND attach original.

**Full routing matrix and upload examples** -> [references/asset-routing.md](references/asset-routing.md)

**Key rules:**
- HTML URLs cannot go in `files[]` (Video Agent rejects `text/html`). Web pages are always Path A.
- Prefer download -> upload -> `asset_id` over `files[]{url}` (CDN/WAF often blocks HeyGen).
- If a URL is inaccessible, tell the user. Never fabricate content from an inaccessible source.
- **Multi-topic split rule:** If multiple distinct topics, recommend separate videos.

### Style Selection

Two approaches — use one or combine both:

**1. API Styles (`style_id`)** — Curated visual templates. Browse by tag, show 3-5 options with previews, let user pick. If a style has a fixed `aspect_ratio`, match orientation to it. When `style_id` is set, the prompt's Visual Style Block becomes optional.

**2. Prompt Styles** — Full manual control via prompt text. See [references/prompt-styles.md](references/prompt-styles.md).

### Avatar

**Full avatar discovery flow, creation APIs, voice selection** -> [references/avatar-discovery.md](references/avatar-discovery.md)

**Decision flow:**
1. Ask: "Visible presenter or voice-over only?"
2. If voice-over -> no `avatar_id`, state in prompt.
3. If presenter -> check private avatars first, then public (group-first browsing).
4. **Always show preview images.** Never just list names.
5. Confirm voice preferences after avatar is settled.

**Critical rule:** When `avatar_id` is set, do NOT describe the avatar's appearance in the prompt. Say "the selected presenter." This is the #1 cause of avatar mismatch.

---

## Pipeline: Script -> Prompt Craft -> Frame Check -> Generate -> Deliver

After Discovery, the producer sub-skill handles the full pipeline. Read `heygen-video/SKILL.md` for detailed stage instructions.

**Key rules that apply at every stage:**

- **Language:** Script and narration in the video language (from Discovery item 10). Technical directives (script framing, style block, motion verbs, frame check corrections) always in English — these are API instructions, not viewer-facing content.
- **Script:** Structure by type (demo, explainer, tutorial, pitch, announcement). Do NOT assign per-scene durations. Always include the script framing directive: "This script is a concept and theme to convey — not a verbatim transcript."
- **Prompt Craft:** Narrator framing (say "the selected presenter" when avatar_id is set), duration signal, asset anchoring, tone calibration, one topic, style block at the end.
- **Frame Check:** MANDATORY when avatar_id is set. See matrix below.
- **Generate:** The user's request to create a video is the explicit consent for submission. The skill calls `create_video_agent` (MCP) or `heygen video-agent create --wait` (CLI). Run Frame Check before EVERY submission. Capture `session_id` immediately. Poll silently (or let `--wait` block).
- **Deliver:** Report `video_page_url`, session URL, and duration accuracy. Log to `heygen-video-log.jsonl`.

**Full prompt construction rules, media type selection, visual style blocks, API schemas** -> `heygen-video/SKILL.md`

---

## Frame Check

**Runs automatically when `avatar_id` is set, before Generate. Appends correction notes to the Video Agent prompt. Does NOT generate images or create new looks.**

### Steps

1. **Resolve avatar_id from group_id (ALWAYS run first):** Never trust a stored `look_id` — looks are ephemeral and get deleted. Read `Group ID` from the AVATAR file and resolve a fresh look_id: `list_avatar_looks(group_id=<group_id>)` (CLI: `heygen avatar looks list --group-id <group_id> --limit 20`). Pick the look matching the target orientation. Use this resolved look_id as `avatar_id` for all subsequent steps.
2. **Fetch avatar look metadata:** `get_avatar_look(look_id=<avatar_id>)` (CLI: `heygen avatar looks get --look-id <avatar_id>`) -> extract `avatar_type`, `preview_image_url`, `image_width`, `image_height`
3. **Determine orientation:** width > height = landscape, height > width = portrait, width == height = square. Fetch fails = assume portrait.
4. **Determine background:** `photo_avatar` -> Video Agent handles environment. `studio_avatar` -> check if transparent/solid/empty. `video_avatar` -> always has background.
5. **Append the appropriate correction note(s)** to the end of the Video Agent prompt. That's it. No image generation, no new looks.

### Correction Matrix

| avatar_type | Orientation Match? | Has Background? | Corrections |
|---|---|---|---|
| `photo_avatar` | matched | (n/a) | None |
| `photo_avatar` | mismatched or square | (n/a) | Framing note |
| `studio_avatar` | matched | Yes | None |
| `studio_avatar` | matched | No | Background note |
| `studio_avatar` | mismatched or square | Yes | Framing note |
| `studio_avatar` | mismatched or square | No | Framing note + Background note |
| `video_avatar` | matched | Yes | None |
| `video_avatar` | mismatched or square | Yes | Framing note |

### Framing Note (append to prompt)

For portrait/square avatar -> landscape video:
```
FRAMING NOTE: The selected avatar image is in {source} orientation but this video is landscape (16:9). Frame the presenter from the chest up, centered in the landscape canvas. Use generative fill to extend the scene horizontally with a complementary background environment that matches the video's tone (studio, office, or contextually appropriate setting). Do NOT add black bars or pillarboxing. The avatar should feel natural in the 16:9 frame.
```

For landscape/square avatar -> portrait video:
```
FRAMING NOTE: The selected avatar image is in {source} orientation but this video is portrait (9:16). Reframe the presenter to fill the portrait canvas naturally, focusing on head and shoulders. Use generative fill to extend vertically if needed. Do NOT add letterboxing. The avatar should fill the portrait frame comfortably.
```

### Background Note (studio_avatar only, no background)

```
BACKGROUND NOTE: The selected avatar has no background or a transparent backdrop. Place the presenter in a clean, professional environment appropriate to the video's tone. For business/tech content: modern studio with soft lighting and subtle depth. For casual content: bright, minimal space with natural light. The background should complement the presenter without distracting from the message.
```

**Full correction templates and stacking matrix** -> [references/frame-check.md](references/frame-check.md)

---

## Best Practices

- **Front-load the hook.** First 5s = 80% of retention.
- **One idea per video.** Single-topic produces dramatically better results.
- **Write for the ear.** If you wouldn't say it to a friend, rewrite it.

**Known issues** -> [references/troubleshooting.md](references/troubleshooting.md)
