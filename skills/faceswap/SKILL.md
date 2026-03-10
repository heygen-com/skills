---
name: faceswap
description: |
  Swap faces in a video using AI via the HeyGen API. Use when: (1) Replacing a face in a video with another face, (2) Face swapping from a source image onto a target video, (3) Creating personalized videos by swapping in a person's face, (4) Working with HeyGen's /v1/nodes/executions endpoint for face swap processing.
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Face Swap (HeyGen API)

Swap a face from a source image into a target video using GPU-accelerated AI processing. The source image provides the face to swap in, and the target video receives the new face.

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X POST "https://api.heygen.com/v1/nodes/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"node_type": "FaceswapNode", "input": {"source_image_url": "https://example.com/face.jpg", "target_video_url": "https://example.com/video.mp4"}}'
```

## Default Workflow

1. Call `POST /v1/nodes/executions` with `node_type: "FaceswapNode"`, a source face image, and a target video
2. Receive a `execution_id` in the response
3. Poll `GET /v1/nodes/executions/{id}` every 10 seconds until status is `completed`
4. Use the returned `video_url` from the output

## Execute Face Swap

### Endpoint

`POST https://api.heygen.com/v1/nodes/executions`

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `node_type` | string | Y | Must be `"FaceswapNode"` |
| `input.source_image_url` | string | Y | URL of the face image to swap in |
| `input.target_video_url` | string | Y | URL of the video to apply the face swap to |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/nodes/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "FaceswapNode",
    "input": {
      "source_image_url": "https://example.com/face-photo.jpg",
      "target_video_url": "https://example.com/original-video.mp4"
    }
  }'
```

### TypeScript

```typescript
interface FaceswapInput {
  source_image_url: string;
  target_video_url: string;
}

interface ExecuteResponse {
  data: {
    execution_id: string;
    status: "submitted";
  };
}

async function faceswap(input: FaceswapInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/nodes/executions", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      node_type: "FaceswapNode",
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

def faceswap(source_image_url: str, target_video_url: str) -> str:
    payload = {
        "node_type": "FaceswapNode",
        "input": {
            "source_image_url": source_image_url,
            "target_video_url": target_video_url,
        },
    }

    response = requests.post(
        "https://api.heygen.com/v1/nodes/executions",
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
    "execution_id": "node-gw-f1s2w3p4",
    "status": "submitted"
  }
}
```

## Check Status

### Endpoint

`GET https://api.heygen.com/v1/nodes/executions/{execution_id}`

### curl

```bash
curl -X GET "https://api.heygen.com/v1/nodes/executions/node-gw-f1s2w3p4" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### Response Format (Completed)

```json
{
  "data": {
    "execution_id": "node-gw-f1s2w3p4",
    "status": "completed",
    "output": {
      "video_url": "https://resource.heygen.ai/faceswap/output.mp4"
    }
  }
}
```

## Polling for Completion

```typescript
async function faceswapAndWait(
  input: FaceswapInput,
  maxWaitMs = 600000,
  pollIntervalMs = 10000
): Promise<string> {
  const executionId = await faceswap(input);
  console.log(`Submitted face swap: ${executionId}`);

  const startTime = Date.now();
  while (Date.now() - startTime < maxWaitMs) {
    const response = await fetch(
      `https://api.heygen.com/v1/nodes/executions/${executionId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );
    const { data } = await response.json();

    switch (data.status) {
      case "completed":
        return data.output.video_url;
      case "failed":
        throw new Error(data.error?.message || "Face swap failed");
      case "not_found":
        throw new Error("Workflow not found");
      default:
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("Face swap timed out");
}
```

## Usage Examples

### Basic Face Swap

```bash
curl -X POST "https://api.heygen.com/v1/nodes/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "FaceswapNode",
    "input": {
      "source_image_url": "https://example.com/headshot.jpg",
      "target_video_url": "https://example.com/presentation.mp4"
    }
  }'
```

### Chain with Avatar Video

Generate an avatar video first, then swap in a custom face:

```python
import time

# Step 1: Generate avatar video
avatar_execution_id = requests.post(
    "https://api.heygen.com/v1/nodes/executions",
    headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"], "Content-Type": "application/json"},
    json={
        "node_type": "AvatarInferenceNode",
        "input": {
            "avatar": {"avatar_id": "Angela-inblackskirt-20220820"},
            "audio_list": [{"audio_url": "https://example.com/speech.mp3"}],
        },
    },
).json()["data"]["execution_id"]

# Step 2: Wait for avatar video to complete
while True:
    status = requests.get(
        f"https://api.heygen.com/v1/nodes/executions/{avatar_execution_id}",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    ).json()["data"]
    if status["status"] == "completed":
        avatar_video_url = status["output"]["video"]["video_url"]
        break
    time.sleep(10)

# Step 3: Swap in a custom face
faceswap_execution_id = faceswap(
    source_image_url="https://example.com/custom-face.jpg",
    target_video_url=avatar_video_url,
)
```

## Best Practices

1. **Use a clear, front-facing face photo** — the source image should show a single face with good lighting
2. **Face swap is GPU-intensive** — expect 1-3 minutes processing time, poll every 10 seconds
3. **Source image quality matters** — higher resolution face photos produce better results
4. **One face per source image** — the source should contain exactly one face to swap in
5. **Works with any video** — the target video can be an avatar video, a recording, or any video with visible faces
6. **Chain with other nodes** — generate an avatar video first, then swap in a custom face for personalization
