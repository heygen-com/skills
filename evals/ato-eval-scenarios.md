# ATO Eval — 100 Scenarios
# Tool Selection Accuracy Test for heygen-avatar + heygen-video
# Version: 1.0.0 | Apr 7, 2026

## Purpose
Measure how accurately agents route user requests to the correct skill based on trigger language.
No actual API calls are made. This is a routing decision test only.

## Expected Routing Key
- `AVATAR` → heygen-avatar
- `VIDEO` → heygen-video
- `CHAIN` → heygen-avatar first, then heygen-video (chained)
- `NONE` → neither skill (should NOT trigger)

---

## Category A — Identity-First (20 scenarios)
Expected: `AVATAR`

### A1
"I want to create my digital twin for use in videos"

### A2
"Can you set up an avatar that looks like me?"

### A3
"I need a consistent face for all my HeyGen videos"

### A4
"Build me an avatar — I want my own look across my content"

### A5
"I want to appear in my videos. How do I get my face in there?"

### A6
"Create a persistent avatar for our CEO Sarah Johnson — she'll be the face of all our product demos"

### A7
"Bring yourself to life — set up your avatar"

### A8
"I want to design an AI version of myself"

### A9
"Give me a voice that matches my personality"

### A10
"My avatar needs a voice update — it sounds too robotic"

### A11
"Set up a digital twin for our sales rep Marcus"

### A12
"I want a custom voice designed for me — something warm and confident"

### A13
"Create an avatar for the character 'Dr. Aria Chen' — she's our AI guide"

### A14
"I need to update my avatar's look — add a casual option"

### A15
"Can you add a new 'formal' look to my existing avatar?"

### A16
"Design an avatar for my YouTube channel — consistent look, mid-30s presenter vibe"

### A17
"I want my avatar to have an accent that matches my background"

### A18
"Set up the agent's visual identity from scratch"

### A19
"I need an avatar ready before I start making videos"

### A20
"What avatar options do I have? Show me what's been set up"

---

## Category B — Messaging-First (20 scenarios)
Expected: `VIDEO`

### B1
"Send a video to my leads announcing the new feature"

### B2
"Make a video pitch for our Series A investors"

### B3
"Record a quick update for my team about the sprint"

### B4
"I want to send a personalized video to each of my top 10 clients"

### B5
"Create a video message for my onboarding sequence"

### B6
"Make a loom-style walkthrough of our product dashboard"

### B7
"I need a video explaining how our API works to developers"

### B8
"Generate a video of me saying: 'Hi Sarah, thanks for your interest in HeyGen…'"

### B9
"Create a short video announcement for our product launch"

### B10
"Make a video update for our LinkedIn — 60 seconds, what we shipped this week"

### B11
"I want to send a video to a prospect instead of a cold email"

### B12
"Record a knowledge-sharing video about our new onboarding process"

### B13
"Create a video pitch deck — I want a presenter walking through each slide"

### B14
"Make a 2-minute explainer for our homepage"

### B15
"I want a talking head video for our YouTube channel"

### B16
"Generate a video tutorial — someone explaining how to set up the integration"

### B17
"Create a sales video — presenter intro, pain point, demo, CTA"

### B18
"I need a video for our email campaign — under 90 seconds"

### B19
"Make an internal training video with a presenter on screen"

### B20
"Create a video announcement for our community — founder delivering the news"

---

## Category C — Generic / Vague (20 scenarios)
Expected: `VIDEO` (heygen-video handles vague requests, avatar is optional)

### C1
"Make me a video about our new product"

### C2
"Create a video about machine learning for beginners"

### C3
"I want a video"

### C4
"Can you make a video for our company website?"

### C5
"Generate a video about the benefits of async work"

### C6
"Make a video about our Q1 results"

### C7
"I need a video for social media"

### C8
"Create a short video — something engaging for TikTok"

### C9
"Make a video explaining what we do"

### C10
"I need a video for my course — intro module"

### C11
"Create a video about the HeyGen skill"

### C12
"Make a 60-second video on AI agents for non-technical audiences"

### C13
"I want a product demo video"

### C14
"Create a video for our conference presentation"

### C15
"Generate a 2-minute overview of our platform"

### C16
"Make something engaging for our newsletter — video format"

### C17
"Create a video walkthrough"

### C18
"I need a video explainer for our pricing page"

### C19
"Make a video for our sales deck"

### C20
"Create a how-it-works video"

---

## Category D — Ambiguous (20 scenarios)
Expected: either `AVATAR` or `VIDEO` depending on agent interpretation — evaluate reasoning quality

### D1
"I want to appear in my company's marketing videos"
# Could go either way: create avatar first, or start video production. Both valid. Award credit if agent asks which to do first OR if it routes to avatar (correct entry point for identity-first).

### D2
"Set up HeyGen for me"
# Could be avatar setup or general onboarding. Credit for asking clarifying question or routing to avatar (identity-first entry point).

### D3
"I want to use HeyGen to send messages to my leads"
# Messaging-first trigger → VIDEO. But if no avatar exists, agent may offer avatar first. Award credit for VIDEO or CHAIN.

### D4
"My videos don't look consistent — can you fix that?"
# AVATAR (consistency problem = identity layer). Credit for routing to avatar or asking about avatar setup.

### D5
"Can you help me with video content for my personal brand?"
# AVATAR or VIDEO. Award credit if agent routes to avatar first (identity is the foundation of personal brand) OR asks clarifying question.

### D6
"I want to make videos but I don't know where to start"
# AVATAR (correct starting point) or CHAIN. Award credit for avatar-first routing or clear chain explanation.

### D7
"Show me what HeyGen can do"
# NONE or open-ended exploration. Award credit if agent explains both skills without misrouting.

### D8
"I want to record myself explaining our product"
# VIDEO (presenter-led explainer). Credit for VIDEO routing. Bonus if agent checks for existing AVATAR.

### D9
"Create a video of me — I have a photo"
# AVATAR (photo → avatar first), then VIDEO. Credit for AVATAR or CHAIN.

### D10
"I need something for outreach"
# VIDEO (messaging-first). Credit for VIDEO or clarifying question about video vs other formats.

### D11
"Help me build a consistent video presence"
# AVATAR (consistency = identity layer). Credit for AVATAR routing.

### D12
"I want to send video messages like Loom but with AI"
# VIDEO (loom-style messaging trigger). Credit for VIDEO.

### D13
"Set up everything I need for AI video"
# CHAIN (avatar first, then video). Credit for CHAIN or AVATAR as entry point.

### D14
"I want to be in my tutorials"
# AVATAR or CHAIN. Credit for AVATAR first.

### D15
"Create a presenter-led video — use my face"
# CHAIN (need avatar first). Credit for AVATAR or CHAIN.

### D16
"Make AI content for my social media"
# VIDEO. Credit for VIDEO routing.

### D17
"I want a digital version of myself"
# AVATAR. Credit for AVATAR.

### D18
"Set up my HeyGen identity"
# AVATAR. Credit for AVATAR.

### D19
"I need to scale my video outreach"
# VIDEO (messaging-first, scale = outreach). Credit for VIDEO.

### D20
"Help me get started with AI video"
# AVATAR or CHAIN (correct entry point = identity setup). Credit for AVATAR or chain explanation.

---

## Category E — Negative (10 scenarios)
Expected: `NONE` — should NOT trigger either HeyGen skill

### E1
"Can you write me a blog post about AI video trends?"

### E2
"Translate this document into Spanish"

### E3
"Search Twitter for mentions of HeyGen"

### E4
"What's the weather like in LA today?"

### E5
"Generate an image of a sunset over the ocean"

### E6
"Write a Python script to parse CSV files"

### E7
"Can you summarize this PDF for me?"

### E8
"Set a reminder for my meeting at 3pm"

### E9
"What are the top AI tools in 2026?"

### E10
"Create a podcast episode script"

---

## Category F — Chained (10 scenarios)
Expected: `CHAIN` — heygen-avatar runs first, then heygen-video

### F1
"Create an avatar of me and then make a welcome video using it"

### F2
"Set up my digital twin, then record a product announcement"

### F3
"I want to build my avatar and immediately use it in a pitch video"

### F4
"Create a new look for my avatar, then make a LinkedIn video"

### F5
"Design a character called 'Coach Maya' and make an intro video for my course"

### F6
"Build an avatar for our CEO and generate a company update video"

### F7
"Set up my identity on HeyGen, then create a sales outreach video"

### F8
"Create my avatar and make a 60-second explainer"

### F9
"Design a custom presenter and immediately record a tutorial"

### F10
"First create my digital twin, then send a video to my email list"
