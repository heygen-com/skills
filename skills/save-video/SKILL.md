---
name: save-video
description: |
  Save a video to your HeyGen library using HeyGen's Node Gateway. Use when: (1) Saving a generated or processed video to HeyGen, (2) Persisting a video URL to your HeyGen video library, (3) Getting a permanent video ID after processing, (4) Working with HeyGen's /v1/node/execute endpoint for saving videos.
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Save Video (HeyGen Node Gateway)

Save a video to your HeyGen library. Takes a video URL and persists it as a named video entry, returning a permanent video ID.

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"node_type": "SaveVideoNode", "input": {"video": {"video_url": "https://example.com/my-video.mp4"}, "title": "My Processed Video"}}'
```

## Default Workflow

1. Call `POST /v1/node/execute` with `node_type: "SaveVideoNode"` and a video URL
2. Receive a `workflow_id` in the response
3. Poll `GET /v1/node/status?workflow_id={id}` every 3 seconds until status is `completed`
4. Use the returned `pacific_video_id` to reference the saved video

## Execute Save

### Endpoint

`POST https://api.heygen.com/v1/node/execute`

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `node_type` | string | Y | Must be `"SaveVideoNode"` |
| `input.video` | object | Y | `{"video_url": "https://..."}` — the video to save |
| `input.title` | string | | Title for the saved video (default: `"Workflow video"`) |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "SaveVideoNode",
    "input": {
      "video": {"video_url": "https://example.com/trimmed-output.mp4"},
      "title": "Q4 Product Demo - Trimmed"
    }
  }'
```

### TypeScript

```typescript
interface SaveVideoInput {
  video: { video_url: string };
  title?: string;
}

async function saveVideo(input: SaveVideoInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/node/execute", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      node_type: "SaveVideoNode",
      input,
    }),
  });

  const json = await response.json();
  return json.data.workflow_id;
}
```

### Python

```python
import requests
import os

def save_video(video_url: str, title: str | None = None) -> str:
    input_data = {
        "video": {"video_url": video_url},
    }

    if title:
        input_data["title"] = title

    response = requests.post(
        "https://api.heygen.com/v1/node/execute",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json={"node_type": "SaveVideoNode", "input": input_data},
    )

    return response.json()["data"]["workflow_id"]
```

### Response Format

```json
{
  "data": {
    "workflow_id": "node-gw-s4v5e6d7",
    "status": "submitted"
  }
}
```

## Check Status

### Endpoint

`GET https://api.heygen.com/v1/node/status?workflow_id={workflow_id}`

### curl

```bash
curl -X GET "https://api.heygen.com/v1/node/status?workflow_id=node-gw-s4v5e6d7" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### Response Format (Completed)

```json
{
  "data": {
    "workflow_id": "node-gw-s4v5e6d7",
    "status": "completed",
    "output": {
      "video": {
        "video_url": "https://resource.heygen.ai/saved/output.mp4"
      },
      "pacific_video_id": "abc123def456"
    }
  }
}
```

## Polling for Completion

```typescript
async function saveVideoAndWait(
  input: SaveVideoInput,
  maxWaitMs = 60000,
  pollIntervalMs = 3000
): Promise<{ video_url: string; pacific_video_id: string }> {
  const workflowId = await saveVideo(input);
  console.log(`Submitted save video: ${workflowId}`);

  const startTime = Date.now();
  while (Date.now() - startTime < maxWaitMs) {
    const response = await fetch(
      `https://api.heygen.com/v1/node/status?workflow_id=${workflowId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );
    const { data } = await response.json();

    switch (data.status) {
      case "completed":
        return {
          video_url: data.output.video.video_url,
          pacific_video_id: data.output.pacific_video_id,
        };
      case "failed":
        throw new Error(data.error?.message || "Save video failed");
      case "not_found":
        throw new Error("Workflow not found");
      default:
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("Save video timed out");
}
```

## Usage Examples

### Save After Trimming

```json
{
  "node_type": "SaveVideoNode",
  "input": {
    "video": {"video_url": "https://resource.heygen.ai/trimmed/clip.mp4"},
    "title": "Trimmed Intro Clip"
  }
}
```

### Save Without Title

```json
{
  "node_type": "SaveVideoNode",
  "input": {
    "video": {"video_url": "https://resource.heygen.ai/generated/avatar-video.mp4"}
  }
}
```

## Best Practices

1. **Always save final outputs** — use SaveVideoNode at the end of a processing pipeline to persist results
2. **Set descriptive titles** — makes videos easier to find in the HeyGen dashboard
3. **Save is fast** — typically completes within 5-10 seconds; poll every 3 seconds
4. **Use the `pacific_video_id`** — this is the permanent identifier for the video in HeyGen
5. **Chain as the final step** — trim, generate, or translate a video, then save the result
