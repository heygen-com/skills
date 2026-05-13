# Language & Locale Guide

The full canonical list comes from `heygen video-translate languages list`. Run
it at session start when the user requests anything non-trivial — the list
evolves and the skill should never hardcode it.

This reference is for **judgement calls** that the API doesn't make for you:
which regional variant to pick, where formality registers matter, where
lip-sync gets harder, and where source-text-on-screen will collide with the
dubbed output.

---

## Defaults for ambiguous user input

When the user says one of these, use the default unless they specify a region:

| User said | Default | When to ASK instead |
|-----------|---------|---------------------|
| "Spanish" | Spanish (Spain) | If the user mentions LATAM audience, Mexico, Argentina, etc. |
| "Portuguese" | ASK — split is critical | Always ask Portugal vs Brazil. They are not interchangeable for audiences. |
| "Chinese" / "Mandarin" | Chinese (Mandarin, Simplified) | If the user mentions Taiwan → Traditional. If Hong Kong → Cantonese. |
| "French" | French (France) | If the user mentions Quebec / Canadian audience. |
| "English" | English (United States) | If the user mentions UK, AU, IN audience. |
| "German" | German (Germany) | Rarely — Austria/Switzerland have meaningful differences but most German content uses Germany standard. |
| "Arabic" | Arabic (the pan-region option) | If the user names a country, use the country variant. |
| "Japanese" | Japanese (Japan) | Single canonical option. |
| "Korean" | Korean (Korea) | Single canonical option. |

---

## Tonal compression / expansion

Translated speech rarely matches the source's exact duration. `enable_dynamic_duration: true` lets the engine flex output timing so speech sounds natural. Without it, you get rushed or stretched audio.

| Direction | Typical compression | Notes |
|-----------|---------------------|-------|
| English → Mandarin Chinese | ~25–35% shorter | Highest compression. `enable_dynamic_duration` is non-negotiable. |
| English → Japanese | ~20–30% shorter | But adds politeness markers that vary by register. |
| English → Korean | ~15–25% shorter | Honorific levels affect length. |
| English → Spanish | ~10–15% LONGER | Spanish is wordier than English. |
| English → German | ~5–15% LONGER | Compound nouns can extend phrasing. |
| English → Arabic | ~15–25% LONGER | Plus RTL caption rendering. |
| English → French | ~10–15% LONGER | Romance languages run longer. |
| German → English | ~10–20% shorter | |
| Japanese → English | ~25–40% LONGER | Japanese drops subjects/objects English must restate. |
| Spanish → English | ~5–10% shorter | |

**Recommend `enable_dynamic_duration: true` for visual translation** (this is the Phase 1 "duration flexibility" question). The only time to set it `false`: the user explicitly needs fixed-length output (e.g., ad slot, synced timeline, music beats). If they choose fixed-length on a high-compression pair (en→zh, en→ja), warn that quality will degrade — the proofread workflow with manual SRT adjustment is the better path for those cases.

---

## Formality / register

The engine defaults to **neutral-formal** in most languages. If the source is
casual conversational and the user wants the dub to match register, this is a
judgement call:

| Language | Register concern | Default | Override path |
|----------|------------------|---------|----------------|
| Japanese (ja-JP) | 敬語 (keigo) levels: tameguchi (casual) → desu/masu (polite) → sonkeigo/kenjougo (honorific). Default lands at desu/masu. | Polite | Proofread: edit SRT to drop polite endings for casual feel. |
| Korean (ko-KR) | 7 speech levels. Default is haeyo-che (polite informal). | Polite informal | Proofread: replace endings (-요/-ㅂ니다) for register match. |
| German (de-DE) | Sie (formal "you") vs du (casual "you"). Default Sie. | Formal | Proofread: search/replace Sie→du, Ihr→dein, Sie haben→du hast, etc. |
| French (fr-FR) | tu vs vous. Default vous. | Formal | Proofread: tu/vous swap. |
| Spanish (es-ES) | tú vs usted (varies by region). Default tú in most LATAM, usted in formal Spain. | Mixed | Proofread per region. |
| Thai (th-TH) | Royal / polite / casual / colloquial registers, plus particles (ka/krap). Default polite + ka/krap. | Polite | Proofread: drop particles for casual. |
| Indonesian (id-ID) | Formal Bahasa vs colloquial. Default formal. | Formal | Proofread: relax to colloquial. |
| Vietnamese (vi-VN) | Pronoun system encodes hierarchy. Default neutral. | Neutral | Proofread per audience. |
| Hindi (hi-IN) | आप (aap) vs तुम (tum) vs तू (tu). Default aap. | Formal | Proofread for casual. |

Rule of thumb: **if the user tells you the source is conversational and the
target language has strong formality conventions (ja, ko, th, de, hi), default
to proofread mode** — even if the video is short.

---

## RTL languages

Right-to-left languages: Arabic, Hebrew, Urdu, Persian (Farsi), Pashto.

**Burned-in caption collision.** When `enable_caption: true`, the engine
renders captions as a lower-third overlay. RTL captions render right-justified.
If the source video has on-screen text, lower-third graphics, or speaker
chyrons in that area, the captions WILL collide visually.

**Action:** for RTL targets with any source-side lower-third graphics, default
to the proofreads workflow. Generate the SRT, deliver it as a sidecar caption
file, and let the user (or their editor) place captions where they don't
collide.

**Voice direction.** RTL is text-direction only — voice clone and audio dub
work the same as any other language.

---

## Regional Spanish variants

Spanish has the largest audience-perception gap of any major language. Picking
the wrong variant for an audience can sound foreign or off-putting.

| Variant | Audience | Notes |
|---------|----------|-------|
| Spanish (Spain) | Spain, some Spanish-speaking Europe | Castilian. "Vosotros" used. Z/C = θ. |
| Spanish (Mexico) | Mexico, US Hispanic (skews Mexican), much of Central America | Most-requested LATAM variant. Neutral-LATAM. |
| Spanish (Argentina) | Argentina, Uruguay | "Vos" instead of tú. Italian-influenced intonation. |
| Spanish (Colombia) | Colombia, parts of Andean region | Neutral, often considered "clearest" Spanish. |
| Spanish (Latin America) | Pan-LATAM | Generic LATAM. Use when audience is mixed-LATAM and Mexico-specific feels too regional. |
| Spanish (United States) | US Hispanic / US-centric Spanish content | Less common but real — anglicisms preserved. |

When the user just says "Spanish": ask once about audience. *"Latin America or
Spain? If Latin America: Mexico, broader LATAM, or somewhere specific?"*

---

## Regional Portuguese

Portuguese (Portugal) and Portuguese (Brazil) are NOT interchangeable. They
diverge significantly in vocabulary, grammar, and pronunciation. Brazilian
audiences will perceive European Portuguese as foreign and vice versa.

**Always ask. Never default.**

---

## Regional Chinese

| Variant | Audience |
|---------|----------|
| Chinese (Mandarin, Simplified) | Mainland China — 1.4B audience. The default for "Chinese". |
| Chinese (Taiwanese Mandarin, Traditional) | Taiwan — Traditional characters, distinct vocabulary. |
| Chinese (Cantonese, Traditional) | Hong Kong, Macau, Cantonese-speaking diaspora — different language entirely from Mandarin. |
| Chinese (Wu, Simplified) / others | Regional dialects within mainland — only when user specifies. |

Cantonese is NOT a Mandarin dialect — it's a different language with different
syntax and vocabulary. A Mandarin speaker can't understand spoken Cantonese.
If the user says "translate for Hong Kong", that's Cantonese. If they say
"translate for China", that's Mandarin (Simplified).

---

## Languages where lip-sync is harder

Lip-sync quality depends partly on phoneme overlap with the source. Languages
with significantly different mouth shapes from English:

- **Mandarin / Cantonese** — tonal phonemes don't map to English mouth shapes. Lip-sync is acceptable but visibly different from native.
- **Japanese** — strict mora-based phonology. Mouth shapes for /tsu/, /ryu/, /ja/ don't have direct English equivalents. Acceptable on talking-head; visibly off on close-ups.
- **Arabic** — pharyngeal consonants (ع, ح, خ, ق) require throat positions English doesn't use. Lip-sync passes but viewers may notice.
- **Russian** — palatalization adds mouth shapes English doesn't have.
- **Korean** — distinct unaspirated/aspirated/tense consonant trios.

For these, set viewer expectations slightly lower: lip-sync will be "natural
enough" but not photorealistic for close-ups. If the source is mostly
mid-shot / wide-shot, this is invisible. If the source is close-up
talking-head, propose a short test clip first.

---

## Source captions burned in

If the source video has captions burned in (subtitles in the source language
already on-screen), they will REMAIN in the source language in the dubbed
output. The translation engine doesn't re-render existing visuals.

If the user wants new-language captions: with `enable_caption: true`, you'll
get TWO caption tracks visible — the source's burned-in captions AND the new
target-language captions. This is almost never what the user wants.

**Action:** in Phase 2 source-quality triage, watch the first few seconds. If
you see burned-in captions, surface in Phase 1: *"Heads up — your source has
subtitles burned in already. Those will stay in the dubbed video. Want me to
turn off new captions to avoid two layers, or do you have a clean source
without subtitles?"*

---

## Multi-speaker languages

When `speaker_num >= 2`, the engine attempts speaker diarization and clones
each speaker's voice separately. This works well for:

- Two-host podcasts with distinct voices
- Interviews with clear turn-taking
- Two-person conversations with no overlap

It works poorly for:

- Overlapping speech (people talking over each other)
- Three+ speakers where two have similar voices
- Single-speaker content mistakenly tagged as multi-speaker

**Always ask the user to confirm the count.** Don't infer from metadata or
filename — count exactly. For >3 speakers, set expectations: results may
include voice swaps or merged voices.
