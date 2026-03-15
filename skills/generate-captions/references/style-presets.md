# Style Presets

## classic

Standard subtitles at the bottom. White text with black outline, orange highlight on the active word.

| Property | Value |
|----------|-------|
| Font | Arial, 48pt |
| Primary (text) | `#FFFFFF` (white) |
| Secondary (highlight) | `#FFA500` (orange) |
| Outline | `#000000`, 3px |
| Shadow | 0 |
| Background | none |
| Position | bottom |
| Animation | karaoke-sweep |
| Words/line | 6 |

## pop

TikTok / Reels style. Centered, mint highlight, outline + drop shadow.

| Property | Value |
|----------|-------|
| Font | Arial Black, 60pt |
| Primary (text) | `#FFFFFF` (white) |
| Secondary (highlight) | `#00FFB2` (mint) |
| Outline | `#000000`, 3px |
| Shadow | 2px |
| Background | none |
| Position | center |
| Animation | karaoke-sweep |
| Words/line | 4 |

## bold

Large, high-impact captions with gold highlight.

| Property | Value |
|----------|-------|
| Font | Arial Black, 72pt |
| Primary (text) | `#FFFFFF` (white) |
| Secondary (highlight) | `#FFD700` (gold) |
| Outline | `#000000`, 4px |
| Shadow | 3px |
| Background | none |
| Position | center |
| Animation | karaoke-sweep |
| Words/line | 3 |

## boxed

White text on a semi-transparent black box. Cyan highlight. Clean, readable over any background.

| Property | Value |
|----------|-------|
| Font | Arial, 52pt |
| Primary (text) | `#FFFFFF` (white) |
| Secondary (highlight) | `#00E5FF` (cyan) |
| Outline | `#000000`, 0px |
| Shadow | 0 |
| Background | `#000000` (semi-transparent) |
| Position | center |
| Animation | karaoke-sweep |
| Words/line | 5 |

The boxed preset generates a two-layer ASS file: a `DefaultBG` style (BorderStyle=3, opaque box) on layer 0, and the `Default` text style on layer 1.

## single

One word at a time, centered. Purple highlight with outline + shadow.

| Property | Value |
|----------|-------|
| Font | Arial Black, 64pt |
| Primary (text) | `#FFFFFF` (white) |
| Secondary (highlight) | `#AA44FF` (purple) |
| Outline | `#000000`, 3px |
| Shadow | 2px |
| Background | none |
| Position | center |
| Animation | karaoke-sweep |
| Words/line | 1 (single_words=true) |

## Animation Types

### none
Words appear as plain text. No word-level highlighting. Primary color used for all text.

### karaoke
Words are highlighted instantly as spoken. Uses ASS `\k` tag. The secondary color fills each word at the moment it starts.

### karaoke-sweep
Words are highlighted with a smooth left-to-right sweep. Uses ASS `\kf` tag. The secondary color sweeps across each word over its duration.

## Color Semantics

- **primary_color** — base text color (what you see most of the time)
- **secondary_color** — highlight / active word color (the karaoke sweep fills with this)

Colors are specified as `#RRGGBB` hex strings. Internally converted to ASS BGR format (`&HAABBGGRR`).

## Ad-Hoc Boxed Mode

Any preset can be given a background box by passing `--background-color`:

```bash
python3 caption_video.py video.mp4 --json captions.json --style classic --background-color "#000000"
```

This adds the `DefaultBG` layer to the ASS output regardless of the base preset.

## Position Values

| Value | ASS Alignment | Description |
|-------|--------------|-------------|
| bottom | 2 | Bottom center (standard subtitle position) |
| center | 5 | Middle center (social media style) |
| top | 8 | Top center |

## Portrait Video

For portrait/vertical videos (height > width), margins are automatically increased (80px vertical, 60px horizontal) to keep captions clear of safe zones.
