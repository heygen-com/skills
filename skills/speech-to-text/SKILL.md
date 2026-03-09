---
name: speech-to-text
description: |
  Transcribe audio or video to text using automatic speech recognition via HeyGen's Node Gateway. Use when: (1) Transcribing audio to text, (2) Getting word-level timestamps from speech, (3) Extracting text from video audio tracks, (4) Detecting the language of spoken content, (5) Working with HeyGen's /v1/node/execute endpoint for ASR.
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Speech-to-Text / ASR (HeyGen Node Gateway)

Transcribe audio or video content to text using automatic speech recognition. Returns word-level timestamps, detected language, and aligned segments.

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"node_type": "ASRNode", "input": {"audio": {"audio_url": "https://example.com/audio.mp3"}}}'
```

## Default Workflow

1. Call `POST /v1/node/execute` with `node_type: "ASRNode"` and an audio or video source
2. Receive a `workflow_id` in the response
3. Poll `GET /v1/node/status?workflow_id={id}` every 5 seconds until status is `completed`
4. Read the transcription from `output.text` with timestamps in `output.segments`

## Execute ASR

### Endpoint

`POST https://api.heygen.com/v1/node/execute`

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `node_type` | string | Y | Must be `"ASRNode"` |
| `input.audio` | object | * | `{"audio_url": "https://..."}` — audio to transcribe (*provide audio or video) |
| `input.video` | object | * | `{"video_url": "https://..."}` — video to extract and transcribe audio from |
| `input.model` | string | | ASR model to use (optional) |
| `input.language` | string | | Language hint (e.g., `"en"`, `"es"`) for better accuracy |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "ASRNode",
    "input": {
      "audio": {"audio_url": "https://example.com/interview.mp3"},
      "language": "en"
    }
  }'
```

### TypeScript

```typescript
interface ASRInput {
  audio?: { audio_url: string };
  video?: { video_url: string };
  model?: string;
  language?: string;
}

async function transcribe(input: ASRInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/node/execute", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ node_type: "ASRNode", input }),
  });

  const json = await response.json();
  return json.data.workflow_id;
}
```

### Python

```python
import requests
import os

def transcribe(
    audio_url: str | None = None,
    video_url: str | None = None,
    language: str | None = None,
) -> str:
    input_data = {}
    if audio_url:
        input_data["audio"] = {"audio_url": audio_url}
    if video_url:
        input_data["video"] = {"video_url": video_url}
    if language:
        input_data["language"] = language

    response = requests.post(
        "https://api.heygen.com/v1/node/execute",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json={"node_type": "ASRNode", "input": input_data},
    )

    return response.json()["data"]["workflow_id"]
```

### Response Format (Completed)

```json
{
  "data": {
    "workflow_id": "node-gw-a5r6n7o8",
    "status": "completed",
    "output": {
      "text": "Hello and welcome to our product demo...",
      "language": "en",
      "segments": [
        {"text": "Hello and welcome", "start": 0.0, "end": 1.2},
        {"text": "to our product demo", "start": 1.2, "end": 2.8}
      ]
    }
  }
}
```

## Best Practices

1. **Provide a language hint** for better accuracy, especially for non-English content
2. **Use audio input when possible** — it's faster than extracting audio from video
3. **Check `segments`** for word-level timestamps useful for captioning and syncing
4. **ASR is fast** — typically completes within 10-30 seconds for short clips
5. **Use the detected `language`** in the output to chain with translation workflows
