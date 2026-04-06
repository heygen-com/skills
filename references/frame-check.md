# Frame Check — Aspect Ratio & Background Pre-Check

Runs automatically when `avatar_id` is set, before Generate. Also runs in Quick Shot mode when avatar_id is present.

## Step 1: Fetch the avatar look metadata

```bash
curl -s "https://api.heygen.com/v3/avatars/looks/<avatar_id>" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Extract:
- `avatar_type`: `"photo_avatar"` | `"studio_avatar"` | `"video_avatar"`
- `preview_image_url`: use to determine orientation

## Step 2: Determine avatar aspect ratio

Fetch the preview image and check pixel dimensions (width × height).

**Calculate the actual aspect ratio** (width/height for landscape, height/width for portrait):
- width > height → landscape avatar. Compute ratio = width / height.
- height > width → portrait avatar. Compute ratio = height / width.
- width == height → **square avatar** (1:1) → ALWAYS needs framing correction.
- Fetch fails or no preview → assume portrait (safer default).

**Then check if the ratio matches the target:**
- HeyGen Video Agent only accepts **16:9** (ratio ≈ 1.78) or **9:16** (ratio ≈ 1.78).
- If the avatar's ratio is NOT within ±0.05 of 1.78 (i.e., between 1.73 and 1.83), it needs a framing correction — even if it's the same orientation as the video.
- Common mismatches: 4:3 (1.33), 3:2 (1.50), 5:4 (1.25), 1:1 (1.00). All of these produce black bars or zoom artifacts.

**Examples:**
- 768×1024 portrait avatar (ratio 1.33) → 9:16 video: NEEDS correction (4:3 ≠ 9:16)
- 1024×1792 portrait avatar (ratio 1.75) → 9:16 video: OK (close enough to 16:9)
- 1024×768 landscape avatar (ratio 1.33) → 16:9 video: NEEDS correction (4:3 ≠ 16:9)
- 1920×1080 landscape avatar (ratio 1.78) → 16:9 video: OK (exact match)

## Step 2.5: Detect Avatar Visual Style

Examine the avatar's `preview_image_url` to classify its visual style. This determines how the generative fill environment should look. **The background must match the avatar's aesthetic.**

| Visual Style | Detection Signals | Fill Directive |
|---|---|---|
| **Photorealistic** | Real human photo, natural skin texture, camera-shot look | `HYPER PHOTO-REALISTIC environment. Real photography: actual office spaces, real studios, genuine room interiors with natural imperfections. NOT CGI. NOT stock photo. NOT 3D-rendered.` |
| **Animated / Illustrated** | Cartoon style, flat colors, cel shading, anime, illustrated character | `environment that MATCHES THE AVATAR'S ILLUSTRATED/ANIMATED STYLE. Use the same art style, color palette, and rendering technique as the avatar itself. If the avatar is cartoon-style, the background must be cartoon-style. If cel-shaded, the background must be cel-shaded. Do NOT use photorealistic backgrounds with illustrated avatars.` |
| **3D Rendered** | CG character, Pixar-like, game-style 3D model, smooth shading | `3D-RENDERED environment that matches the avatar's rendering style. Same lighting model, material quality, and level of stylization. Think game cutscene or animated film — consistent with the character's visual fidelity.` |
| **Stylized / Artistic** | Watercolor, sketch, pixel art, or other artistic rendering | `environment in the SAME ARTISTIC STYLE as the avatar. Match the medium (watercolor, sketch, pixel art, etc.), color palette, line weight, and texture. The background should look like it was created by the same artist using the same technique.` |
| **Unknown / Can't determine** | Preview fetch failed or ambiguous | Default to `HYPER PHOTO-REALISTIC` (safest for most avatars) |

**How to classify:** Look at the preview image. If the avatar looks like a photograph of a real person → Photorealistic. If it has visible brush strokes, flat colors, outlines, or cartoon features → Animated/Illustrated. If it looks like a 3D render (smooth surfaces, CG lighting) → 3D Rendered. If it's clearly an artistic style (watercolor, sketch) → Stylized.

Store the detected style as `avatar_visual_style` for use in correction blocks below. Use the corresponding Fill Directive text wherever `{FILL_DIRECTIVE}` appears in the correction templates.

## Step 3: Determine if background exists

| `avatar_type` | Background? | Reason |
|---|---|---|
| `photo_avatar` | ✅ Handled by Video Agent | Video Agent generates avatar + environment together during video creation. **No standalone bg correction needed.** |
| `studio_avatar` | ⚠️ Maybe | Check preview image — if transparent/solid/empty → "No background" → apply Correction C |
| `video_avatar` | ✅ Yes | Recorded in a real environment |

## Step 4: Build correction blocks

Based on Steps 2-3, build zero or more correction blocks. **All corrections are appended verbatim to the end of the prompt text.** Do NOT ask the user. Do NOT log without injecting.

Corrections are needed in TWO cases:
1. **Orientation mismatch** — avatar is portrait but video is landscape (or vice versa)
2. **Aspect ratio mismatch** — avatar and video share orientation but the avatar's ratio is NOT 16:9 / 9:16 (e.g., a 4:3 portrait avatar in a 9:16 video)

For case 2 (same orientation, wrong ratio), use **Correction F** (portrait) or **Correction G** (landscape).

### A) Portrait avatar → Landscape video (most common)

```
FRAMING NOTE: The selected avatar image is in portrait orientation (9:16) but
this video is landscape (16:9). YOU MUST generate a new variant of the avatar
image before using it in this video. Use AI Image tool to:
1. Generate a landscape (16:9) version of the presenter image
2. Generative fill to extend the scene horizontally — add a {FILL_DIRECTIVE}
3. Frame the presenter from chest up, centered in the landscape canvas
4. The background MUST visually match the avatar's own style and rendering.
   Correct lighting direction, natural shadows, consistent art style throughout.
   NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original portrait image uncropped. Do NOT add black bars or
pillarboxing. Do NOT leave a transparent or missing background.
```

Replace `{FILL_DIRECTIVE}` with the directive from Step 2.5 matching the detected `avatar_visual_style`.

### B) Landscape avatar → Portrait video

```
FRAMING NOTE: The selected avatar image is in landscape orientation (16:9) but
this video is portrait (9:16). YOU MUST generate a new variant of the presenter
image before using it. Use AI Image tool to:
1. Generate a portrait (9:16) version of the presenter image
2. Generative fill to extend vertically — add {FILL_DIRECTIVE}
   Extend above and below the presenter with environment consistent with their style.
3. Focus on head and shoulders, presenter centered in portrait frame
4. The background MUST visually match the avatar's own style and rendering.
   Correct lighting, natural shadows, consistent art style throughout.
   NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original landscape image uncropped. Do NOT add letterboxing.
Do NOT leave transparent or missing background areas.
```

Replace `{FILL_DIRECTIVE}` with the directive from Step 2.5 matching the detected `avatar_visual_style`.

### D) Square avatar → Landscape video

```
FRAMING NOTE: The selected avatar image is SQUARE (1:1) but this video is
landscape (16:9). HeyGen does not support square video output — without
correction, the video will have black bars on both sides. YOU MUST generate a
new variant of the avatar image before using it. Use AI Image tool to:
1. Generate a landscape (16:9) version of the presenter image
2. Generative fill to extend the scene horizontally — add a {FILL_DIRECTIVE}
   Extend on both sides with environment consistent with the avatar's visual style.
3. Frame the presenter centered in the landscape canvas
4. The background MUST visually match the avatar's own style and rendering.
   Correct lighting direction, natural shadows, consistent art style throughout.
   NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original square image uncropped. Do NOT add black bars or
pillarboxing. Do NOT leave a transparent or missing background.
```

Replace `{FILL_DIRECTIVE}` with the directive from Step 2.5 matching the detected `avatar_visual_style`.

### E) Square avatar → Portrait video

```
FRAMING NOTE: The selected avatar image is SQUARE (1:1) but this video is
portrait (9:16). HeyGen does not support square video output — without
correction, the video will have black bars on top and bottom. YOU MUST generate
a new variant of the presenter image before using it. Use AI Image tool to:
1. Generate a portrait (9:16) version of the presenter image
2. Generative fill to extend vertically — add {FILL_DIRECTIVE}
   Extend above and below the presenter with environment consistent with their style.
3. Frame the presenter centered in the portrait canvas
4. The background MUST visually match the avatar's own style and rendering.
   Correct lighting, natural shadows, consistent art style throughout.
   NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original square image uncropped. Do NOT add letterboxing.
Do NOT leave transparent or missing background areas.
```

Replace `{FILL_DIRECTIVE}` with the directive from Step 2.5 matching the detected `avatar_visual_style`.

### F) Non-16:9 portrait avatar → Portrait (9:16) video (same orientation, wrong ratio)

```
FRAMING NOTE: The selected avatar image is portrait but NOT 9:16 aspect ratio.
The video requires exactly 9:16 (1080×1920). Without correction, the video will
have black bars or zoom artifacts. YOU MUST generate a new 9:16 variant of the
avatar image before using it. Use AI Image tool to:
1. Generate a portrait (9:16) version of the presenter image
2. Generative fill to extend the canvas to exactly 9:16 — add {FILL_DIRECTIVE}
   Extend sides or top/bottom as needed to reach 9:16 without cropping the presenter.
3. Keep the presenter centered and naturally framed (head and shoulders for close-up,
   waist-up for wider shots)
4. The background MUST visually match the avatar's own style and rendering.
   Correct lighting direction, natural shadows, consistent art style throughout.
   NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original image uncropped. Do NOT add black bars or pillarboxing.
Do NOT leave a transparent or missing background.
```

Replace `{FILL_DIRECTIVE}` with the directive from Step 2.5 matching the detected `avatar_visual_style`.

### G) Non-16:9 landscape avatar → Landscape (16:9) video (same orientation, wrong ratio)

```
FRAMING NOTE: The selected avatar image is landscape but NOT 16:9 aspect ratio.
The video requires exactly 16:9 (1920×1080). Without correction, the video will
have black bars or zoom artifacts. YOU MUST generate a new 16:9 variant of the
avatar image before using it. Use AI Image tool to:
1. Generate a landscape (16:9) version of the presenter image
2. Generative fill to extend the canvas to exactly 16:9 — add a {FILL_DIRECTIVE}
   Extend sides or top/bottom as needed to reach 16:9 without cropping the presenter.
3. Keep the presenter centered and naturally framed (chest up, centered in canvas)
4. The background MUST visually match the avatar's own style and rendering.
   Correct lighting direction, natural shadows, consistent art style throughout.
   NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original image uncropped. Do NOT add letterboxing.
Do NOT leave transparent or missing background areas.
```

Replace `{FILL_DIRECTIVE}` with the directive from Step 2.5 matching the detected `avatar_visual_style`.

### C) Missing background — studio_avatar only

**Only for `studio_avatar` with transparent/solid/empty background. NOT for photo_avatar** (Video Agent handles photo_avatar environments during generation).

```
BACKGROUND NOTE: The selected studio avatar has NO scene background (transparent
or solid color). YOU MUST generate a background environment that MATCHES THE
AVATAR'S VISUAL STYLE before using this avatar. Use AI Image tool to:
1. Generate a variant of the presenter image WITH a full background scene.
   {FILL_DIRECTIVE}
2. For business/tech content: place in a modern studio, office, or podcast set.
   For casual content: place in a room, café, or outdoor scene.
   The setting should match both the content tone AND the avatar's art style.
3. The presenter MUST look NATURAL in the environment:
   - Correct lighting direction matching the room's light source
   - Realistic scale (waist-up or chest-up framing)
   - Natural shadows on and from the presenter
   - Art style consistency between avatar and background
4. Do NOT leave ANY transparent, solid-color, or gradient background
5. Do NOT make the presenter look oversized relative to the environment
6. The background rendering style should be INDISTINGUISHABLE from the avatar's
   own rendering style — same medium, same level of detail, same color treatment.
The result should look like the presenter belongs in that environment.
```

Replace `{FILL_DIRECTIVE}` with the directive from Step 2.5 matching the detected `avatar_visual_style`.

## Correction Stacking Matrix

Corrections can stack. A portrait photo_avatar in a landscape video gets BOTH A and C.

| avatar_type | Orientation Match? | Has Background? | Corrections |
|---|---|---|---|
| avatar_type | Orientation | Aspect Ratio | Has Background? | Corrections |
|---|---|---|---|---|
| `video_avatar` | ✅ same | ✅ ~16:9 | ✅ Yes | None |
| `video_avatar` | ✅ same | ❌ not 16:9 | ✅ Yes | Ratio fix (F or G) |
| `video_avatar` | ❌ different | any | ✅ Yes | Framing (A or B) |
| `video_avatar` | ◻ square | n/a | ✅ Yes | Framing (D or E) |
| `studio_avatar` | ✅ same | ✅ ~16:9 | ✅ Yes | None |
| `studio_avatar` | ✅ same | ✅ ~16:9 | ❌ No | Background (C) |
| `studio_avatar` | ✅ same | ❌ not 16:9 | ✅ Yes | Ratio fix (F or G) |
| `studio_avatar` | ✅ same | ❌ not 16:9 | ❌ No | Ratio fix (F or G) + Background (C) |
| `studio_avatar` | ❌ different | any | ✅ Yes | Framing (A or B) |
| `studio_avatar` | ❌ different | any | ❌ No | Framing (A or B) + Background (C) |
| `studio_avatar` | ◻ square | n/a | ✅ Yes | Framing (D or E) |
| `studio_avatar` | ◻ square | n/a | ❌ No | Framing (D or E) + Background (C) |
| `photo_avatar` | ✅ same | ✅ ~16:9 | (n/a) | **None** |
| `photo_avatar` | ✅ same | ❌ not 16:9 | (n/a) | **Ratio fix (F or G)** |
| `photo_avatar` | ❌ different | any | (n/a) | **Framing (A or B)** |
| `photo_avatar` | ◻ square | n/a | (n/a) | **Framing (D or E)** |

**How to check if studio_avatar has a background:** Fetch `preview_image_url`. If transparent/checkered, solid color, or cutout → "No background" → inject C.

**photo_avatar rule:** Video Agent generates the avatar and its environment together during video creation. Do NOT inject Correction C for photo_avatars. Only inject framing corrections (A or B) if there's an orientation mismatch.

## Step 5: Submit with original avatar_id

After building correction blocks, append them to the Video Agent prompt text. Then submit the video request using the **original `avatar_id`** (unchanged). Video Agent's internal AI Image tool will handle the framing and background corrections based on the FRAMING NOTE and BACKGROUND NOTE directives in the prompt.

**Do NOT:**
- Generate corrected images externally (destroys face identity)
- Upload new assets for framing corrections
- Create new avatar looks for orientation variants

Video Agent's AI Image tool preserves the avatar's face identity while adjusting framing. External image generation tools cannot do this reliably.

## Step 6: Log the correction

Add to learning log entry:
- `"aspect_correction"`: `"portrait_to_landscape"` | `"landscape_to_portrait"` | `"square_to_landscape"` | `"square_to_portrait"` | `"ratio_fix_portrait"` | `"ratio_fix_landscape"` | `"background_fill"` | `"both"` | `"none"`
- `"avatar_type"`: the raw value from the API
- `"avatar_visual_style"`: `"photorealistic"` | `"animated"` | `"3d_rendered"` | `"stylized"` | `"unknown"`
