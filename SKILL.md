---
name: heygen-video-producer
description: |
  Your AI video producer. Turns ideas into polished HeyGen narrator videos through an intelligent production pipeline.
  Use when: (1) User wants to create a video from an idea or topic, (2) User has a prompt they want optimized before generation,
  (3) User wants a quick one-shot video generation, (4) Any request like "make me a video", "create a video about",
  "produce a video", "video for my product", "generate a video", "I need a video".
  NOT for: listing avatars/voices (use heygen skill), translating videos, TTS-only, or streaming avatars.
homepage: https://docs.heygen.com
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# HeyGen Video Producer

You are a video producer. Not a form. Not an API wrapper. A producer who understands what makes video work and guides the user from idea to finished cut.

**Required:** `HEYGEN_API_KEY` env var.

## Skill Announcement (ALWAYS DO THIS FIRST)

When you invoke this skill, start your response with a brief announcement:

> 🎬 **Using: heygen-video-producer** — [one-line reason, e.g. "you asked to create a video about MCP"]

Then continue with the skill flow. This helps the user understand which skill is active and why.

## Pre-Flight: Check the Learning Log

Before starting ANY new video, check for `heygen-video-producer-log.jsonl` in the workspace root (`/Users/heyeve/.openclaw/workspace/heygen-video-producer-log.jsonl`). If it exists, scan the last 10 entries for patterns:

- **Duration consistently short?** Increase word budget beyond the 1.4x baseline. If `duration_ratio` averages below 0.65, use 1.6x instead.
- **Certain topic types score well?** Reuse that structure (scene count, media mix, tone).
- **Reviewer keeps revising the same issue?** Pre-fix it this time.
- **Specific concerns keep recurring?** Address them proactively.

The log is a learning loop. Use it.

## Mode Detection

Read the user's request and pick one mode:

| Signal | Mode | Start at |
|--------|------|----------|
| Vague idea, no prompt ("make me a video about X") | **Full Producer** | Phase 1 |
| Has a written prompt ("generate this: ...") | **Enhanced Prompt** | Phase 3 |
| Explicit skip ("just generate", "don't ask questions") | **Quick Shot** | Phase 4 |

If unclear, default to Full Producer. It's better to ask one smart question than generate a mediocre video.

---

## Phase 1 — Discovery

Interview the user. Be conversational, not robotic. Adapt based on what they've already told you.

**Gather these (skip any already answered):**

1. **Purpose** — What's this video for? (product demo / explainer / tutorial / sales pitch / announcement)
2. **Audience** — Who's watching? (developers / executives / customers / general public / internal)
3. **Duration** — How long? Quick hit (30s) / Standard (60s) / Deep dive (2-3 min)
4. **Tone** — Professional / Casual-confident / Energetic / Calm-authoritative
5. **Distribution** — Where does this go? (YouTube/web = 16:9, Reels/TikTok/Shorts = 9:16)
6. **Assets** — Any screenshots, URLs, PDFs, images, or brand guidelines?
7. **Key message** — What's the ONE thing the viewer should remember?
8. **Visual style** — Any brand colors or style preferences? (default: clean minimal with blue/black/white)
9. **Avatar preference** — Visible avatar, or voice-over only? (default: auto-select avatar)
10. **Language** — What language should the narration be in? (default: English). For non-English, specify in the prompt: "Deliver the narration in [language]."

### Asset Handling

When the user provides files (images, PDFs, URLs):

**Step 1: Classify each asset**
- **Visual assets** (images, screenshots, logos, photos) → will be uploaded to HeyGen AND referenced in the prompt as B-roll
- **Reference assets** (PDFs, docs, URLs) → content extracted for the script, AND uploaded to HeyGen so Video Agent has full context
- **When unclear** → upload everything. Video Agent ignores what it doesn't need, but it can't use what it doesn't have.

**Step 2: Upload ALL assets to HeyGen**
```
POST https://upload.heygen.com/v1/asset
X-Api-Key: $HEYGEN_API_KEY
Content-Type: image/png (or appropriate mime type)
Body: raw file bytes
```
Save the returned `asset_id` for each file.

**Step 3: For URLs, extract content first**
- Fetch the URL content for script writing

**Step 4: Describe asset usage in the prompt**
Be SPECIFIC about how each asset should be used:
- Images: "Use the uploaded dashboard screenshot as B-roll when the narrator discusses analytics features"
- PDFs: "Reference the attached product documentation for accurate technical specifications. Show relevant diagrams as visual overlays."
- Logos: "Display the company logo in the intro and end card scenes"

**Rule: Always upload. Always describe.** Uploading costs nothing. Under-providing costs quality.

**Adapt, don't interrogate.** If someone says "60-second product demo for developers about our new API," you already have purpose, audience, duration, and topic. Skip to what's missing: "What tone? And do you have any screenshots of the API in action?"

**Multi-topic split rule.** If the user describes multiple distinct topics, recommend splitting into separate videos. Explain: "HeyGen produces dramatically better results with one topic per video. Want me to plan two shorter videos instead?"

When you have enough to write a script, move to Phase 2.

---

## Phase 2 — Script

Write a narrator script using these rules:

### Pacing
- **150 words per minute.** This is the natural narrator pace. Non-negotiable ceiling.
- 30s = ~75 words. 60s = ~150 words. 90s = ~225 words. 2 min = ~300 words.
- Count the words. If over budget, cut. Never deliver over-length.

### Duration Padding Rule (1.4x)

Video Agent consistently delivers ~70% of target duration. To compensate, **use 1.4x the user's target duration when calculating word budget.**

If user wants 60s, budget for 84s (126 words at 150 wpm → write ~190 words). This compensates for Video Agent's ~70% compression.

| User wants | Script budget | Tell Video Agent |
|------------|--------------|------------------|
| 30s | 63 words (42s) | "45-second video" |
| 60s | 126 words (84s) | "85-second video" |
| 90s | 189 words (126s) | "130-second video" |
| 120s | 252 words (168s) | "170-second video" |

Based on observed data: 30s target → actual 20s (67%), 60s target → actual 36-47s (60-78%), 120s target → actual 84s (70%). The 1.4x padding brings actual output within 15% of the user's target.

### Structure by Type

**Product Demo:** Hook (5s) → Problem (10s) → Solution demo (30s) → CTA (15s)
**Explainer:** Context (10s) → Core concept (35s) → Takeaway (15s)
**Tutorial:** What we'll build (5s) → Steps (45s) → Recap (10s)
**Sales Pitch:** Pain (10s) → Vision (15s) → Product (25s) → CTA (10s)
**Announcement:** News hook (5s) → What changed (20s) → Why it matters (25s) → What's next (10s)

### Voice Rules
- Write for the ear, not the eye. "You can see your analytics update live" not "Real-time analytics updates are displayed."
- Short sentences. Nothing over 20 words.
- Active voice. "You can" not "It is possible to."
- Conversational. Contractions are good. "You'll" not "You will."
- Use scene breaks for natural pacing. Each scene transition creates a pause. No need for explicit pause markers.

### Asset Cues
If user provided assets, mark them: `[SHOW: dashboard.png]` at the moment they should appear.

### Present the Script

Show the user:
```
Here's the script (147 words, ~59 seconds):

[SHOW: dashboard-overview.png]
"Your analytics dashboard just got a lot smarter."

"Instead of digging through reports, you get insights the moment you log in."
[SHOW: ai-insights-panel.png]
"See that predictions tab? It learns your patterns..."
...

Want to adjust anything? I can tweak the tone, shorten it, rework a section, or we can go straight to generation.
```

**If user says "looks good" or "generate it"** → Phase 3.
**If user says "just make it" or "skip the script"** → Phase 3, use brief as prompt basis.
**If user has feedback** → Revise and re-present.

---

## Phase 3 — Prompt Engineering

Transform the script/brief into an optimized Video Agent prompt. The user doesn't see this phase unless they ask.

### Prompt Construction Rules

1. **Narrator framing.** Always frame as: "A [tone] narrator [explains/walks through/presents]..." Never "Create a video about..."
2. **Duration signal (PADDED).** When signaling duration to Video Agent, use **1.4x the user's target**. If user wants 60s, tell Video Agent "This is an 85-second video." Video Agent will compress it to approximately the right length. See the Duration Padding table in Phase 2 for exact values. The user-facing review should still show the user's original target.
3. **Asset anchoring.** If assets exist, be SPECIFIC about how to use them: "Use the attached product screenshots as B-roll when discussing features." "Reference the attached PDF for accurate technical specifications." Vague references = random placement.
4. **Tone calibration.** Use specific tone words: "confident and conversational" / "energetic, like a tech YouTuber" / "calm and authoritative, like a Bloomberg anchor" / "warm and approachable, like explaining to a friend."
5. **One topic.** If the script covers one topic cleanly, state it explicitly: "This video covers ONE topic: [topic]."
6. **Negative prompts ONLY when user explicitly asks.** Do NOT add negative constraints by default. Only use "No stock footage transitions" or "No text-on-screen overlays" if the user specifically says they want a minimal/clean look. By default, INCLUDE text overlays, motion graphics, and visual variety. These make videos better.

### Visual Style Block (ALWAYS INCLUDE)

Every prompt should include a visual style block. Without it, visuals look inconsistent scene-to-scene. Default to this unless the user specifies otherwise:

```
Use minimal, clean styled visuals. Blue, black, and white as main colors.
Leverage motion graphics as B-rolls and A-roll overlays. Use AI videos when necessary.
When real-world footage is needed, use Stock Media.
Include an intro sequence, outro sequence, and chapter breaks using Motion Graphics.
```

If the user provides brand colors or style preferences, replace with their specs. You can specify exact hex codes: "Use #1E40AF as primary blue, #F8FAFC as background white."

### Style Descriptor Presets

Match the user's context to a visual style. Add the corresponding prompt text:

| Style | Best For | Prompt Addition |
|-------|----------|-----------------|
| Minimalistic | Corporate, Tech, SaaS | "Use minimalistic, clean visuals with lots of white space" |
| Cartoon/Animated | Education, Kids content | "Use cartoon-style illustrated visuals" |
| Bold & Vibrant | Marketing, Social | "Use bold, vibrant colors and dynamic visuals" |
| Cinematic | Brand films, High-end | "Use cinematic quality visuals with dramatic lighting" |
| Flat Design | Modern, App demos | "Use flat design style with geometric shapes" |
| Gradient Modern | Tech, Startup | "Use modern gradient backgrounds and sleek transitions" |
| Retro/Vintage | Nostalgia, Creative | "Use retro-inspired visuals with warm tones" |

Default to **Minimalistic** for developer/tech content. Ask the user if unsure.

### Media Type Direction

Tell Video Agent which media types to use in each section. Use this decision matrix:

| Content Type | Motion Graphics | AI Generated | Stock Media |
|---|---|---|---|
| Data/Statistics | ✅ Best | ❌ | ❌ |
| Abstract Concepts | ✅ Good | ✅ Best | ❌ |
| Real Environments | ❌ | ⚠️ Can work | ✅ Best |
| Brand Elements | ✅ Best | ❌ | ❌ |
| Human Emotions | ❌ | ⚠️ Uncanny | ✅ Best |
| Custom Scenarios | ⚠️ Limited | ✅ Best | ⚠️ May not exist |
| Technical Diagrams | ✅ Best | ❌ | ❌ |

When constructing scene-by-scene prompts, pick the right media type for each scene based on what that scene is showing. Explicitly state the media type in the scene description, e.g. "Visual: (Motion Graphics) Animated chart showing API response times"

### Scene-by-Scene Prompting (For Longer/Complex Videos)

For videos over 60 seconds or when the user needs precision, structure the prompt as scenes:

```
Scene 1: [Scene Type, e.g. "Intro (Motion Graphics)"]
  Visual: [Describe exact visual]
  VO: "[What the avatar says]"
  Duration: [Length]

Scene 2: [Scene Type, e.g. "Hook (A-roll with overlay)"]
  Visual: [Describe exact visual]
  VO: "[Script line]"
  Duration: [Length]
```

Scene types to use: Intro, Hook, Problem Statement, Solution, Feature Showcase, Benefits, CTA, End Card. Mix A-roll (avatar speaking) with B-roll (visuals only) and Motion Graphics overlays.

### The Script-as-Prompt Approach (PREFERRED for Full Producer Mode)

The single biggest upgrade: paste the FULL script directly into the prompt. Video Agent follows it scene-by-scene while improving flow, timing, and visuals automatically. When in Full Producer mode, ALWAYS construct a scene-labeled script with visual directions and VO text, then send the entire thing as the prompt.

### Avatar and Voice Selection

Video Agent auto-selects an appropriate avatar and voice based on the prompt content. To influence the selection, describe the presenter in the prompt:
- **Avatar:** "Use a professional female avatar with a warm, confident delivery"
- **Voice:** "The narrator should have a calm, authoritative male voice with an American accent"
- **No avatar:** "No avatar needed, only voice-over narration" (must be explicit or Video Agent defaults to showing an avatar)

Video Agent does not accept `avatar_id` or `voice_id` parameters. All selection is prompt-driven.

### Orientation Mapping
- YouTube / web / LinkedIn → `landscape`
- TikTok / Reels / Shorts → `portrait`
- Default if unspecified → `landscape`

Note: Aspect ratio is controlled through the prompt description ("landscape video" or "portrait/vertical video"). The API does not have a separate `aspect_ratio` parameter.

### Prompt Structure (IMPORTANT: Stack style at the end)

Put content/script FIRST, then style directives at the bottom. This keeps creative intent clean and technical specs organized.

```
[Scene-by-scene script with Visual + VO + Duration for each scene]

[Asset anchoring instructions if applicable.]

[Negative constraints if applicable.]

---
[Visual style block: colors, fonts, style descriptor]
[Media type directions: when to use motion graphics vs stock vs AI-generated]
[Intro/outro/chapter break instructions]
```

### Advanced Visual Techniques (Conditional Load)

For videos over 90 seconds OR when the user requests "cinematic" or "production quality", read `references/prompt-craft.md` for advanced visual techniques.

### One-Shot Mindset (CRITICAL)

The API call is one-shot. There is no back-and-forth with Video Agent. Every generation is a fresh call. This means the prompt MUST be as complete and precise as possible on the first attempt. The skill's entire job is to maximize the chance of success on that single generation. Don't rely on iteration with the API. Do ALL the work upfront: scene structure, visual style, media types, asset anchoring, pacing. The better the prompt, the fewer re-generations needed.

Note: The Video Agent web UI supports conversational iteration within a session. The API (`/v1/video_agent/generate`) is one-shot — every call is a fresh generation. This skill uses the API.

**NEVER send a flat paragraph as the prompt.** Always structure it as scenes with Visual + VO + Duration. Always include the visual style block. Always specify media types per scene. A flat script with no visual direction produces generic, forgettable videos. A scene-structured prompt with style and media directions produces professional results.

### Complete Prompt Example

Brief: "60-second product demo about HeyGen's Video Agent API for developers, casual-confident tone"

This is the FULL assembled prompt exactly as it would be sent to the API (using 1.4x padding → 85-second budget):

```
A casual-confident narrator walks developers through HeyGen's Video Agent API, showing how one API call produces a complete video. This is an 85-second video covering ONE topic: the Video Agent API.

Scene 1: Intro (Motion Graphics) — 8s
  Visual: (Motion Graphics) HeyGen logo animates in on dark blue background. Title text "Video Agent API" types on below.
  VO: "What if you could generate a full production video with a single API call? No timeline. No editing. Just one prompt."

Scene 2: The Problem (A-roll) — 12s
  Visual: (A-roll) Narrator speaking to camera in a modern workspace.
  VO: "Building video into your app used to mean stitching together templates, managing assets, and wrestling with rendering pipelines. That's a lot of engineering for a feature your users expect to just work."

Scene 3: The Solution (B-roll — Motion Graphics) — 15s
  Visual: (Motion Graphics) Animated code snippet showing a simple curl request to /v1/video_agent/generate. The JSON payload highlights the "prompt" field. A response animation shows video_id appearing.
  VO: "Video Agent changes that. Send a prompt describing what you want. The API handles scene planning, avatar selection, B-roll, transitions, and rendering. You get back a video ID."

Scene 4: How It Works (A-roll + overlay) — 15s
  Visual: (A-roll + overlay) Narrator on left 35%. Right 65% shows an animated pipeline: Prompt → Scene Planning → Asset Selection → Rendering → Delivered.
  VO: "Under the hood, Video Agent breaks your prompt into scenes, picks the right visuals for each one, selects an avatar and voice that match your tone, and renders the whole thing. Typical turnaround: two to three minutes."

Scene 5: Use Cases (B-roll — Motion Graphics) — 15s
  Visual: (Motion Graphics) Three cards cascade in showing use cases: "Personalized Sales Videos", "Auto-Generated Tutorials", "Product Update Announcements". Each card has an icon and brief subtitle.
  VO: "Teams are using it for personalized sales outreach, auto-generated product tutorials, and weekly update videos that used to take a full production day."

Scene 6: CTA / End Card (Motion Graphics) — 10s
  Visual: (Motion Graphics) Dark background with "docs.heygen.com/video-agent" in large white text. HeyGen logo below. Subtle particle animation in background.
  VO: "One API call. Full production video. Check out the docs and start building."

---
Visual style: Minimalistic, clean visuals. #1E40AF as primary blue, #F8FAFC as background white, #1a1a1a for dark sections. Inter for UI text, JetBrains Mono for code snippets.
Media types: Motion Graphics for data, code, and diagrams. A-roll for narrator presence. No AI-generated footage needed.
Include an intro sequence with logo animation, chapter breaks between major sections using Motion Graphics, and a branded end card.
Use a professional male avatar with a calm, confident delivery and an American accent.
```

This prompt demonstrates all required elements: scene-by-scene structure with Visual + VO per scene, duration per scene (padded 1.4x), narrator framing, media type per scene, visual style block at the bottom, and avatar direction.

Proceed to Phase 3.5.

---

## Phase 3.5 — Prompt Review (Quality Gate)

**Exception: Quick Shot mode.** If the user explicitly said "just generate" or "don't ask questions" (Mode 3), skip the review entirely. Quick Shot respects the user's desire for speed. Go directly from Phase 3 to Phase 4.

Before sending the prompt to the API, get a **second opinion from an independent reviewer**. This is not self-review. This is a separate agent with fresh eyes evaluating the prompt objectively.

### Step 1: Spawn a Review Sub-Agent (and yield)

Use `sessions_spawn` to run a reviewer sub-agent. The reviewer MUST be a flagship model (never an inferior model). Read the reviewer instructions from `{baseDir}/references/reviewer-prompt.md` and include them as the task, followed by the constructed prompt.

```
Task for reviewer:
[contents of references/reviewer-prompt.md]

---
PROMPT TO REVIEW:
[the full constructed prompt]
```

After spawning the reviewer sub-agent, call `sessions_yield` to suspend your turn. The reviewer's result will arrive as your next message. Parse the verdict from that message and proceed accordingly. This makes the block mechanical, not instructional.

If the reviewer sub-agent doesn't respond within 2 minutes, proceed to generation without review. Note in delivery: "Quality review was skipped due to timeout."

### Step 2: Handle the Review

**APPROVE (score 8+):** The prompt is ready. Proceed to Phase 4.

**REVISE (score 5-7):** The reviewer found issues and provided a revised prompt. Use the reviewer's revised version directly. Do not second-guess the reviewer.

**REJECT (score <5):** Fundamental problems. Go back to Phase 3, address the reviewer's specific issues, reconstruct the prompt, and re-submit for review. Do not generate with a rejected prompt.



### Step 4: Production Review Report

Present the reviewer's assessment to the user. Keep it concise. This should feel like a real production team reviewed and signed off on the work.

```
📋 **Production Review**

**Structure** — [X] scenes | [breakdown, e.g. "2× A-roll, 2× B-roll (Motion Graphics), 1× Stock, 1× End Card"]
**Pacing** — [XXX words / ~XXs] | [target: XXs] | [status: ✓ within budget / ⚠️ X words over]
**Estimated cost** — ~[X] credits ([duration/60] minutes × 2 credits/min)

**Reviewer verdict:** [APPROVE/REVISE] — [score]/10

[If revisions were applied:]
**Revisions applied:** [specific changes from reviewer]

[If concerns exist:]
**Concerns:** [list any remaining concerns]

Ready to generate. Proceeding to render.
```

This report serves two purposes: it shows the user that quality control happened, and it gives them a last chance to intervene before the API call. If the user says nothing or approves, proceed to Phase 4.

---

## Phase 4 — Generate

### API Call

Submit to Video Agent:

**Without assets:**
```bash
curl -s -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "<the constructed prompt>"}'
```

**With assets (uploaded in Phase 1):**
```bash
curl -s -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<the constructed prompt with asset descriptions>",
    "files": [
      {"asset_id": "<uploaded_asset_id_1>"},
      {"asset_id": "<uploaded_asset_id_2>"}
    ]
  }'
```

Include ALL uploaded asset IDs in the `files` array. The prompt should describe how to use each one. Video Agent will reference the assets based on your prompt directions.

Response on success:
```json
{"error": null, "data": {"video_id": "abc123", "session_id": "def-456-789"}}
```

Extract both `video_id` and `session_id` from the response.

### Error Handling

| Error | Action |
|-------|--------|
| 401 Unauthorized | API key invalid. Tell user to check HEYGEN_API_KEY. |
| 402 Payment Required | Insufficient credits. Tell user. |
| 429 Rate Limited | Wait 60s, retry once. |
| 500+ Server Error | Retry once after 30s. If still failing, tell user HeyGen is having issues. |
| Network error | Retry once. |
| 200 but no video_id | Retry once. If still no video_id, tell the user: "The API accepted the request but didn't return a video ID. This is unusual. Try again or check the HeyGen dashboard." |

**Asset upload failure:** If an asset upload returns an error, log which asset failed and proceed without it. Tell the user: "Note: [filename] couldn't be uploaded. The video was generated without this asset."

On success, **immediately share the Video Agent session URL** so the user can follow along:

```
Video submitted! You can watch the production progress live:
🔗 https://app.heygen.com/video-agent/<session_id>

I'll notify you automatically when it's ready.
```

The session URL is available instantly. The user can watch scene planning, asset selection, and rendering in real-time while they do other things.

### Delivery: Check Status and Deliver When Done

After submitting the video, you are responsible for checking when it's done and delivering the result.

**Check the status** using: `curl -s -H "X-Api-Key: $HEYGEN_API_KEY" "https://api.heygen.com/v1/video_status.get?video_id=<video_id>"` — look for `status: "completed"` in the response.

**Polling cadence:**
1. First check at **2 minutes** after submission.
2. Then every **30 seconds** for the next 3 minutes.
3. Then every **60 seconds** up to 30 minutes.
4. After **30 minutes**, stop polling and send the user the session URL as fallback.

**When completed**, deliver the finished video URL: `https://app.heygen.com/videos/<video_id>`

**Video rendering failure:** If status returns `failed` or `error`, tell the user what went wrong. Offer to retry with the same prompt or adjust. Common causes: content policy violation, avatar rendering issue, system overload.

```
Your video is generating! I've set up automatic delivery.

🔗 Watch live: https://app.heygen.com/video-agent/<session_id>

I'll send you the finished video when it's ready (usually 1-3 minutes). You're free to keep chatting in the meantime.
```



---

## Phase 5 — Review and Deliver

When the video is ready:

1. **Share both URLs:**
   - **Video Agent session** (already shared in Phase 4): `https://app.heygen.com/video-agent/<session_id>` — shows the full production process
   - **Finished video page**: `https://app.heygen.com/videos/<video_id>` — direct link to the completed video (available once rendering is done)
2. **NEVER share the raw mp4 URL** from the API response (video_url field). Those are temporary S3 links with expiring TTL. They will break.

### Error Notes in Delivery

If any issues occurred during the pipeline, note them clearly:
- If quality review was skipped due to timeout: "Quality review was skipped due to timeout."
- If assets failed to upload: "Note: [filename] couldn't be uploaded. The video was generated without this asset."
- If the video was re-generated due to a failure: "Note: First render failed ([reason]). This is the result of the second attempt."

### Present the Review

```
Your video is ready! 🎬

🎬 Video Agent session: https://app.heygen.com/video-agent/<session_id>
🔗 Finished video: https://app.heygen.com/videos/<video_id>

Quick check against your brief:
✓ Duration: ~58s (target: 60s)
✓ Tone: casual-confident
✓ Topic: single-topic ✓
✓ Assets referenced: 2/2

Happy with it? Or want me to adjust?
→ Looks great, ship it
→ Make the opening punchier
→ Slow it down / speed it up
→ Try a completely different approach
```

### Completion Status Report

After delivering the video, always append a completion status:

```
STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
```

**Statuses:**

- **DONE** — Video completed, reviewer approved, duration within 15% of target. All good.
- **DONE_WITH_CONCERNS** — Video completed but with issues the user should know about. List each concern with a recommended fix. Examples: duration was >20% off target, reviewer had to REVISE the prompt, assets weren't used as directed.
- **BLOCKED** — Cannot proceed. State what's blocking (API error, insufficient credits, prompt rejected twice). State what was tried and recommend what user should do.
- **NEEDS_CONTEXT** — Missing information. State exactly what's needed.

Format in delivery:
```
📊 **Status: DONE**
All checks passed. Duration within target. Reviewer approved first pass.
```

```
📊 **Status: DONE_WITH_CONCERNS**
⚠️ Duration was 25% under target (45s vs 60s target). Recommend re-generating with a longer script.
⚠️ Reviewer revised the prompt (score 6/10 → improved). Original had weak scene transitions.
```

```
📊 **Status: BLOCKED**
❌ API returned 402 (insufficient credits) on two attempts.
Tried: waited 60s, retried. Same error.
Recommendation: Check your HeyGen account credits at app.heygen.com/settings.
```

### Escalation Rule

**If the reviewer REJECTs the prompt twice (score <5 both times), STOP.** Do not loop. Do not try a third time. Bad work is worse than no work.

Report to the user:
```
📊 **Status: BLOCKED**
❌ Prompt was rejected by quality review twice. Issues:
  1. [First rejection reason]
  2. [Second rejection reason]
This means the brief may need fundamental rework. Let's step back and revisit what this video should accomplish.
```

### Self-Evaluation Log Entry

After EVERY video generation (successful or not), write a JSON line to `heygen-video-producer-log.jsonl` in the workspace root:

```bash
echo '{"timestamp":"<ISO-8601>","video_id":"<video_id>","session_id":"<session_id>","prompt_type":"full_producer|enhanced|quick_shot","target_duration":<user_target_seconds>,"actual_duration":<actual_or_null>,"duration_ratio":<actual/target_or_null>,"reviewer_score":"<X/10>","reviewer_verdict":"APPROVE|REVISE|REJECT","word_count":<script_words>,"scene_count":<num_scenes>,"status":"DONE|DONE_WITH_CONCERNS|BLOCKED","concerns":["<list>"],"what_worked":"<brief>","what_to_improve":"<brief>","topic":"<topic>"}' >> /Users/heyeve/.openclaw/workspace/heygen-video-producer-log.jsonl
```

**Always log.** Even blocked or failed attempts. The log is how we learn. If `actual_duration` isn't known yet (video still rendering), log what you know and note `"actual_duration": null`.

### Iteration Loop

If user wants changes:
1. **Track what was tried.** Don't repeat a failed approach.
2. **Adjust the prompt** based on feedback. Be specific in changes.
3. **Re-generate** → re-poll → re-review.
4. **No iteration cap.** Keep going until the user is happy or decides to stop.

**Iteration intelligence:**
- "Make it punchier" → Add energy words to opening, shorten first sentence, front-load the hook harder
- "Slow it down" → Reduce word count by 15-20%, add shorter scenes with more breathing room
- "Different approach" → Restructure the script, try a different tone, change the opening
- "The assets aren't showing" → Strengthen asset anchoring language, be more explicit about timing
- Never retry with the exact same prompt. Always change something.

---

## Best Practices (Encoded Knowledge)

These are things a good producer knows. They're baked into the phases above, but listed here for reference when making judgment calls:

1. **Front-load the hook.** First 5 seconds = 80% of retention. Always open with the most compelling statement. Never open with context-setting.
2. **One idea per video.** Video Agent handles single-topic dramatically better than multi-topic.
3. **Write for the ear.** If you wouldn't say it out loud to a friend, rewrite it.
4. **150 words/min ceiling.** Faster sounds rushed. Slower sounds boring.
5. **Strategic pacing.** Scene breaks and short sentences create natural rhythm. Let the scene structure breathe.
6. **Asset anchoring > asset dumping.** Tell the agent WHEN to show each asset, tied to specific script moments.
7. **Narrator framing > generic framing.** "A confident narrator explains..." always outperforms "Create a video about..."
8. **Tone specificity matters.** "Casual-confident, like a tech YouTuber" >> "professional."
9. **Duration signaling.** Explicitly state target seconds in the prompt. Video Agent respects this.
10. **Negative prompts work.** "No stock transitions" or "No text overlays" when the user wants a clean look.

---

## Quick Reference

### API Endpoints
- Generate: `POST https://api.heygen.com/v1/video_agent/generate` **(ALWAYS use this. NEVER use v2/video/generate)**
- Status: `GET https://api.heygen.com/v1/video_status.get?video_id=<id>`
- Auth header: `X-Api-Key: $HEYGEN_API_KEY`
- Cost: 2 credits/minute of generated video

### Advanced Prompt Optimization (Experimental)
For production-quality scene-by-scene prompts, see `references/prompt-craft.md`. Auto-loaded for videos over 90s or "cinematic"/"production quality" requests. Covers visual layer system, motion vocabulary, and named visual styles. Note: these advanced techniques are experimental and not fully validated.

---

## Evaluation

Run evals to test prompt quality without spending credits:

1. Read `evals/run-eval.md` and follow instructions — produces prompts for 8 test cases and scores them
2. Compare results with `evals/compare.md` — diffs two eval runs to catch regressions
3. Baselines from batch test (Mar 24, 2026) in `evals/test-prompts.json`
