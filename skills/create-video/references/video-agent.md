---
name: video-agent
description: One-shot prompt video generation with HeyGen Video Agent API
---

# Video Agent API

The Video Agent API generates complete videos from a single text prompt. Unlike the standard video generation API which requires detailed scene-by-scene configuration, Video Agent automatically handles script writing, avatar selection, visuals, voiceover, pacing, and captions.

## MCP Tool (Preferred)

If the HeyGen MCP server is connected, use `mcp__heygen__create_video_agent` instead of direct API calls:

```
Tool: mcp__heygen__create_video_agent
Parameters:
  prompt: "<optimized prompt from prompt-optimizer.md>"
  avatar_id: "avatar_id"       # optional, agent selects if omitted
  voice_id: "voice_id"         # optional, agent selects if omitted
  orientation: "landscape"     # optional, "landscape" or "portrait"
  files:                       # optional, type-discriminated union
    - type: "asset_id"
      asset_id: "uploaded_asset_id"
```

Then check status with `mcp__heygen__get_video` using the returned `video_id`.

The prompt quality is still the critical factor — always follow [prompt-optimizer.md](prompt-optimizer.md) regardless of whether you use MCP or direct API.

## When to Use Video Agent vs Standard API

| Use Case | Recommended API |
|----------|-----------------|
| Quick video from idea | Video Agent |
| Precise control over scenes, avatars, timing | Standard POST /v3/videos |
| Automated content generation at scale | Video Agent |
| Specific avatar with exact script | Standard POST /v3/videos |
| Prototype or draft video | Video Agent |
| Brand-consistent production video | Standard POST /v3/videos |

## Before You Call This API

**Required step:** Optimize your prompt using [prompt-optimizer.md](prompt-optimizer.md) before generating a video. The difference between mediocre and professional results depends entirely on prompt quality.

Quick checklist:
1. Define visual style (colors, aesthetic) — see [visual-styles.md](visual-styles.md)
2. Structure scenes with specific scene types
3. Write VO script at ~150 words/minute
4. Specify media types for each scene (Motion Graphics, Stock, AI-generated)

## Direct API Endpoint

```
POST https://api.heygen.com/v3/video-agents
```

## Request Fields

All fields are top-level (no nested `config` object).

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `prompt` | string | ✓ | Text prompt describing the video you want (1-10000 chars) |
| `avatar_id` | string \| null | | Specific avatar to use (agent selects if omitted) |
| `voice_id` | string \| null | | Specific voice for narration (agent selects if omitted) |
| `orientation` | string \| null | | `"landscape"` or `"portrait"` |
| `files` | array \| null | | Asset files to reference in generation (max 20, see below) |
| `callback_url` | string \| null | | Webhook URL for completion notification |
| `callback_id` | string \| null | | Custom ID for tracking. **Requires `callback_url` to also be set** — omit both if you don't need webhooks |

### Files Array

Each file entry is a type-discriminated union. You must include the `type` field to indicate the format.

| Variant | Fields | Description |
|---------|--------|-------------|
| `AssetUrl` | `{ type: "url", url: string }` | Public URL to a file |
| `AssetId` | `{ type: "asset_id", asset_id: string }` | Asset ID of a previously uploaded file |
| `AssetBase64` | `{ type: "base64", media_type: string, data: string }` | Inline base64-encoded file |

## Response Format

```json
{
  "data": {
    "session_id": "sess_012abc345def678",
    "status": "generating",
    "video_id": "v_abc123def456",
    "created_at": 1711929600
  }
}
```

**Error format:**

```json
{
  "error": {
    "code": "invalid_request",
    "message": "prompt is required"
  }
}
```

## curl Example

```bash
curl -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 60-second product demo video for a new AI-powered calendar app. The tone should be professional but friendly, targeting busy professionals. Highlight the smart scheduling feature and time zone handling."
  }'
```

## TypeScript

```typescript
type AssetUrl = { type: "url"; url: string };
type AssetId = { type: "asset_id"; asset_id: string };
type AssetBase64 = { type: "base64"; media_type: string; data: string };
type VideoAgentFile = AssetUrl | AssetId | AssetBase64;

interface VideoAgentRequest {
  prompt: string;                              // Required, 1-10000 chars
  avatar_id?: string | null;                   // Optional: specific avatar
  voice_id?: string | null;                    // Optional: specific voice
  orientation?: "portrait" | "landscape" | null;
  files?: VideoAgentFile[] | null;             // Max 20 files
  callback_id?: string | null;                 // Requires callback_url if set
  callback_url?: string | null;
}

interface VideoAgentResponse {
  data: {
    session_id: string;
    status: string;
    video_id: string;
    created_at: number;
  };
}

interface VideoAgentError {
  error: {
    code: string;
    message: string;
  };
}

async function generateWithVideoAgent(
  prompt: string,
  options?: {
    avatar_id?: string;
    voice_id?: string;
    orientation?: "portrait" | "landscape";
    files?: VideoAgentFile[];
  }
): Promise<{ session_id: string; video_id: string }> {
  const request: VideoAgentRequest = { prompt, ...options };

  const response = await fetch(
    "https://api.heygen.com/v3/video-agents",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  const json = await response.json();

  if ("error" in json) {
    const err = json as VideoAgentError;
    throw new Error(`Video Agent failed: ${err.error.code} — ${err.error.message}`);
  }

  const result = json as VideoAgentResponse;
  return {
    session_id: result.data.session_id,
    video_id: result.data.video_id,
  };
}
```

## Python

```python
import requests
import os
from typing import Optional

def generate_with_video_agent(
    prompt: str,
    avatar_id: Optional[str] = None,
    voice_id: Optional[str] = None,
    orientation: Optional[str] = None,
    files: Optional[list[dict]] = None,
) -> dict:
    """Returns dict with session_id, status, video_id, created_at."""
    request_body: dict = {"prompt": prompt}

    if avatar_id:
        request_body["avatar_id"] = avatar_id
    if voice_id:
        request_body["voice_id"] = voice_id
    if orientation:
        request_body["orientation"] = orientation
    if files:
        request_body["files"] = files

    response = requests.post(
        "https://api.heygen.com/v3/video-agents",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=request_body,
    )

    data = response.json()
    if "error" in data:
        err = data["error"]
        raise Exception(f"Video Agent failed: {err['code']} — {err['message']}")

    return data["data"]
```

## Examples

### Basic: Prompt Only

```typescript
const { video_id } = await generateWithVideoAgent(
  "Create a 30-second welcome video for new employees at a tech startup. Keep it energetic and modern."
);
```

```python
result = generate_with_video_agent(
    "Create a 30-second welcome video for new employees at a tech startup. Keep it energetic and modern."
)
video_id = result["video_id"]
```

```bash
curl -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 30-second welcome video for new employees at a tech startup. Keep it energetic and modern."
  }'
```

### With Orientation

```typescript
const { video_id } = await generateWithVideoAgent(
  "Explain the benefits of cloud computing for small businesses. Use simple language and real-world examples.",
  { orientation: "landscape" }
);
```

```python
result = generate_with_video_agent(
    "Explain the benefits of cloud computing for small businesses. Use simple language and real-world examples.",
    orientation="landscape",
)
```

```bash
curl -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain the benefits of cloud computing for small businesses. Use simple language and real-world examples.",
    "orientation": "landscape"
  }'
```

### With Specific Avatar and Voice

```typescript
const { video_id } = await generateWithVideoAgent(
  "Present quarterly sales results. Professional tone, data-focused.",
  {
    avatar_id: "josh_lite3_20230714",
    voice_id: "1bd001e7e50f421d891986aad5158bc8",
    orientation: "landscape",
  }
);
```

```python
result = generate_with_video_agent(
    "Present quarterly sales results. Professional tone, data-focused.",
    avatar_id="josh_lite3_20230714",
    voice_id="1bd001e7e50f421d891986aad5158bc8",
    orientation="landscape",
)
```

```bash
curl -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Present quarterly sales results. Professional tone, data-focused.",
    "avatar_id": "josh_lite3_20230714",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "orientation": "landscape"
  }'
```

### With Reference Files

Upload assets first, then reference them:

```typescript
// 1. Upload reference materials (see assets.md)
const logoAssetId = await uploadFile("./company-logo.png", "image/png");
const productImageId = await uploadFile("./product-screenshot.png", "image/png");

// 2. Generate video with references
const { video_id } = await generateWithVideoAgent(
  "Create a product demo video showcasing our new dashboard feature. Use the uploaded screenshots as visual references.",
  {
    orientation: "landscape",
    files: [
      { type: "asset_id", asset_id: logoAssetId },
      { type: "asset_id", asset_id: productImageId },
    ],
  }
);
```

```python
# 1. Upload reference materials (see assets.md)
logo_asset_id = upload_file("./company-logo.png", "image/png")
product_image_id = upload_file("./product-screenshot.png", "image/png")

# 2. Generate video with references
result = generate_with_video_agent(
    "Create a product demo video showcasing our new dashboard feature. Use the uploaded screenshots as visual references.",
    orientation="landscape",
    files=[
        {"type": "asset_id", "asset_id": logo_asset_id},
        {"type": "asset_id", "asset_id": product_image_id},
    ],
)
```

```bash
curl -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a product demo video showcasing our new dashboard feature. Use the uploaded screenshots as visual references.",
    "orientation": "landscape",
    "files": [
      { "type": "asset_id", "asset_id": "uploaded_logo_id" },
      { "type": "url", "url": "https://example.com/product-screenshot.png" }
    ]
  }'
```

## Writing Effective Prompts

See **[prompt-optimizer.md](prompt-optimizer.md)** for comprehensive prompt writing guidance.

The prompt optimizer covers:
- Prompt complexity levels (basic -> scene-by-scene)
- Visual style taxonomy and color specification
- Media type selection (Motion Graphics vs Stock vs AI-generated)
- Scene structure and timing calculations
- Ready-to-use templates for common video types

## Checking Video Status

Video Agent returns a `video_id` — use the standard status endpoint to check progress:

```
GET https://api.heygen.com/v3/videos/{video_id}
```

```typescript
// Same polling as standard video generation
const videoUrl = await waitForVideo(videoId);
```

```python
import time

def wait_for_video(video_id: str, timeout: int = 600) -> str:
    """Poll until video is ready. Returns the video URL."""
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(
            f"https://api.heygen.com/v3/videos/{video_id}",
            headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        )
        data = resp.json()["data"]
        if data["status"] == "completed":
            return data["video_url"]
        if data["status"] == "failed":
            raise Exception(f"Video failed: {data.get('error')}")
        time.sleep(5)
    raise TimeoutError(f"Video {video_id} did not complete within {timeout}s")
```

```bash
curl "https://api.heygen.com/v3/videos/$VIDEO_ID" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

See [video-status.md](video-status.md) for full polling implementation.

## Comparison: Video Agent vs Standard API

### Video Agent Request
```typescript
// Simple: describe what you want
const { video_id } = await generateWithVideoAgent(
  "Create a 60-second tutorial on setting up two-factor authentication. Professional tone, step-by-step."
);
```

### Equivalent Standard API Request
```typescript
// Complex: specify every detail via POST /v3/videos
const videoId = await generateVideo({
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Welcome to this tutorial on two-factor authentication...",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
    // ... more scenes for each step
  ],
  dimension: { width: 1920, height: 1080 },
});
```

## Limitations

- Avatar selection may vary if not specified
- Scene composition is automated
- May not match precise brand guidelines
- Duration is approximate (determined by the agent from the prompt, not directly configurable)

## Best Practices

1. **Be specific in prompts** — More detail = better results
2. **Specify voice if needed** — Use `voice_id` to lock a specific voice for consistency
3. **Lock avatar if needed** — Use `avatar_id` for consistency across videos
4. **Upload reference files** — Help agent understand your brand/product (use `type: "asset_id"` for uploaded assets, `type: "url"` for public URLs)
5. **Iterate on prompts** — Refine based on results
6. **Use for drafts** — Video Agent is great for quick iterations before final production
