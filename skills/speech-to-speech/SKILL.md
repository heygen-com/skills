---
name: speech-to-speech
description: |
  Convert speech audio to another voice using HeyGen's Node Gateway. Use when: (1) Changing the voice in an audio recording, (2) Voice conversion or voice cloning from audio, (3) Re-voicing content with a different speaker, (4) Working with HeyGen's /v1/node/execute endpoint for speech-to-speech conversion.
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Speech-to-Speech (HeyGen Node Gateway)

Convert speech audio from one voice to another. Preserves the content and timing while changing the speaker's voice characteristics.

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"node_type": "STSNode", "input": {"audio_url": "https://example.com/speech.mp3", "voice": {"voice_id": "YOUR_VOICE_ID"}}}'
```

## Default Workflow

1. Call `POST /v1/node/execute` with `node_type: "STSNode"`, source audio URL, and target voice
2. Receive a `workflow_id` in the response
3. Poll `GET /v1/node/status?workflow_id={id}` every 5 seconds until status is `completed`
4. Use the returned `audio_url` from the output

## Execute Voice Conversion

### Endpoint

`POST https://api.heygen.com/v1/node/execute`

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `node_type` | string | Y | Must be `"STSNode"` |
| `input.audio_url` | string | Y | URL of the source audio to convert |
| `input.voice` | object | Y | `{"voice_id": "..."}` — target voice to convert to |
| `input.emotion` | string | | Emotion style for the output (optional) |
| `input.settings` | object | | Advanced voice conversion settings (optional) |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/node/execute" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "STSNode",
    "input": {
      "audio_url": "https://example.com/original-speech.mp3",
      "voice": {"voice_id": "YOUR_VOICE_ID"}
    }
  }'
```

### TypeScript

```typescript
interface STSInput {
  audio_url: string;
  voice: { voice_id: string };
  emotion?: string;
  settings?: Record<string, any>;
}

async function speechToSpeech(input: STSInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/node/execute", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ node_type: "STSNode", input }),
  });

  const json = await response.json();
  return json.data.workflow_id;
}
```

### Python

```python
import requests
import os

def speech_to_speech(audio_url: str, voice_id: str, emotion: str | None = None) -> str:
    payload = {
        "node_type": "STSNode",
        "input": {
            "audio_url": audio_url,
            "voice": {"voice_id": voice_id},
        },
    }

    if emotion:
        payload["input"]["emotion"] = emotion

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
    "workflow_id": "node-gw-s1t2s3n4",
    "status": "completed",
    "output": {
      "audio": {
        "audio_url": "https://resource.heygen.ai/sts/output.wav",
        "duration": 12.5
      }
    }
  }
}
```

## Best Practices

1. **Use clear source audio** — background noise reduces conversion quality
2. **Get voice IDs from `GET /v2/voices`** or `GET /v1/audio/voices` to find available voices
3. **Voice conversion preserves timing** — output duration matches input
4. **Processing takes 15-60 seconds** depending on audio length
5. **Chain with avatar inference** — use converted audio to drive avatar videos
