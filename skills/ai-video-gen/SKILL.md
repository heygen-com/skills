---
name: ai-video-gen
description: |
  Generate AI videos from text prompts using the HeyGen API. Use when: (1) Generating videos from text descriptions, (2) Creating AI-generated video clips for content production, (3) Image-to-video generation with a reference image, (4) Choosing between video generation providers (VEO, Kling, Sora, Runway, Seedance), (5) Working with HeyGen's /v1/workflows/executions endpoint for video generation.
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Video Generation (HeyGen API)

Generate AI videos from text prompts. Supports multiple providers (VEO 3.1, Kling, Sora, Runway, Seedance), configurable aspect ratios, and optional reference images for image-to-video generation.

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workflow_type": "GenerateVideoNode", "input": {"prompt": "A drone shot flying over a coastal city at sunset"}}'
```

## Default Workflow

1. Call `POST /v1/workflows/executions` with `workflow_type: "GenerateVideoNode"` and your prompt
2. Receive a `execution_id` in the response
3. Poll `GET /v1/workflows/executions/{id}` every 10 seconds until status is `completed`
4. Use the returned `video_url` from the output

## Execute Video Generation

### Endpoint

`POST https://api.heygen.com/v1/workflows/executions`

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `workflow_type` | string | Y | Must be `"GenerateVideoNode"` |
| `input.prompt` | string | Y | Text description of the video to generate |
| `input.provider` | string | | Video generation provider (default: `"veo_3_1"`). See Providers below. |
| `input.aspect_ratio` | string | | Aspect ratio (default: `"16:9"`). Common values: `"16:9"`, `"9:16"`, `"1:1"` |
| `input.reference_image_url` | string | | Reference image URL for image-to-video generation |
| `input.tail_image_url` | string | | Tail image URL for last-frame guidance |
| `input.config` | object | | Provider-specific configuration overrides |

### Providers

| Provider | Value | Description |
|----------|-------|-------------|
| VEO 3.1 | `"veo_3_1"` | Google VEO 3.1 (default, highest quality) |
| VEO 3.1 Fast | `"veo_3_1_fast"` | Faster VEO 3.1 variant |
| VEO 3 | `"veo3"` | Google VEO 3 |
| VEO 3 Fast | `"veo3_fast"` | Faster VEO 3 variant |
| VEO 2 | `"veo2"` | Google VEO 2 |
| Kling Pro | `"kling_pro"` | Kling Pro model |
| Kling V2 | `"kling_v2"` | Kling V2 model |
| Sora V2 | `"sora_v2"` | OpenAI Sora V2 |
| Sora V2 Pro | `"sora_v2_pro"` | OpenAI Sora V2 Pro |
| Runway Gen-4 | `"runway_gen4"` | Runway Gen-4 |
| Seedance Lite | `"seedance_lite"` | Seedance Lite |
| Seedance Pro | `"seedance_pro"` | Seedance Pro |
| LTX Distilled | `"ltx_distilled"` | LTX Distilled (fastest) |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "GenerateVideoNode",
    "input": {
      "prompt": "A drone shot flying over a coastal city at golden hour, cinematic lighting",
      "provider": "veo_3_1",
      "aspect_ratio": "16:9"
    }
  }'
```

### TypeScript

```typescript
interface GenerateVideoInput {
  prompt: string;
  provider?: string;
  aspect_ratio?: string;
  reference_image_url?: string;
  tail_image_url?: string;
  config?: Record<string, any>;
}

interface ExecuteResponse {
  data: {
    execution_id: string;
    status: "submitted";
  };
}

async function generateVideo(input: GenerateVideoInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/workflows/executions", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      workflow_type: "GenerateVideoNode",
      input,
    }),
  });

  const json: ExecuteResponse = await response.json();
  return json.data.execution_id;
}
```

### Python

```python
import requests
import os

def generate_video(
    prompt: str,
    provider: str = "veo_3_1",
    aspect_ratio: str = "16:9",
    reference_image_url: str | None = None,
    tail_image_url: str | None = None,
) -> str:
    payload = {
        "workflow_type": "GenerateVideoNode",
        "input": {
            "prompt": prompt,
            "provider": provider,
            "aspect_ratio": aspect_ratio,
        },
    }

    if reference_image_url:
        payload["input"]["reference_image_url"] = reference_image_url
    if tail_image_url:
        payload["input"]["tail_image_url"] = tail_image_url

    response = requests.post(
        "https://api.heygen.com/v1/workflows/executions",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=payload,
    )

    data = response.json()
    return data["data"]["execution_id"]
```

### Response Format

```json
{
  "data": {
    "execution_id": "node-gw-v1d2e3o4",
    "status": "submitted"
  }
}
```

## Check Status

### Endpoint

`GET https://api.heygen.com/v1/workflows/executions/{execution_id}`

### curl

```bash
curl -X GET "https://api.heygen.com/v1/workflows/executions/node-gw-v1d2e3o4" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### Response Format (Completed)

```json
{
  "data": {
    "execution_id": "node-gw-v1d2e3o4",
    "status": "completed",
    "output": {
      "video": {
        "video_url": "https://resource.heygen.ai/generated/video.mp4",
        "video_id": "abc123"
      },
      "asset_id": "asset-xyz789"
    }
  }
}
```

## Polling for Completion

```typescript
async function generateVideoAndWait(
  input: GenerateVideoInput,
  maxWaitMs = 600000,
  pollIntervalMs = 10000
): Promise<{ video_url: string; video_id: string; asset_id: string }> {
  const executionId = await generateVideo(input);
  console.log(`Submitted video generation: ${executionId}`);

  const startTime = Date.now();
  while (Date.now() - startTime < maxWaitMs) {
    const response = await fetch(
      `https://api.heygen.com/v1/workflows/executions/${executionId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );
    const { data } = await response.json();

    switch (data.status) {
      case "completed":
        return {
          video_url: data.output.video.video_url,
          video_id: data.output.video.video_id,
          asset_id: data.output.asset_id,
        };
      case "failed":
        throw new Error(data.error?.message || "Video generation failed");
      case "not_found":
        throw new Error("Workflow not found");
      default:
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("Video generation timed out");
}
```

## Usage Examples

### Simple Text-to-Video

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "GenerateVideoNode",
    "input": {
      "prompt": "A person walking through a sunlit park, shallow depth of field"
    }
  }'
```

### Image-to-Video

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "Animate this product photo with a slow zoom and soft particle effects",
    "reference_image_url": "https://example.com/product-photo.png",
    "provider": "kling_pro"
  }
}
```

### Vertical Format for Social Media

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "A trendy coffee shop interior, camera slowly panning across the counter",
    "aspect_ratio": "9:16",
    "provider": "veo_3_1"
  }
}
```

### Fast Generation with LTX

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "Abstract colorful shapes morphing and flowing",
    "provider": "ltx_distilled"
  }
}
```

## Best Practices

1. **Be descriptive in prompts** — include camera movement, lighting, style, and mood details
2. **Default to VEO 3.1** for highest quality; use `ltx_distilled` or `veo3_fast` when speed matters
3. **Use reference images** for image-to-video generation — great for animating product photos or still images
4. **Video generation is the slowest workflow** — allow up to 5 minutes, poll every 10 seconds
5. **Aspect ratio matters** — use `9:16` for social media stories/reels, `16:9` for landscape, `1:1` for square
6. **Output includes `asset_id`** — use this to reference the generated video in other HeyGen workflows
7. **Output URLs are temporary** — download or save generated videos promptly
