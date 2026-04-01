# Round 12 — Push the Boundaries

**Goal:** Stress-test edge cases, creative extremes, and multi-step workflows that real users will throw at this skill. Every scenario should make the skill sweat.

## Scenarios

### S1 — Rapid-Fire Multi-Video (3 videos, 1 session)
**User prompt:** "I need 3 short videos for a social campaign: (1) a 15-second teaser about AI agents, (2) a 20-second 'did you know' fact video, and (3) a 15-second CTA to visit heygen.com. Use Eve Park for all three. Portrait format for all."
**Tests:** Multi-video request handling. Does the skill batch, sequence, or ask the user to split? How does it handle shared avatar across videos? Portrait + photo_avatar = Correction C for all three.
**Expected:** Clear guidance on multi-video workflow. Should NOT attempt a single 50-second video. Each video generated separately with consistent avatar.

### S2 — Extremely Long Script (5+ minutes)
**User prompt:** "Create a detailed 5-minute documentary-style video explaining the entire history of generative AI, from GANs in 2014 through diffusion models to today's video generation. Cover key milestones: StyleGAN, DALL-E, Stable Diffusion, Midjourney, Sora's rise and fall, and HeyGen's avatar technology. Use a professional male stock presenter. Cinematic style."
**Tests:** Long-form content handling. 5 min = 750 words at 150 WPM. Scene-by-scene structure at this length. Duration padding at 1.3x for 120s+. Stock avatar discovery. Does the skill warn about API limits or cost ($0.0333/sec × 300s = ~$10)?
**Expected:** Scene-by-scene mode, 8-10 scenes, stock avatar via group browse, cost awareness.

### S3 — Non-English Content (Korean)
**User prompt:** "한국어로 30초 영상을 만들어줘. 주제는 'AI 에이전트가 비즈니스를 바꾸는 3가지 방법'. Eve Park 아바타를 사용하고, 깔끔한 스타일로 해줘."
**Tests:** Non-English prompt handling. Korean script generation. Voice selection (Korean voice needed). Does SKILL.md address multilingual at all?
**Expected:** Korean script at 150 WPM equivalent, Korean voice discovered via /v3/voices with language filter, photo avatar.

### S4 — Contradictory Instructions
**User prompt:** "Make a 30-second video. Use a cinematic widescreen style. Portrait format. Use Eve Park but I don't want to see her face. Make it professional but fun and quirky. Serious tone."
**Tests:** Contradictory instruction resolution. Widescreen ≠ portrait. "Don't want to see face" ≠ avatar presenter. "Serious" ≠ "fun and quirky." Does the skill ask for clarification or silently pick a side?
**Expected:** Skill should surface contradictions and ask user to resolve before proceeding. NOT silently guess.

### S5 — Raw Image as Avatar (Photo Avatar Creation Path)
**User prompt:** "I want to use this photo as my avatar: https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/800px-Camponotus_flavomarginatus_ant.jpg. Make a 30-second video about nature documentaries."
**Tests:** Photo avatar creation from user-uploaded image. This is an ant photo (not a human face). Does the skill validate the image is a human face? Does it know how to create a photo avatar from an image? SKILL.md says "avatars only, never photo avatar creation APIs."
**Expected:** Skill should explain that custom photo avatars need to be created in the HeyGen dashboard first, and that the image must be a human face. Should NOT attempt to use the ant image as an avatar.

### S6 — Competitor Mention + Sensitive Content
**User prompt:** "Make a 45-second video comparing HeyGen to Synthesia. Explain why HeyGen is better. Use Eve Park. Make it spicy — really roast Synthesia."
**Tests:** Sensitive content handling. Brand comparison. "Roasting" competitors. Does the skill have any content guardrails? Does Video Agent reject it?
**Expected:** Skill should proceed (no content filtering is the skill's job) but the video output quality/tone is worth documenting. See if Video Agent self-moderates.

### S7 — Interactive Session Flow
**User prompt:** "I want to brainstorm a video concept with you interactively. Start an interactive session. My topic is launching a SaaS product."
**Tests:** Interactive session path (POST /v3/video-agents/sessions). Multi-turn conversation. Does SKILL.md explain this clearly enough? Does Adam know when to use interactive vs one-shot?
**Expected:** Interactive session created, multi-turn dialogue, eventually produces a video from the session.

### S8 — Style Override Mid-Flow
**User prompt:** "Make a 60-second video about remote work tips. Use Eve Park. Start with a bright, cheerful style."
**Follow-up (after dry-run or first draft):** "Actually, change it to dark and moody. Think noir documentary."
**Tests:** Style change after initial setup. Does the skill support mid-flow changes? Does it regenerate from scratch or try to modify? Prompt-injected style swap.
**Expected:** Skill should show dry-run first (or ask), then allow style change before generation. Clean restart of Phase 3 with new style.

### S9 — Massive Asset Bundle (4+ files)
**User prompt:** "Create a 2-minute investor pitch video. Here are my assets: Logo: https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/OpenAI_Logo.svg/1200px-OpenAI_Logo.svg.png, Chart 1: https://i.imgur.com/JjGkR9O.png, Chart 2: https://i.imgur.com/8QqK1xG.png, Team photo: https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800. Use Eve Park. Professional editorial style."
**Tests:** 4-asset routing. Multiple uploads to /v3/assets. Asset classification (logo vs chart vs photo). Does the skill handle all four or hit limits? Rate limiting on uploads?
**Expected:** All 4 assets uploaded, classified (logo=visual, charts=data, team=contextual), included in prompt with appropriate visual directions.

### S10 — Zero Guidance Stress Test
**User prompt:** "make me a video"
**Tests:** Absolute minimum input. No topic, no duration, no avatar, no style. How does Phase 1 discovery handle this? Does the skill ask good questions or just wing it?
**Expected:** Skill should enter discovery mode and ask at minimum: topic/subject, target duration, avatar preference. Should NOT generate a random video.
