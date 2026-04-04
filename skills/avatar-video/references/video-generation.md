---
name: video-generation
description: POST /v3/videos workflow for creating AI avatar videos with HeyGen
---

# Video Generation

## Table of Contents
- [Basic Video Generation](#basic-video-generation)
- [Request Fields](#request-fields)
- [Type: Avatar](#type-avatar)
- [Type: Image](#type-image)
- [Voice Input Modes](#voice-input-modes)
- [Voice Settings](#voice-settings)
- [Motion and Expressiveness](#motion-and-expressiveness)
- [Background Options](#background-options)
- [Resolution and Aspect Ratio](#resolution-and-aspect-ratio)
- [Complete Workflow Example](#complete-workflow-example)
- [Error Handling](#error-handling)
- [Script Length Limits](#script-length-limits)
- [Adding Pauses to Scripts](#adding-pauses-to-scripts)
- [Transparent Background](#transparent-background)
- [Production-Ready Workflow](#production-ready-workflow)
- [Best Practices](#best-practices)

---

The `POST /v3/videos` endpoint creates AI avatar videos with HeyGen. The request body is a **discriminated union** on the `type` field with two variants:

- **`type: "avatar"`** -- Use a HeyGen avatar (video or photo avatar) by its look ID.
- **`type: "image"`** -- Animate an arbitrary image (via URL, asset ID, or base64). Uses Avatar IV automatically.

Each request produces a single video with one avatar/image and one voice input. For multi-scene workflows, create multiple videos and stitch them together in post-production.

## Basic Video Generation

### From a HeyGen avatar (`type: "avatar"`)

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "Hello! Welcome to HeyGen.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "resolution": "1080p",
    "aspect_ratio": "16:9"
  }'
```

### From an arbitrary image (`type: "image"`)

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "image": {
      "type": "url",
      "url": "https://example.com/my-photo.jpg"
    },
    "script": "Hello from a custom image!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "resolution": "1080p",
    "aspect_ratio": "16:9"
  }'
```

### Response (same for both)

```json
{
  "data": {
    "video_id": "abc123",
    "status": "waiting"
  }
}
```

### TypeScript

```typescript
// Discriminated union: the `type` field determines which variant is used.

interface AssetInputUrl {
  type: "url";
  url: string;
}

interface AssetInputAssetId {
  type: "asset_id";
  asset_id: string;
}

interface AssetInputBase64 {
  type: "base64";
  media_type: string;  // e.g. "image/png"
  data: string;
}

type AssetInput = AssetInputUrl | AssetInputAssetId | AssetInputBase64;

interface SharedVideoFields {
  // Voice source (mutually exclusive groups)
  script?: string;          // Text script -- requires voice_id
  voice_id?: string;        // Voice ID for TTS -- required with script
  audio_url?: string;       // Public URL of audio to lip-sync
  audio_asset_id?: string;  // HeyGen asset ID of uploaded audio

  // Display
  title?: string;
  resolution?: "1080p" | "720p";
  aspect_ratio?: "16:9" | "9:16";

  // Avatar behavior (photo avatars / image mode)
  motion_prompt?: string;
  expressiveness?: "high" | "medium" | "low";

  // Background
  remove_background?: boolean;
  background?: {
    type: "color" | "image";
    value?: string;     // Hex color (when type is "color")
    url?: string;       // Image URL (when type is "image")
    asset_id?: string;  // HeyGen asset ID (when type is "image")
  };

  // Voice tuning
  voice_settings?: {
    speed?: number;   // 0.5 - 1.5
    pitch?: number;   // -50 to 50
    locale?: string;  // e.g. "en-US"
  };

  // Callbacks
  callback_url?: string;
  callback_id?: string;
}

interface CreateVideoFromAvatar extends SharedVideoFields {
  type: "avatar";
  avatar_id: string;       // Required: HeyGen avatar look ID
}

interface CreateVideoFromImage extends SharedVideoFields {
  type: "image";
  image: AssetInput;       // Required: image source (url, asset_id, or base64)
}

type CreateVideoRequest = CreateVideoFromAvatar | CreateVideoFromImage;

interface CreateVideoResponse {
  data: {
    video_id: string;
    status: string; // e.g. "waiting"
  };
}

interface VideoErrorResponse {
  error: {
    code: string;
    message: string;
  };
}

async function generateVideo(config: CreateVideoRequest): Promise<string> {
  const response = await fetch("https://api.heygen.com/v3/videos", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  const json = await response.json();

  if (!response.ok) {
    const err = json as VideoErrorResponse;
    throw new Error(`${err.error.code}: ${err.error.message}`);
  }

  const result = json as CreateVideoResponse;
  return result.data.video_id;
}
```

### Python

```python
import requests
import os

def generate_video(config: dict) -> str:
    response = requests.post(
        "https://api.heygen.com/v3/videos",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=config,
    )

    data = response.json()
    if not response.ok:
        err = data["error"]
        raise Exception(f"{err['code']}: {err['message']}")

    return data["data"]["video_id"]
```

## Request Fields

The v3 API uses a **discriminated union** on the `type` field. The `type` determines which variant-specific fields are required, while audio, display, and output fields are shared across both variants.

### Discriminator

| Field | Type | Description |
|-------|------|-------------|
| `type` | `"avatar"` \| `"image"` | **Required.** Selects the creation mode. |

### Type-specific Fields

| Field | Applies to | Type | Description |
|-------|-----------|------|-------------|
| `avatar_id` | `type: "avatar"` | string | **Required.** HeyGen avatar look ID. |
| `image` | `type: "image"` | AssetInput | **Required.** Image source as a discriminated union (see [Type: Image](#type-image)). |

### Shared Audio Fields (mutually exclusive groups)

Provide exactly one audio source: `script` + `voice_id`, or `audio_url`, or `audio_asset_id`.

| Field | Type | Description |
|-------|------|-------------|
| `script` | string \| null | Text script for the avatar to speak. Requires `voice_id`. |
| `voice_id` | string \| null | Voice ID for TTS. Required when `script` is provided. |
| `audio_url` | string \| null | Public URL of audio file to lip-sync. Mutually exclusive with `script`. |
| `audio_asset_id` | string \| null | HeyGen asset ID of uploaded audio. Mutually exclusive with `script`. |

### Shared Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string \| null | Display title in HeyGen dashboard. |
| `resolution` | `"1080p"` \| `"720p"` \| null | Output resolution. |
| `aspect_ratio` | `"16:9"` \| `"9:16"` \| null | Output aspect ratio. |
| `motion_prompt` | string \| null | Natural-language prompt controlling body motion. Photo avatars and image mode. |
| `expressiveness` | `"high"` \| `"medium"` \| `"low"` \| null | Expression intensity. Photo avatars and image mode. Defaults to `"low"`. |
| `remove_background` | boolean \| null | Remove the avatar background. |
| `background` | object \| null | Background config (see [Background Options](#background-options)). |
| `voice_settings` | object \| null | Voice tuning (see [Voice Settings](#voice-settings)). |
| `callback_url` | string \| null | URL for completion webhook notification. |
| `callback_id` | string \| null | Custom ID included in webhook payload. |

## Type: Avatar

Use `type: "avatar"` to create a video from a HeyGen avatar (video or photo avatar) by its look ID. The `avatar_id` field is required.

### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "Hello from a HeyGen avatar!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8"
  }'
```

### TypeScript

```typescript
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "Hello from a HeyGen avatar!",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
});
```

### Python

```python
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "Hello from a HeyGen avatar!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
})
```

## Type: Image

Use `type: "image"` to animate an arbitrary image. The `image` field is required and is itself a discriminated union (`AssetInput`) with three variants:

| Variant | Fields | Description |
|---------|--------|-------------|
| `type: "url"` | `url` (string, required) | Public URL of the image. |
| `type: "asset_id"` | `asset_id` (string, required) | HeyGen asset ID from a previous upload. |
| `type: "base64"` | `media_type` (string, required), `data` (string, required) | Inline base64-encoded image. |

### 1. Image from URL

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "image": {
      "type": "url",
      "url": "https://example.com/my-photo.jpg"
    },
    "script": "Hello from a custom image!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8"
  }'
```

#### TypeScript

```typescript
const videoId = await generateVideo({
  type: "image",
  image: {
    type: "url",
    url: "https://example.com/my-photo.jpg",
  },
  script: "Hello from a custom image!",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
});
```

#### Python

```python
video_id = generate_video({
    "type": "image",
    "image": {
        "type": "url",
        "url": "https://example.com/my-photo.jpg",
    },
    "script": "Hello from a custom image!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
})
```

### 2. Image from Asset ID

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "image": {
      "type": "asset_id",
      "asset_id": "asset_abc123"
    },
    "script": "Hello from an uploaded image!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8"
  }'
```

#### TypeScript

```typescript
const videoId = await generateVideo({
  type: "image",
  image: {
    type: "asset_id",
    asset_id: "asset_abc123",
  },
  script: "Hello from an uploaded image!",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
});
```

#### Python

```python
video_id = generate_video({
    "type": "image",
    "image": {
        "type": "asset_id",
        "asset_id": "asset_abc123",
    },
    "script": "Hello from an uploaded image!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
})
```

### 3. Image from Base64

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "image": {
      "type": "base64",
      "media_type": "image/png",
      "data": "iVBORw0KGgoAAAANSUhEUgAA..."
    },
    "script": "Hello from a base64 image!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8"
  }'
```

#### TypeScript

```typescript
import { readFileSync } from "fs";

const imageData = readFileSync("photo.png").toString("base64");

const videoId = await generateVideo({
  type: "image",
  image: {
    type: "base64",
    media_type: "image/png",
    data: imageData,
  },
  script: "Hello from a base64 image!",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
});
```

#### Python

```python
import base64

with open("photo.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

video_id = generate_video({
    "type": "image",
    "image": {
        "type": "base64",
        "media_type": "image/png",
        "data": image_data,
    },
    "script": "Hello from a base64 image!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
})
```

## Voice Input Modes

There are three mutually exclusive ways to provide voice input. These work the same for both `type: "avatar"` and `type: "image"`.

### 1. Text-to-Speech (`script` + `voice_id`)

Provide a text script and a voice ID. HeyGen generates speech and lip-syncs the avatar.

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "This is text-to-speech with a chosen voice.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "voice_settings": {
      "speed": 1.1,
      "pitch": 5
    }
  }'
```

#### TypeScript

```typescript
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "This is text-to-speech with a chosen voice.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  voice_settings: {
    speed: 1.1,
    pitch: 5,
  },
});
```

#### Python

```python
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "This is text-to-speech with a chosen voice.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "voice_settings": {
        "speed": 1.1,
        "pitch": 5,
    },
})
```

### 2. Custom Audio (`audio_url`)

Provide a pre-recorded audio file by URL. The avatar lip-syncs to it. Do not provide `script` or `voice_id` when using audio input.

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "audio_url": "https://example.com/narration.mp3"
  }'
```

#### TypeScript

```typescript
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  audio_url: "https://example.com/narration.mp3",
});
```

#### Python

```python
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "audio_url": "https://example.com/narration.mp3",
})
```

### 3. Uploaded Audio Asset (`audio_asset_id`)

Use an audio file previously uploaded to HeyGen's asset system.

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "audio_asset_id": "asset_audio_456"
  }'
```

#### TypeScript

```typescript
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  audio_asset_id: "asset_audio_456",
});
```

#### Python

```python
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "audio_asset_id": "asset_audio_456",
})
```

## Voice Settings

Fine-tune TTS output with `voice_settings`. Only applicable when using `script` + `voice_id`.

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `speed` | number | 0.5 - 1.5 | Speech speed multiplier. Default 1.0. |
| `pitch` | number | -50 to 50 | Voice pitch adjustment. Default 0. |
| `locale` | string | | Language locale hint (e.g. `"en-US"`, `"es-ES"`). |

### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "This has custom voice settings.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "voice_settings": {
      "speed": 0.9,
      "pitch": -10,
      "locale": "en-US"
    }
  }'
```

### TypeScript

```typescript
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "This has custom voice settings.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  voice_settings: {
    speed: 0.9,
    pitch: -10,
    locale: "en-US",
  },
});
```

### Python

```python
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "This has custom voice settings.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "voice_settings": {
        "speed": 0.9,
        "pitch": -10,
        "locale": "en-US",
    },
})
```

## Motion and Expressiveness

Control avatar body motion and facial expressiveness. These work with **photo avatars** (`type: "avatar"`) and **image mode** (`type: "image"`).

| Field | Type | Description |
|-------|------|-------------|
| `motion_prompt` | string | Natural-language description of desired body motion (e.g. `"lean forward enthusiastically"`, `"nod while speaking"`). |
| `expressiveness` | `"high"` \| `"medium"` \| `"low"` | Facial expression intensity. Defaults to `"low"`. |

### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "I am really excited to show you this feature!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "motion_prompt": "lean forward with enthusiasm, use hand gestures",
    "expressiveness": "high"
  }'
```

### TypeScript

```typescript
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "I am really excited to show you this feature!",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  motion_prompt: "lean forward with enthusiasm, use hand gestures",
  expressiveness: "high",
});
```

### Python

```python
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "I am really excited to show you this feature!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "motion_prompt": "lean forward with enthusiasm, use hand gestures",
    "expressiveness": "high",
})
```

## Background Options

Set a custom background with the `background` field.

| Field | Type | Description |
|-------|------|-------------|
| `type` | `"color"` \| `"image"` | Background type. |
| `value` | string | Hex color code (when type is `"color"`). |
| `url` | string | Public image URL (when type is `"image"`). |
| `asset_id` | string | HeyGen asset ID of uploaded image (when type is `"image"`). |

### Solid Color Background

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "White background video.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "background": {
      "type": "color",
      "value": "#FFFFFF"
    }
  }'
```

#### TypeScript

```typescript
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "White background video.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  background: {
    type: "color",
    value: "#FFFFFF",
  },
});
```

#### Python

```python
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "White background video.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "background": {
        "type": "color",
        "value": "#FFFFFF",
    },
})
```

### Image Background

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "Custom image background.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "background": {
      "type": "image",
      "url": "https://example.com/office-bg.jpg"
    }
  }'
```

#### TypeScript

```typescript
// Using a public URL
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "Custom image background.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  background: {
    type: "image",
    url: "https://example.com/office-bg.jpg",
  },
});

// Using a HeyGen asset
const videoId2 = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "Background from uploaded asset.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  background: {
    type: "image",
    asset_id: "asset_bg_789",
  },
});
```

#### Python

```python
# Using a public URL
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "Custom image background.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "background": {
        "type": "image",
        "url": "https://example.com/office-bg.jpg",
    },
})

# Using a HeyGen asset
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "Background from uploaded asset.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "background": {
        "type": "image",
        "asset_id": "asset_bg_789",
    },
})
```

## Resolution and Aspect Ratio

| Field | Values | Description |
|-------|--------|-------------|
| `resolution` | `"1080p"`, `"720p"` | Output resolution. Defaults to `"1080p"`. |
| `aspect_ratio` | `"16:9"`, `"9:16"` | Output aspect ratio. `"16:9"` for landscape, `"9:16"` for portrait/mobile. |

### curl

```bash
# Portrait/mobile video
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "This is a portrait video for mobile.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "resolution": "1080p",
    "aspect_ratio": "9:16"
  }'
```

### TypeScript

```typescript
// Portrait/mobile video
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "This is a portrait video for mobile.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  resolution: "1080p",
  aspect_ratio: "9:16",
});
```

### Python

```python
# Portrait/mobile video
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "This is a portrait video for mobile.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "resolution": "1080p",
    "aspect_ratio": "9:16",
})
```

## Complete Workflow Example

### TypeScript

```typescript
async function createVideo(
  script: string,
  avatarId: string,
  voiceId: string
): Promise<string> {
  // 1. Generate video
  console.log("Starting video generation...");
  const videoId = await generateVideo({
    type: "avatar",
    avatar_id: avatarId,
    script: script,
    voice_id: voiceId,
    resolution: "1080p",
    aspect_ratio: "16:9",
    background: {
      type: "color",
      value: "#FFFFFF",
    },
  });

  console.log(`Video ID: ${videoId}`);

  // 2. Poll for completion
  console.log("Waiting for video completion...");
  const videoUrl = await waitForVideo(videoId);

  console.log(`Video ready: ${videoUrl}`);
  return videoUrl;
}

// Helper function for polling
async function waitForVideo(videoId: string): Promise<string> {
  const maxAttempts = 60;
  const pollInterval = 10000; // 10 seconds

  for (let i = 0; i < maxAttempts; i++) {
    const response = await fetch(
      `https://api.heygen.com/v3/videos/${videoId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );

    const json = await response.json();

    if (!response.ok) {
      const err = json as VideoErrorResponse;
      throw new Error(`${err.error.code}: ${err.error.message}`);
    }

    const { data } = json;

    if (data.status === "completed") {
      return data.video_url;
    } else if (data.status === "failed") {
      throw new Error(data.failure_message || "Video generation failed");
    }

    await new Promise((r) => setTimeout(r, pollInterval));
  }

  throw new Error("Video generation timed out");
}
```

### Python

```python
import time

def create_video(script: str, avatar_id: str, voice_id: str) -> str:
    # 1. Generate video
    print("Starting video generation...")
    video_id = generate_video({
        "type": "avatar",
        "avatar_id": avatar_id,
        "script": script,
        "voice_id": voice_id,
        "resolution": "1080p",
        "aspect_ratio": "16:9",
        "background": {
            "type": "color",
            "value": "#FFFFFF",
        },
    })

    print(f"Video ID: {video_id}")

    # 2. Poll for completion
    print("Waiting for video completion...")
    video_url = wait_for_video(video_id)

    print(f"Video ready: {video_url}")
    return video_url


def wait_for_video(video_id: str, max_attempts: int = 60, poll_interval: int = 10) -> str:
    for _ in range(max_attempts):
        response = requests.get(
            f"https://api.heygen.com/v3/videos/{video_id}",
            headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        )

        data = response.json()
        if not response.ok:
            err = data["error"]
            raise Exception(f"{err['code']}: {err['message']}")

        status = data["data"]["status"]

        if status == "completed":
            return data["data"]["video_url"]
        elif status == "failed":
            raise Exception(data["data"].get("failure_message", "Video generation failed"))

        time.sleep(poll_interval)

    raise Exception("Video generation timed out")
```

## Error Handling

The v3 API returns errors in a structured format:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "avatar_id is required when type is avatar"
  }
}
```

### TypeScript

```typescript
async function generateVideoSafe(config: CreateVideoRequest) {
  try {
    const videoId = await generateVideo(config);
    return { success: true, videoId };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);

    // Common error patterns
    if (message.includes("quota") || message.includes("credit")) {
      console.error("Insufficient credits");
    } else if (message.includes("avatar")) {
      console.error("Invalid avatar ID");
    } else if (message.includes("voice")) {
      console.error("Invalid voice ID");
    } else if (message.includes("image")) {
      console.error("Invalid image input");
    } else if (message.includes("script")) {
      console.error("Script too long or invalid");
    }

    return { success: false, error: message };
  }
}
```

### Python

```python
def generate_video_safe(config: dict) -> dict:
    try:
        video_id = generate_video(config)
        return {"success": True, "video_id": video_id}
    except Exception as e:
        message = str(e)

        if "quota" in message or "credit" in message:
            print("Insufficient credits")
        elif "avatar" in message:
            print("Invalid avatar ID")
        elif "voice" in message:
            print("Invalid voice ID")
        elif "image" in message:
            print("Invalid image input")
        elif "script" in message:
            print("Script too long or invalid")

        return {"success": False, "error": message}
```

## Script Length Limits

| Tier | Max Characters |
|------|----------------|
| Free | ~500 |
| Creator | ~1,500 |
| Team | ~3,000 |
| Enterprise | ~5,000+ |

## Adding Pauses to Scripts

Use `<break>` tags to add pauses in your script:

```typescript
const script = 'Welcome to our demo. <break time="1s"/> Let me show you the features.';
```

**Format:** `<break time="Xs"/>` where X is seconds (e.g., `1s`, `1.5s`, `0.5s`)

**Important:** Break tags must have spaces before and after them.

See [voices.md](voices.md) for detailed break tag documentation.

## Transparent Background

Use `remove_background: true` to generate a video with the avatar's background removed. This is useful when you want to overlay the avatar on other content in post-production.

### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "This video has the background removed.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "remove_background": true
  }'
```

### TypeScript

```typescript
const videoId = await generateVideo({
  type: "avatar",
  avatar_id: "josh_lite3_20230714",
  script: "This video has the background removed.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  remove_background: true,
});
```

### Python

```python
video_id = generate_video({
    "type": "avatar",
    "avatar_id": "josh_lite3_20230714",
    "script": "This video has the background removed.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "remove_background": True,
})
```

**When to use `remove_background`:**
- Avatar overlaid on screen recordings (Loom-style)
- Avatar floating over video or image content
- True alpha-channel compositing in post-production

**When you do NOT need `remove_background`:**
- Avatar with overlays/text on top of the avatar
- Standard presenter videos with a solid or image background

## Production-Ready Workflow

Complete example using the avatar's default voice (recommended), proper timeouts, and retry logic.

### TypeScript

```typescript
interface VideoGenerationResult {
  videoId: string;
  videoUrl: string;
  duration: number;
  avatarId: string;
  voiceId: string;
  avatarName: string;
}

async function generateAvatarVideo(
  script: string,
  options: {
    avatarId?: string; // Specific avatar, or will pick first available
    resolution?: "1080p" | "720p";
    aspectRatio?: "16:9" | "9:16";
  } = {}
): Promise<VideoGenerationResult> {
  const { resolution = "1080p", aspectRatio = "16:9" } = options;
  let { avatarId } = options;

  // 1. List avatar looks if no specific one provided
  if (!avatarId) {
    console.log("Listing available avatar looks...");
    const listResponse = await fetch("https://api.heygen.com/v3/avatars/looks", {
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    });

    if (!listResponse.ok) {
      const err = await listResponse.json();
      throw new Error(`${err.error.code}: ${err.error.message}`);
    }

    const listData = await listResponse.json();

    if (!listData.data?.length) {
      throw new Error("No avatar looks available");
    }
    avatarId = listData.data[0].id;
  }

  // 2. Get avatar look details including default voice
  console.log(`Getting details for avatar look: ${avatarId}`);
  const detailsResponse = await fetch(
    `https://api.heygen.com/v3/avatars/looks/${avatarId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  if (!detailsResponse.ok) {
    const err = await detailsResponse.json();
    throw new Error(`${err.error.code}: ${err.error.message}`);
  }

  const { data: avatar } = await detailsResponse.json();

  if (!avatar.default_voice_id) {
    throw new Error(
      `Avatar ${avatar.name} has no default voice - select a voice manually`
    );
  }

  console.log(
    `Using avatar: ${avatar.name} with default voice: ${avatar.default_voice_id}`
  );

  // 3. Generate video
  const videoId = await generateVideo({
    type: "avatar",
    avatar_id: avatarId,
    script: script,
    voice_id: avatar.default_voice_id,
    resolution: resolution,
    aspect_ratio: aspectRatio,
    background: {
      type: "color",
      value: "#1a1a2e",
    },
  });

  console.log(`Video ID: ${videoId}`);

  // 4. Wait for completion (20 minute timeout - generation can take 15+ min)
  console.log("Waiting for video generation (typically 5-15 minutes)...");
  const maxAttempts = 120; // 120 * 10s = 20 minutes
  const pollInterval = 10000;

  for (let i = 0; i < maxAttempts; i++) {
    const response = await fetch(
      `https://api.heygen.com/v3/videos/${videoId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );

    const json = await response.json();

    if (!response.ok) {
      const err = json as VideoErrorResponse;
      throw new Error(`${err.error.code}: ${err.error.message}`);
    }

    const { data } = json;

    console.log(`  [${Math.round((i * pollInterval) / 1000)}s] ${data.status}`);

    if (data.status === "completed") {
      return {
        videoId,
        videoUrl: data.video_url,
        duration: data.duration,
        avatarId: avatarId!,
        voiceId: avatar.default_voice_id,
        avatarName: avatar.name,
      };
    } else if (data.status === "failed") {
      throw new Error(data.failure_message || "Video generation failed");
    }

    await new Promise((r) => setTimeout(r, pollInterval));
  }

  throw new Error("Video generation timed out after 20 minutes");
}

// Usage - let it pick an avatar automatically
const result = await generateAvatarVideo(
  "Hello! Welcome to our product demonstration."
);
console.log(`Video ready: ${result.videoUrl}`);

// Or specify a known avatar look ID
const result2 = await generateAvatarVideo(
  "Hello! Welcome to our product demonstration.",
  { avatarId: "josh_lite3_20230714", aspectRatio: "9:16" }
);
```

### Python

```python
def generate_avatar_video(
    script: str,
    avatar_id: str | None = None,
    resolution: str = "1080p",
    aspect_ratio: str = "16:9",
) -> dict:
    headers = {"X-Api-Key": os.environ["HEYGEN_API_KEY"]}

    # 1. List avatar looks if no specific one provided
    if not avatar_id:
        print("Listing available avatar looks...")
        list_resp = requests.get(
            "https://api.heygen.com/v3/avatars/looks",
            headers=headers,
        )
        list_data = list_resp.json()
        if not list_resp.ok:
            err = list_data["error"]
            raise Exception(f"{err['code']}: {err['message']}")

        if not list_data.get("data"):
            raise Exception("No avatar looks available")
        avatar_id = list_data["data"][0]["id"]

    # 2. Get avatar look details
    print(f"Getting details for avatar look: {avatar_id}")
    details_resp = requests.get(
        f"https://api.heygen.com/v3/avatars/looks/{avatar_id}",
        headers=headers,
    )
    details_data = details_resp.json()
    if not details_resp.ok:
        err = details_data["error"]
        raise Exception(f"{err['code']}: {err['message']}")

    avatar = details_data["data"]

    if not avatar.get("default_voice_id"):
        raise Exception(f"Avatar {avatar['name']} has no default voice")

    voice_id = avatar["default_voice_id"]
    print(f"Using avatar: {avatar['name']} with default voice: {voice_id}")

    # 3. Generate video
    video_id = generate_video({
        "type": "avatar",
        "avatar_id": avatar_id,
        "script": script,
        "voice_id": voice_id,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "background": {
            "type": "color",
            "value": "#1a1a2e",
        },
    })

    print(f"Video ID: {video_id}")

    # 4. Wait for completion (20 minute timeout)
    print("Waiting for video generation (typically 5-15 minutes)...")
    max_attempts = 120
    poll_interval = 10

    for i in range(max_attempts):
        resp = requests.get(
            f"https://api.heygen.com/v3/videos/{video_id}",
            headers=headers,
        )
        data = resp.json()
        if not resp.ok:
            err = data["error"]
            raise Exception(f"{err['code']}: {err['message']}")

        status = data["data"]["status"]
        print(f"  [{i * poll_interval}s] {status}")

        if status == "completed":
            return {
                "video_id": video_id,
                "video_url": data["data"]["video_url"],
                "duration": data["data"]["duration"],
                "avatar_id": avatar_id,
                "voice_id": voice_id,
                "avatar_name": avatar["name"],
            }
        elif status == "failed":
            raise Exception(
                data["data"].get("failure_message", "Video generation failed")
            )

        time.sleep(poll_interval)

    raise Exception("Video generation timed out after 20 minutes")


# Usage
result = generate_avatar_video("Hello! Welcome to our product demonstration.")
print(f"Video ready: {result['video_url']}")
```

## Multi-Scene Note

The v3 API creates **one video per request** (single scene). For multi-scene workflows, generate multiple videos and concatenate them in post-production using tools like ffmpeg, Remotion, or a video editor.

## Best Practices

1. **Preview avatars before generating** - Download `preview_image_url` so the user can see what the avatar looks like before committing to a video (see [avatars.md](avatars.md))
2. **Use the avatar's default voice** - Most avatars have a `default_voice_id` that is pre-matched for natural results (see [avatars.md](avatars.md))
3. **Fallback: match gender manually** - If no default voice, ensure avatar and voice genders match (see [voices.md](voices.md))
4. **Validate inputs** - Check avatar and voice IDs before generating
5. **Set generous timeouts** - Use 15-20 minutes; generation often takes 10-15 min, sometimes longer
6. **Consider async patterns** - For long videos, save `video_id` and check status later (see [video-status.md](video-status.md))
7. **Handle errors gracefully** - Check `response.ok` and parse the structured `error` object
8. **Monitor progress** - Implement polling with progress feedback
9. **Optimize scripts** - Keep scripts concise and natural
10. **Match resolution to use case** - Use `"9:16"` for mobile/social, `"16:9"` for presentations and web
