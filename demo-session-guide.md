# HeyGen + Remotion Skills Demo Session Guide

A structured approach for testing the HeyGen and Remotion skills together, optimized for HeyGen's generation time.

## Prerequisites

1. Remotion project initialized (`npx create-video@latest`)
2. Skills installed in `.claude/skills/`
3. `.env` file with `HEYGEN_API_KEY`

---

## Phase 1: Kick Off HeyGen Early (Don't Wait)

**Prompt:**
```
Create a script for a 30-second explainer about how HeyGen and Remotion work together to create AI-powered videos. Then start generating the HeyGen avatar video using the script.

Important:
- Use an avatar with its default voice (get avatar details to find default_voice_id)
- Save the video_id to a file so we can check status later
- Don't wait for completion - just start the generation and move on
```

**Expected outcome:**
- Script written
- HeyGen generation started
- video_id saved to `heygen-pending.json` or similar
- Agent moves on without blocking

---

## Phase 2: Build Remotion Composition with Placeholder

**Prompt:**
```
While HeyGen generates, create a Remotion composition for the explainer video:

- Dimensions: 1920x1080
- FPS: 30
- Duration: estimate from script length (~150 words/minute)

Include:
- A dark gradient background (#0f0f23 to #1a1a2e)
- A placeholder div for the avatar video (positioned bottom-right, 40% width)
- An animated title "HeyGen + Remotion" that fades in at the start

Use a placeholder component that shows "[Avatar Video]" text so we can test the layout.
```

**Expected outcome:**
- New composition file created
- Root.tsx updated with composition
- Placeholder visible in Remotion Studio (`npm run dev`)

---

## Phase 3: Add Motion Graphics

**Prompt:**
```
Add animated text callouts that appear at different times during the video:

1. "AI Avatar Generation" - appears at 2 seconds with a spring animation from the left
2. "Programmatic Video Creation" - appears at 5 seconds from the right
3. "Seamless Integration" - appears at 8 seconds, centered

Each callout should:
- Use spring physics for smooth animation
- Have a subtle background pill/badge
- Fade out after 3 seconds

Also add a subtle animated gradient or particle effect in the background for visual interest.
```

**Expected outcome:**
- AnimatedCallout component created
- Callouts appear at correct times
- Spring animations working

---

## Phase 4: Check HeyGen Status & Integrate

**Prompt:**
```
Check if the HeyGen video is ready:
1. Read the video_id from the pending file
2. Check the video status
3. If completed:
   - Get the video URL and duration
   - Update the composition to use the real avatar video
   - Adjust composition duration to match the avatar video length
4. If still processing:
   - Tell me the current status and estimated wait time
```

**Expected outcome:**
- Status checked
- If ready: composition updated with real video URL
- Duration synced to actual avatar video length

---

## Phase 5: Polish & Lower Third

**Prompt:**
```
Add finishing touches:

1. A lower-third banner that appears in the last 4 seconds with:
   - Text: "Built with HeyGen + Remotion Skills"
   - Subtle slide-up animation
   - Semi-transparent dark background

2. Fade out the entire composition in the last 1 second

3. Make sure the avatar video is properly positioned and sized

Then render a preview so I can see the result.
```

**Expected outcome:**
- Lower-third component added
- Fade out transition at end
- Preview rendered

---

## Alternative: Single Consolidated Prompt

If you prefer one prompt that handles the full flow:

```
Create an explainer video about HeyGen and Remotion integration:

1. Write a 30-second script explaining how the two tools work together
2. Start HeyGen avatar generation with the script (use avatar's default voice, save video_id, don't wait)
3. While HeyGen processes, build a Remotion composition with:
   - 1920x1080, 30fps
   - Dark gradient background
   - Placeholder for avatar (bottom-right, 40% width)
   - Animated title "HeyGen + Remotion"
   - Text callouts appearing at intervals: "AI Avatars", "Programmatic Video", "Integration"
   - Spring animations for polish
4. Periodically check HeyGen status
5. When ready, integrate the real avatar video and adjust duration
6. Add a lower-third "Built with HeyGen + Remotion Skills"
7. Render preview

Start by kicking off the HeyGen generation, then build the Remotion composition while waiting.
```

---

## Tips for Best Results

- **Be specific about dimensions and timing** - helps agent make good defaults
- **Mention "spring animation"** - triggers use of Remotion's spring() function
- **Say "don't wait"** - prevents agent from blocking on HeyGen generation
- **Reference "default voice"** - triggers the avatar details → default_voice_id flow
- **Ask for preview render** - validates everything works end-to-end

---

## Troubleshooting

**HeyGen generation times out:**
- Check status manually: read the pending file, call status endpoint
- Generation can take 15+ minutes for longer scripts

**Avatar/voice mismatch:**
- Ensure agent used `/v2/avatar/{id}/details` to get `default_voice_id`
- Check the skills are properly installed in `.claude/skills/`

**Composition duration wrong:**
- Avatar video duration comes from status response
- Calculate frames: `Math.ceil(duration * fps)`

**WebM not working:**
- Only `normal` and `closeUp` styles supported
- Circle style requires MP4 + CSS border-radius masking
