# Dry Run — Full Pipeline Preview

Iterate on the complete video production pipeline WITHOUT burning HeyGen credits. Produces the exact API payload (prompt, avatar_id, asset_ids, orientation) that would be sent to `POST /v3/video-agents`.

## Purpose

This is the fast iteration loop. Run it dozens of times to nail the user interaction flow, avatar selection, prompt construction, and payload assembly. When satisfied, flip to a real run.

## What Gets Tested

1. **Avatar Decision Flow** — Did the skill guide the user through avatar selection correctly?
2. **Discovery Phase** — Did it ask the right questions? Skip the right ones?
3. **Script Quality** — Word count, pacing, structure
4. **Prompt Construction** — Scene-by-scene structure, visual style block, media types
5. **Final API Payload** — Exact JSON that would hit the API

## How to Run

Eve spawns Adam (or runs it herself) with a dry-run scenario. The skill follows the full pipeline but STOPS before calling the API. Instead, it outputs the final payload.

### Dry-Run Prompt Template

```
You are testing the heygen-video-producer skill in DRY RUN mode.

## Setup
Read the skill at: skills/heygen-video-producer/SKILL.md
You have HEYGEN_API_KEY set.

## DRY RUN RULES
- Follow the ENTIRE skill pipeline (Discovery → Script → Prompt → Generate)
- DO NOT call the HeyGen API. No POST to /v3/video-agents.
- Instead, output the FINAL PAYLOAD section below.
- For the avatar flow, call the LIST APIs (GET /v3/avatars, GET /v3/avatars/looks) to see real data.
- For asset uploads, note what WOULD be uploaded but don't actually upload.

## Simulated User
You are playing both roles: the skill agent AND the user. For user responses, use the scenario below.

## Scenario
{SCENARIO}

## Avatar Interaction
When the skill asks about avatar preference, respond as the user would based on the scenario's avatar_intent field.

## Required Output

After completing the full pipeline, output this EXACT format:

---
## DRY RUN RESULT

### Interaction Trace
[Numbered list of every agent↔user exchange that happened. Show both sides.]

1. Agent: "What's this video for?"
   User: "Product demo for developers"
2. Agent: "Do you have a preferred avatar?"
   User: "Use my existing one"
3. ...

### Avatar Decision
- User intent: [use existing / new look / new avatar / no preference / voice-only]
- Decision path taken: [which branch of the avatar flow]
- Avatar selected: [name, id, type (static/motion), group_id]
- Avatar look: [if applicable, which look within group]
- Voice selected: [voice_id, name if known]
- How avatar was determined: [auto-selected / user chose from list / user specified by name / default]

### Script
[Full script with word count, scene count, estimated duration]

### Prompt (as constructed)
[The exact prompt string that would go in the API payload]

### Final API Payload
```json
{
  "prompt": "<the full prompt>",
  "files": [
    {"asset_id": "<id>", "note": "<what this asset is>"}
  ]
}
```

If no assets: `"files": []`

### Payload Checklist
- [ ] Prompt uses narrator framing ("A narrator explains..." not "Create a video...")
- [ ] Duration is padded 1.4x from user target
- [ ] Visual style block present at bottom
- [ ] Media types specified per scene
- [ ] Avatar direction included in prompt (if using avatar)
- [ ] Asset anchoring is specific (if assets exist)
- [ ] Word count within 150 wpm budget
- [ ] Scene-by-scene structure (not flat paragraph)

### Friction Points
[Anything that was confusing, contradictory, or missing in the skill during this dry run]

### Score
- Avatar flow: [1-10] — was avatar selection smooth and correct?
- Discovery: [1-10] — right questions, right skips?
- Script: [1-10] — quality, pacing, structure?
- Prompt: [1-10] — would this produce a good video?
- Payload: [1-10] — correct format, all fields present?
- Overall: [1-10]
---
```

---

## Scenarios

Each scenario simulates a different user with different avatar needs. The `avatar_intent` field tells the simulated user how to respond when asked about avatars.

### Scenario 1: Has Existing Avatar, Wants to Use It
```yaml
name: returning-user-existing-avatar
user_context: "I'm a developer who's made videos before. I have a custom avatar."
request: "Make me a 60-second video about our new REST API for developers."
avatar_intent: "Use my existing avatar. I already have one set up."
assets: none
tone: casual-confident
duration: 60s
```

### Scenario 2: Has Avatar Group, Wants Different Look
```yaml
name: same-avatar-different-look
user_context: "I've got an avatar but I want a different vibe for this video."
request: "Create a 45-second sales pitch for enterprise clients. Professional tone."
avatar_intent: "I have my avatar but can we make it look more corporate? Different outfit or setting."
assets: none
tone: professional
duration: 45s
```

### Scenario 3: No Avatar, Needs New One
```yaml
name: first-time-new-avatar
user_context: "First time using HeyGen. No avatar yet."
request: "I need a product demo video, about 90 seconds."
avatar_intent: "I don't have an avatar. What are my options?"
assets: [screenshot.png (simulated)]
tone: energetic
duration: 90s
```

### Scenario 4: Wants Voice-Only (No Avatar)
```yaml
name: voice-only
user_context: "I want a clean explainer with just visuals and voiceover."
request: "60-second explainer about MCP for a technical blog post."
avatar_intent: "No avatar. Just voice-over with B-roll."
assets: none
tone: calm-authoritative
duration: 60s
```

### Scenario 5: Has Avatar, Wants Completely New One
```yaml
name: wants-new-avatar-entirely
user_context: "I have an old avatar from last year. It doesn't match our rebrand."
request: "30-second announcement about our company rebrand."
avatar_intent: "I need a completely new avatar. The old one doesn't fit our new brand."
assets: [new-brand-guidelines.pdf (simulated)]
tone: energetic
duration: 30s
```

### Scenario 6: No Preference (Let the Skill Decide)
```yaml
name: no-avatar-preference
user_context: "Just want a video. Don't care about avatar specifics."
request: "Make a quick video about AI agents for my LinkedIn."
avatar_intent: "Whatever works. You pick."
assets: none
tone: casual
duration: 30s
```

### Scenario 7: Quick Shot (Skip Everything)
```yaml
name: quick-shot-skip-all
user_context: "Just generate it, don't ask me anything."
request: "Just make this: A narrator explains why every developer needs an AI video API. 30 seconds."
avatar_intent: [not applicable — quick shot mode should not ask]
assets: none
tone: implied from prompt
duration: 30s
```

### Scenario 8: Has Specific Stock Avatar in Mind
```yaml
name: wants-specific-stock-avatar
user_context: "I saw a HeyGen avatar I liked. Her name was Abigail."
request: "Create a 60-second tutorial walkthrough."
avatar_intent: "Can I use Abigail? The one with the office background."
assets: none
tone: professional
duration: 60s
```

---

## Avatar Decision Flow (What the Skill SHOULD Do)

This is the avatar guidance tree the skill should follow. Use it to evaluate whether the dry run got it right.

```
User request arrives
  │
  ├─ Quick Shot mode? → Skip avatar question. Let Video Agent auto-select.
  │
  ├─ User said "no avatar" / "voice only"? → Include in prompt: "No visible avatar, voice-over only."
  │
  └─ All other modes → Ask about avatar preference:
      │
      │   "Do you have a preferred avatar, or should I pick one for you?"
      │   Options:
      │   a) Use my existing avatar
      │   b) I want a different look (same person, different outfit/setting)
      │   c) Create a new avatar from scratch
      │   d) Use a stock HeyGen avatar
      │   e) No preference, you decide
      │
      ├─ (a) Use existing →
      │     1. GET /v3/avatars → show user their groups
      │     2. User picks group → GET /v3/avatars/looks?group_id={id} → show looks
      │     3. User picks look → save avatar_id (look_id), voice_id
      │     4. Pass avatar_id as top-level parameter to POST /v3/video-agents
      │
      ├─ (b) Different look →
      │     1. GET /v3/avatars → show groups
      │     2. User picks group → GET /v3/avatars/looks?group_id={id} → show current looks
      │     3. If desired look exists → pass avatar_id (look_id) to generation
      │     4. If user wants a new look → create via POST /v3/avatars (type: photo_avatar)
      │        then add look. This takes a few minutes to process.
      │     5. For this video, can also describe desired appearance in prompt alongside avatar_id
      │
      ├─ (c) New avatar from scratch →
      │     1. Ask: "Do you have a photo to use, or should I describe what you want?"
      │     2. Photo provided → upload to HeyGen → create avatar group → train → add motion
      │        (Full flow from photo-avatar-api-flow.md, takes 5-10 min)
      │     3. No photo → describe in prompt, let Video Agent pick a stock avatar that matches
      │     4. Note: creating a new avatar is a separate workflow. Offer to do it now
      │        (delays video) or proceed with a stock avatar and create the custom one after.
      │
      ├─ (d) Stock avatar →
      │     1. GET /v3/avatars?ownership=public → show curated list (filter by gender/style if user specified)
      │     2. User picks group → GET /v3/avatars/looks?group_id={id} → show looks
      │     3. User picks look → pass avatar_id (look_id) to POST /v3/video-agents
      │
      └─ (e) No preference →
            Don't ask more questions. Include generic prompt direction:
            "Use a professional presenter appropriate for [audience]."
            Let Video Agent auto-select.
```

### Key Technical Constraint
**Video Agent API (`POST /v3/video-agents`) accepts `avatar_id` as a top-level parameter alongside the prompt.** When a custom or stock avatar is selected, pass `avatar_id` directly. This achieves ~97% duration accuracy vs ~80% with prompt-only descriptions.

Avatar discovery uses:
- `GET /v3/avatars` → list avatar groups (custom + stock)
- `GET /v3/avatars/looks` → list individual looks within a group
- Each look has a `look_id` which is passed as `avatar_id` in the generation call

This means:
- "Use my existing avatar" → discover via API, pass avatar_id directly
- Stock avatars → browse groups, pick look, pass avatar_id
- Custom avatars → discover group, pick look, pass avatar_id
- Voice-only → include "no visible avatar, voice-over only" in prompt

---

## Saving Results

Save each dry run to:
```
evals/runs/dry-YYYY-MM-DD-{scenario_name}.md
```

Include the full DRY RUN RESULT output. Compare across runs to track improvement.

---

## Fast Iteration Loop

The whole point: run a scenario → read the output → tweak SKILL.md → run again.

1. Pick a scenario (start with #6 "no preference" — simplest path)
2. Run dry run
3. Read the interaction trace — is the flow natural?
4. Read the avatar decision — did it guide correctly?
5. Read the payload — would this produce a good video?
6. Identify friction → edit SKILL.md → run again
7. Repeat until all 8 scenarios score 8+/10

Typical iteration: 5-10 runs per SKILL.md change. Each run takes ~2-3 minutes (no API cost).
