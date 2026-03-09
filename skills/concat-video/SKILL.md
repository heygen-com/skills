---
name: concat-video
description: |
  Concatenate multiple video clips into a single video using HeyGen's Node Gateway. Use when: (1) Joining or merging multiple videos into one, (2) Stitching video clips together horizontally or vertically, (3) Creating compilations from separate video segments, (4) Working with HeyGen's /v1/node/execute endpoint for video concatenation.
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Video Concatenation (HeyGen Node Gateway)

Concatenate multiple video clips into a single video. Supports horizontal and vertical orientation, optional aspect ratio normalization, and any number of input clips.

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"node_type": "ConcatVideoNode", "input": {"video_list": [{"video_url": "https://example.com/clip1.mp4"}, {"video_url": "https://example.com/clip2.mp4"}]}}'
```

## Default Workflow

1. Call `POST /v1/node/execute` with `node_type: "ConcatVideoNode"` and a list of videos
2. Receive a `workflow_id` in the response
3. Poll `GET /v1/node/status?workflow_id={id}` every 5 seconds until status is `completed`
4. Use the returned `video_url` from the output

## Execute Concatenation

### Endpoint

`POST https://api.heygen.com/v1/node/execute`

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `node_type` | string | Y | Must be `"ConcatVideoNode"` |
| `input.video_list` | object[] | Y | Array of `{"video_url": "https://..."}` objects to concatenate |
| `input.orientation` | string | | `"horizontal"` (default) or `"vertical"` — layout direction |
| `input.normalize_aspect_ratio` | boolean | | Normalize all clips to the same aspect ratio (default: false) |
| `input.target_aspect_ratio` | string | | Target aspect ratio when normalizing (e.g., `"16:9"`) |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "ConcatVideoNode",
    "input": {
      "video_list": [
        {"video_url": "https://example.com/intro.mp4"},
        {"video_url": "https://example.com/main.mp4"},
        {"video_url": "https://example.com/outro.mp4"}
      ],
      "orientation": "horizontal"
    }
  }'
```

### TypeScript

```typescript
interface ConcatVideoInput {
  video_list: { video_url: string }[];
  orientation?: "horizontal" | "vertical";
  normalize_aspect_ratio?: boolean;
  target_aspect_ratio?: string;
}

async function concatVideos(input: ConcatVideoInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/node/execute", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ node_type: "ConcatVideoNode", input }),
  });

  const json = await response.json();
  return json.data.workflow_id;
}
```

### Python

```python
import requests
import os

def concat_videos(
    video_urls: list[str],
    orientation: str = "horizontal",
    normalize_aspect_ratio: bool = False,
    target_aspect_ratio: str | None = None,
) -> str:
    payload = {
        "node_type": "ConcatVideoNode",
        "input": {
            "video_list": [{"video_url": url} for url in video_urls],
            "orientation": orientation,
            "normalize_aspect_ratio": normalize_aspect_ratio,
        },
    }

    if target_aspect_ratio:
        payload["input"]["target_aspect_ratio"] = target_aspect_ratio

    response = requests.post(
        "https://api.heygen.com/v1/node/execute",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=payload,
    )

    return response.json()["data"]["workflow_id"]
```

### Response Format (Completed)

```json
{
  "data": {
    "workflow_id": "node-gw-c0n1c2a3",
    "status": "completed",
    "output": {
      "video": {
        "video_url": "https://resource.heygen.ai/concat/output.mp4",
        "duration": 95.5
      }
    }
  }
}
```

## Best Practices

1. **Order matters** — videos are concatenated in the order provided in `video_list`
2. **Match aspect ratios** — use `normalize_aspect_ratio: true` when combining clips with different dimensions
3. **Keep clips reasonable** — concatenating many long videos increases processing time
4. **Poll every 5 seconds** — concatenation typically completes within 30-120 seconds depending on total duration
