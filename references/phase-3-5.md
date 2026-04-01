# Phase 3.5 — Aspect Ratio & Background Pre-Check

Runs automatically when `avatar_id` is set, before Phase 4. Also runs in Quick Shot mode when avatar_id is present.

## Step 1: Fetch the avatar look metadata

```bash
curl -s "https://api.heygen.com/v3/avatars/looks/<avatar_id>" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Extract:
- `avatar_type`: `"photo_avatar"` | `"studio_avatar"` | `"video_avatar"`
- `preview_image_url`: use to determine orientation

## Step 2: Determine avatar orientation

Fetch the preview image and check pixel dimensions (width × height).
- width > height → landscape avatar
- height > width → portrait avatar
- Fetch fails or no preview → assume portrait (safer default)

## Step 3: Determine if background exists

| `avatar_type` | Background? | Reason |
|---|---|---|
| `studio_avatar` | ⚠️ Maybe | Check preview image — if transparent/solid/empty → "No background" |
| `video_avatar` | ✅ Yes | Recorded in a real environment |
| `photo_avatar` | ❌ No | Static photo, typically no scene background |

## Step 4: Build correction blocks

Based on Steps 2-3, build zero or more correction blocks. **All corrections are appended verbatim to the end of the prompt text.** Do NOT ask the user. Do NOT log without injecting.

### A) Portrait avatar → Landscape video (most common)

```
FRAMING NOTE: The selected avatar image is in portrait orientation (9:16) but
this video is landscape (16:9). YOU MUST generate a new variant of the avatar
image before using it in this video. Use AI Image tool to:
1. Generate a landscape (16:9) version of the presenter image
2. Generative fill to extend the scene horizontally — add a professional
   environment (modern studio, office, or setting matching the video tone)
3. Frame the presenter from chest up, centered in the landscape canvas
4. The background MUST be a real-looking environment, NOT a solid color,
   NOT transparent, NOT a gradient
Do NOT use the original portrait image uncropped. Do NOT add black bars or
pillarboxing. Do NOT leave a transparent or missing background.
```

### B) Landscape avatar → Portrait video

```
FRAMING NOTE: The selected avatar image is in landscape orientation (16:9) but
this video is portrait (9:16). YOU MUST generate a new variant of the presenter
image before using it. Use AI Image tool to:
1. Generate a portrait (9:16) version of the presenter image
2. Generative fill to extend vertically — add environment above and below
   the presenter (ceiling, floor, room depth) that looks natural
3. Focus on head and shoulders, presenter centered in portrait frame
4. The background MUST be a real-looking environment, NOT a solid color,
   NOT transparent, NOT a gradient
Do NOT use the original landscape image uncropped. Do NOT add letterboxing.
Do NOT leave transparent or missing background areas.
```

### C) Missing background — photo_avatar type

```
BACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static
photo — it has NO scene background (just the person, cutout-style). YOU MUST
generate a complete background environment before using this avatar. Use AI Image
tool to:
1. Generate a variant of the presenter image WITH a full background scene
2. For business/tech content: place in a modern studio, office with monitors,
   or professional podcast set with soft lighting and depth-of-field blur
3. For casual content: place in a bright room with natural light, plants,
   or a café-style setting
4. The presenter should look NATURAL in the environment — correct lighting
   direction, realistic scale (waist-up or chest-up framing), shadows present
5. Do NOT leave ANY transparent, solid-color, or gradient background
6. Do NOT make the presenter look oversized relative to the environment
   (the "giant in a room" effect means the scale is wrong — zoom out or
   reframe until the person looks like they naturally belong in the space)
The result should look like the presenter was actually filmed in that location.
```

## Correction Stacking Matrix

Corrections can stack. A portrait photo_avatar in a landscape video gets BOTH A and C.

| avatar_type | Orientation Match? | Has Background? | Corrections |
|---|---|---|---|
| `video_avatar` | ✅ matched | ✅ Yes | None |
| `video_avatar` | ❌ mismatched | ✅ Yes | Framing only (A or B) |
| `studio_avatar` | ✅ matched | ✅ Yes (check preview) | None |
| `studio_avatar` | ✅ matched | ❌ No | Background (C) |
| `studio_avatar` | ❌ mismatched | ✅ Yes | Framing only (A or B) |
| `studio_avatar` | ❌ mismatched | ❌ No | Framing (A or B) + Background (C) |
| `photo_avatar` | ✅ matched | ❌ No (always) | Background (C) |
| `photo_avatar` | ❌ mismatched | ❌ No (always) | Framing (A or B) + Background (C) |

**How to check if studio_avatar has a background:** Fetch `preview_image_url`. If transparent/checkered, solid color, or cutout → "No background" → inject C.

## Step 5: Log the correction

Add to learning log entry:
- `"aspect_correction"`: `"portrait_to_landscape"` | `"landscape_to_portrait"` | `"background_fill"` | `"both"` | `"none"`
- `"avatar_type"`: the raw value from the API
