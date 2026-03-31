# Round 5 Scenarios — Asset Classification & Attachment Strategy

Focus: Test the new Asset Classification Engine. Do assets get routed correctly (contextualize vs attach vs both)? Does the skill handle auth-walled URLs, public URLs, images, PDFs, and ambiguous intent without asking the user unnecessary questions? Also retests core flows from Round 4 to confirm no regressions.

12 scenarios total: 6 asset-focused (new), 4 core flow retests, 2 edge cases.

---

## S1: Public URL — Blog Post (VIDEO AGENT CAN CRAWL)
- **Prompt:** "Make a 45-second video summarizing this blog post: https://openai.com/index/introducing-chatgpt-pro/"
- **Mode:** Full Producer
- **Avatar:** Eve's Podcast (05bf07b91de446a3b6e5d47c48214857)
- **Orientation:** landscape
- **Asset:** One public URL (no auth required)
- **Watch for:** Skill should classify this as Path B (pass URL in `files[]`) because Video Agent can crawl public URLs. The skill should ALSO contextualize key points into the script (Path A+B is ideal). Does the skill try `web_fetch` to read the content for script writing AND pass the URL to the API?
- **Pass:** URL passed in `files[]`. Script contains specific facts from the article (not generic). Both paths used.

## S2: Auth-Walled URL — Notion Doc (VIDEO AGENT CANNOT ACCESS)
- **Prompt:** "Create a 30-second video overview of our GTM strategy based on this doc: https://www.notion.so/31e449792c6980978181f16d2fa8149f"
- **Mode:** Full Producer
- **Avatar:** Eve's Podcast (05bf07b91de446a3b6e5d47c48214857)
- **Orientation:** landscape
- **Asset:** One auth-walled Notion URL
- **Watch for:** Skill MUST recognize this is a Notion URL and fetch it using MCP tools (not pass it to Video Agent which would fail). Content should be contextualized into the script. Optionally convert to PDF and attach. Does the skill even think about accessibility?
- **Pass:** Skill fetches Notion content itself. Does NOT pass raw Notion URL to Video Agent. Script reflects actual page content.

## S3: Screenshot — Show On Screen
- **Prompt:** "Make a 30-second video about our dashboard. Use this screenshot." Then attach/reference an image URL: https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Google_Analytics_dashboard_screenshot.png/1280px-Google_Analytics_dashboard_screenshot.png
- **Mode:** Full Producer
- **Avatar:** Any stock studio_avatar
- **Orientation:** landscape
- **Asset:** One screenshot image
- **Watch for:** Skill should classify as Path B (attach). The image should be uploaded to HeyGen assets and described in the prompt as B-roll. The prompt should reference the screenshot at a specific scene ("Use the attached dashboard screenshot when discussing metrics").
- **Pass:** Image attached via `files[]` or uploaded as asset. Prompt specifically references it as visual B-roll.

## S4: PDF — Long Research Document
- **Prompt:** "Make a 60-second video about the findings in this research paper." Pass URL: https://arxiv.org/pdf/2310.06825
- **Mode:** Full Producer
- **Avatar:** Any stock studio_avatar
- **Orientation:** landscape
- **Asset:** One long PDF (research paper, many pages)
- **Watch for:** Skill should classify as Path A+B. Too long to fully embed in prompt, so summarize top 3-5 findings for the script. Also attach the PDF so Video Agent can extract relevant figures/charts. Does the skill handle the download? Does it summarize well?
- **Pass:** PDF attached AND key findings summarized in script. Script doesn't just say "see the paper" — it has specific content.

## S5: Multiple Assets — Screenshot + URL + Brand Guidelines Text
- **Prompt:** "Make a 45-second product launch video. Here's our product screenshot, our blog announcement, and brand colors are #1E40AF primary, #F97316 accent, white background."
- **Assets:**
  - Image: https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Dash_MERL_Center.jpg/1280px-Dash_MERL_Center.jpg
  - URL: https://developers.heygen.com/docs/quick-start (public docs page)
  - Text: brand guidelines (inline, not a file)
- **Mode:** Full Producer
- **Avatar:** Eve's Podcast (05bf07b91de446a3b6e5d47c48214857)
- **Orientation:** landscape
- **Watch for:** Three different asset types in one request. Each should be routed correctly: image → attach, URL → attach + contextualize, brand text → embed in visual style block. Does the skill handle multi-asset without asking "which should I attach?"
- **Pass:** All three assets correctly routed. Image attached. URL fetched and passed. Brand colors in style block. No unnecessary questions to user.

## S6: Ambiguous Asset — "Make a video about this PDF" (INTENT UNCLEAR)
- **Prompt:** "Make a 30-second video about this." Pass URL: https://arxiv.org/pdf/2310.06825
- **Mode:** Full Producer
- **Avatar:** Any stock studio_avatar
- **Orientation:** landscape
- **Asset:** One PDF, ambiguous intent (does user want to show the PDF or just talk about its content?)
- **Watch for:** This is the hardest classification case. "About this" could mean either path. Skill should default to A+B (both) without asking. Contextualize the key points AND attach. Does the skill handle ambiguity gracefully?
- **Pass:** Skill does NOT ask "should I attach this or summarize it?" — just does both. Video generates with specific content from PDF.

---

## S7: Core Retest — Quick Shot (REGRESSION CHECK)
- **Prompt:** "20-second video: 3 reasons every developer needs an AI video API"
- **Mode:** Quick Shot
- **Avatar:** No preference (test the Quick Shot avatar gap from R4)
- **Orientation:** landscape
- **Watch for:** R4 found a contradiction: "never auto-select" vs Quick Shot "generate immediately." Has this been addressed? Check if SKILL.md now has Quick Shot-specific avatar guidance.
- **Pass:** Quick Shot mode detected. Avatar handling is clear (either asks one question or has a documented default).

## S8: Core Retest — Dry-Run → Go (REGRESSION CHECK)
- **Prompt:** "Make a 45-second video about why Interactive Avatars are being replaced by LiveAvatars" with dry-run flag
- **Mode:** Full Producer, dry-run
- **Avatar:** Eve's Podcast (05bf07b91de446a3b6e5d47c48214857)
- **Orientation:** landscape
- **Watch for:** Dry-run preview format (one-liner, scene labels, tone cues, logline). Then "go" triggers generation. Same as R4 S5 but different topic.
- **Pass:** Dry-run preview correct. "Go" generates video. Session URL captured.

## S9: Core Retest — Interactive Session (R4 P1 REGRESSION)
- **Prompt:** "Let's iterate on a video concept. Topic: the death of Sora and what it means for AI video startups."
- **Mode:** Interactive Session
- **Avatar:** Any stock studio_avatar
- **Watch for:** R4 S9 was a P1 — interactive session stuck pending. Has the backend been fixed? Does the stop command trigger generation now? Document session behavior in detail.
- **Pass:** Either works end-to-end OR fails with clear error + session URL documented.

## S10: Core Retest — Voice-Over Only (REGRESSION CHECK)
- **Prompt:** "30-second voice narration about the future of agentic skills. No avatar."
- **Mode:** Full Producer
- **Avatar:** None (voice-over only)
- **Watch for:** Phase 3.5 skipped. No corrections. Voice discovery still happens. Clean path.
- **Pass:** Video generates voice-over only. No corrections injected.

---

## S11: Edge Case — URL Behind Paywall (DETECTION TEST)
- **Prompt:** "Make a 30-second video summarizing this article: https://www.wsj.com/tech/ai/openai-revenue-2025-01234567" (or any paywalled URL)
- **Mode:** Full Producer
- **Avatar:** Any stock studio_avatar
- **Orientation:** landscape
- **Asset:** One paywalled URL
- **Watch for:** Skill should attempt `web_fetch`, detect paywall/login wall, then fall back to Path A (contextualize what it CAN access — maybe the headline and first paragraph). Should NOT blindly pass to Video Agent. Does the skill handle the paywall gracefully?
- **Pass:** Skill detects paywall. Falls back to available content. Doesn't pass a useless URL to Video Agent. Communicates limitation to user if content is too thin.

## S12: Edge Case — Asset Classification + Phase 3.5 Stacking
- **Prompt:** "Make a portrait Instagram Reel using Eve's avatar. Here's a screenshot of our API docs to show on screen." Pass image: https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Google_Analytics_dashboard_screenshot.png/1280px-Google_Analytics_dashboard_screenshot.png
- **Mode:** Full Producer
- **Avatar:** Eve's Podcast (05bf07b91de446a3b6e5d47c48214857) (photo_avatar)
- **Orientation:** portrait (Instagram Reel)
- **Duration:** 30s
- **Asset:** One screenshot
- **Watch for:** This stacks TWO new concerns: (1) asset classification (screenshot → attach as B-roll) AND (2) Phase 3.5 corrections (photo_avatar portrait orientation → portrait video = match, but no background → background correction). Does the skill handle both correctly in one flow?
- **Pass:** Screenshot attached and referenced. Phase 3.5 triggers background correction (C) but NOT framing (orientation matches). Both concerns handled in one prompt.

---

## Round 5 Scoring Focus

For each scenario, the eval runner MUST document:
1. **Session URL** — captured from POST response (MANDATORY for every non-dry-run scenario)
2. **Asset classification decision** — what route was chosen per asset and why
3. **Was the user asked unnecessary questions?** (should be zero for most scenarios)
4. **Phase 3.5 behavior** — triggered when expected? corrections correct?
5. **Learning log** — assets_classified field present and accurate?
6. **Duration accuracy** — actual vs target vs padded

### New Columns for Asset Scenarios (S1-S6, S11-S12)

In addition to the standard eval format, add:

```
- **Assets Provided:** [list of assets with types]
- **Classification:** [per-asset: type, route chosen, reason]
- **User Questions Asked:** [0 if none — ideal. List any questions about asset routing.]
- **Video Agent Access:** [could Video Agent access the asset directly? yes/no per asset]
```

### Pass Criteria
- S1: URL in `files[]` + contextualized in script → PASS
- S2: Notion fetched by skill, NOT passed to Video Agent → PASS
- S3: Image attached, described as B-roll in prompt → PASS
- S4: PDF attached + summarized in script → PASS
- S5: All 3 assets correctly routed, zero user questions → PASS
- S6: Both paths used without asking user → PASS
- S7: Quick Shot mode, avatar handling clear → PASS
- S8: Dry-run correct, "go" works → PASS
- S9: Interactive session works OR documented failure → PASS
- S10: Voice-over, Phase 3.5 skipped → PASS
- S11: Paywall detected, graceful fallback → PASS
- S12: Asset classification + Phase 3.5 stacking correct → PASS
