---
name: trim-video
description: |
  Trim a video by time range using HeyGen's Node Gateway. Use when: (1) Trimming or cutting a video to a specific time range, (2) Removing the beginning or end of a video, (3) Extracting a clip from a longer video, (4) Shortening video duration by cutting from start or end, (5) Working with HeyGen's /v1/node/execute endpoint for video trimming.
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Video Trimming (HeyGen Node Gateway)

Trim a video by time range. Supports start_time, end_time, and duration parameters. Negative values are relative to the end of the video (e.g. `end_time: -10` removes the last 10 seconds). `end_time` and `duration` are mutually exclusive.

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"node_type": "TrimVideoNode", "input": {"video": {"video_url": "https://example.com/video.mp4"}, "start_time": 0, "end_time": 30}}'
```

## Default Workflow

1. Call `POST /v1/node/execute` with `node_type: "TrimVideoNode"` and trim parameters
2. Receive a `workflow_id` in the response
3. Poll `GET /v1/node/status?workflow_id={id}` every 5 seconds until status is `completed`
4. Use the returned `video_url` from the output

## Execute Trim

### Endpoint

`POST https://api.heygen.com/v1/node/execute`

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `node_type` | string | Y | Must be `"TrimVideoNode"` |
| `input.video` | object | Y | `{"video_url": "https://..."}` — the video to trim |
| `input.start_time` | number | | Start time in seconds (default: 0). Negative = relative to end. |
| `input.end_time` | number | | End time in seconds (default: end of video). Mutually exclusive with `duration`. |
| `input.duration` | number | | Duration to keep from `start_time` in seconds. Mutually exclusive with `end_time`. |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "TrimVideoNode",
    "input": {
      "video": {"video_url": "https://example.com/video.mp4"},
      "start_time": 10,
      "end_time": 40
    }
  }'
```

### TypeScript

```typescript
interface TrimVideoInput {
  video: { video_url: string };
  start_time?: number;
  end_time?: number;
  duration?: number;
}

interface ExecuteResponse {
  data: {
    workflow_id: string;
    status: "submitted";
  };
}

async function trimVideo(input: TrimVideoInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/node/execute", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      node_type: "TrimVideoNode",
      input,
    }),
  });

  const json: ExecuteResponse = await response.json();
  return json.data.workflow_id;
}
```

### Python

```python
import requests
import os

def trim_video(
    video_url: str,
    start_time: float | None = None,
    end_time: float | None = None,
    duration: float | None = None,
) -> str:
    payload = {
        "node_type": "TrimVideoNode",
        "input": {
            "video": {"video_url": video_url},
        },
    }

    if start_time is not None:
        payload["input"]["start_time"] = start_time
    if end_time is not None:
        payload["input"]["end_time"] = end_time
    if duration is not None:
        payload["input"]["duration"] = duration

    response = requests.post(
        "https://api.heygen.com/v1/node/execute",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=payload,
    )

    data = response.json()
    return data["data"]["workflow_id"]
```

### Response Format

```json
{
  "data": {
    "workflow_id": "node-gw-a1b2c3d4",
    "status": "submitted"
  }
}
```

## Check Status

### Endpoint

`GET https://api.heygen.com/v1/node/status?workflow_id={workflow_id}`

### curl

```bash
curl -X GET "https://api.heygen.com/v1/node/status?workflow_id=node-gw-a1b2c3d4" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface StatusResponse {
  data: {
    workflow_id: string;
    status: "submitted" | "running" | "completed" | "failed" | "not_found";
    output?: { video: { video_url: string; duration?: number } };
    error?: { type: string; message: string };
  };
}

async function getStatus(workflowId: string): Promise<StatusResponse["data"]> {
  const response = await fetch(
    `https://api.heygen.com/v1/node/status?workflow_id=${workflowId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: StatusResponse = await response.json();
  return json.data;
}
```

### Python

```python
def get_status(workflow_id: str) -> dict:
    response = requests.get(
        f"https://api.heygen.com/v1/node/status?workflow_id={workflow_id}",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    )
    return response.json()["data"]
```

### Response Format (Completed)

```json
{
  "data": {
    "workflow_id": "node-gw-a1b2c3d4",
    "status": "completed",
    "output": {
      "video": {
        "video_url": "https://resource.heygen.ai/trimmed/output.mp4",
        "duration": 30.0
      }
    }
  }
}
```

## Polling for Completion

```typescript
async function trimVideoAndWait(
  input: TrimVideoInput,
  maxWaitMs = 600000,
  pollIntervalMs = 5000
): Promise<string> {
  const workflowId = await trimVideo(input);
  console.log(`Submitted trim job: ${workflowId}`);

  const startTime = Date.now();
  while (Date.now() - startTime < maxWaitMs) {
    const status = await getStatus(workflowId);

    switch (status.status) {
      case "completed":
        return status.output!.video.video_url;
      case "failed":
        throw new Error(status.error?.message || "Trim failed");
      case "not_found":
        throw new Error("Workflow not found");
      default:
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("Trim timed out");
}
```

## Usage Examples

### Trim First 30 Seconds

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "TrimVideoNode",
    "input": {
      "video": {"video_url": "https://example.com/video.mp4"},
      "start_time": 0,
      "end_time": 30
    }
  }'
```

### Remove Last 10 Seconds

```json
{
  "node_type": "TrimVideoNode",
  "input": {
    "video": {"video_url": "https://example.com/video.mp4"},
    "end_time": -10
  }
}
```

### Keep 60 Seconds Starting at 1 Minute

```json
{
  "node_type": "TrimVideoNode",
  "input": {
    "video": {"video_url": "https://example.com/video.mp4"},
    "start_time": 60,
    "duration": 60
  }
}
```

## Best Practices

1. **Use `end_time` or `duration`, not both** — they are mutually exclusive
2. **Negative values are relative to end** — `end_time: -5` means "5 seconds before the end"
3. **Poll every 5 seconds** — trimming typically completes within 30-60 seconds
4. **Check the output `duration`** to verify the trim was applied correctly
5. **Use `video_url` from the output** — the original video is not modified
