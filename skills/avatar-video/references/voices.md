---
name: voices
description: Listing voices via v3 API, locales, speed/pitch configuration, server-side filtering for HeyGen
---

# HeyGen Voices

HeyGen provides a wide variety of AI voices for different languages, accents, and styles. The v3 voices endpoint (`GET /v3/voices`) is a unified API that replaces both the v2 video voices and v1 TTS audio voices endpoints, with built-in server-side filtering and cursor-based pagination.

## Listing Available Voices

### curl

```bash
curl -X GET "https://api.heygen.com/v3/voices?limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface AudioVoiceItem {
  voice_id: string;
  name: string;
  language: string;
  gender: string;
  preview_audio_url: string | null;
  support_pause: boolean;
  support_locale: boolean;
  type: "public" | "private";
}

interface VoicesResponse {
  data: AudioVoiceItem[];
  has_more: boolean;
  next_token: string | null;
}

async function listVoices(limit = 20): Promise<AudioVoiceItem[]> {
  const response = await fetch(
    `https://api.heygen.com/v3/voices?limit=${limit}`,
    {
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  const json: VoicesResponse = await response.json();
  return json.data;
}
```

### Python

```python
import requests
import os

def list_voices(limit: int = 20) -> list:
    response = requests.get(
        "https://api.heygen.com/v3/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        params={"limit": limit},
    )

    data = response.json()
    return data["data"]
```

## Response Format

```json
{
  "data": [
    {
      "voice_id": "1bd001e7e50f421d891986aad5158bc8",
      "name": "Sara",
      "language": "English",
      "gender": "female",
      "preview_audio_url": "https://files.heygen.ai/...",
      "support_pause": true,
      "support_locale": true,
      "type": "public"
    },
    {
      "voice_id": "de8b5d78f2e0485f88d1e9f5c8e7f9a6",
      "name": "Paul",
      "language": "English",
      "gender": "male",
      "preview_audio_url": "https://files.heygen.ai/...",
      "support_pause": true,
      "support_locale": false,
      "type": "public"
    }
  ],
  "has_more": true,
  "next_token": "eyJsYXN0X2lkIjoiZGU4YjVkNzhmMmUwNDg1Zjg4ZDFlOWY1YzhlN2Y5YTYifQ=="
}
```

## Supported Languages

HeyGen supports many languages including:

| Language | Code | Notes |
|----------|------|-------|
| English (US) | en-US | Multiple voice options |
| English (UK) | en-GB | British accent |
| Spanish | es-ES | Spain Spanish |
| Spanish (Latin) | es-MX | Mexican Spanish |
| French | fr-FR | France French |
| German | de-DE | Standard German |
| Portuguese | pt-BR | Brazilian Portuguese |
| Chinese (Mandarin) | zh-CN | Simplified Chinese |
| Japanese | ja-JP | Standard Japanese |
| Korean | ko-KR | Standard Korean |
| Italian | it-IT | Standard Italian |
| Dutch | nl-NL | Standard Dutch |
| Polish | pl-PL | Standard Polish |
| Arabic | ar-SA | Saudi Arabic |

## Using Voices in Video Generation

### Basic Voice Usage

In the v3 API, video generation uses a flat structure with `script` and `voice_id` fields inside each scene's `audio` object.

#### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "scenes": [
      {
        "avatar": {
          "avatar_id": "josh_lite3_20230714",
          "type": "avatar"
        },
        "audio": {
          "script": "Hello! Welcome to our presentation.",
          "voice_id": "1bd001e7e50f421d891986aad5158bc8"
        }
      }
    ]
  }'
```

#### TypeScript

```typescript
const videoPayload = {
  scenes: [
    {
      avatar: {
        avatar_id: "josh_lite3_20230714",
        type: "avatar",
      },
      audio: {
        script: "Hello! Welcome to our presentation.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};

const response = await fetch("https://api.heygen.com/v3/videos", {
  method: "POST",
  headers: {
    "X-Api-Key": process.env.HEYGEN_API_KEY!,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(videoPayload),
});
```

#### Python

```python
import requests
import os

payload = {
    "scenes": [
        {
            "avatar": {
                "avatar_id": "josh_lite3_20230714",
                "type": "avatar",
            },
            "audio": {
                "script": "Hello! Welcome to our presentation.",
                "voice_id": "1bd001e7e50f421d891986aad5158bc8",
            },
        }
    ]
}

response = requests.post(
    "https://api.heygen.com/v3/videos",
    headers={
        "X-Api-Key": os.environ["HEYGEN_API_KEY"],
        "Content-Type": "application/json",
    },
    json=payload,
)
```

### Voice with Speed and Pitch Adjustment

Speed and pitch settings are specified in a `voice_settings` object within the `audio` block.

```typescript
const videoPayload = {
  scenes: [
    {
      avatar: {
        avatar_id: "josh_lite3_20230714",
        type: "avatar",
      },
      audio: {
        script: "This is spoken at a faster pace with higher pitch.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
        voice_settings: {
          speed: 1.2, // 1.0 is normal, range: 0.5 - 2.0
          pitch: 10,  // Range: -20 to 20
        },
      },
    },
  ],
};
```

```python
payload = {
    "scenes": [
        {
            "avatar": {
                "avatar_id": "josh_lite3_20230714",
                "type": "avatar",
            },
            "audio": {
                "script": "This is spoken at a faster pace with higher pitch.",
                "voice_id": "1bd001e7e50f421d891986aad5158bc8",
                "voice_settings": {
                    "speed": 1.2,
                    "pitch": 10,
                },
            },
        }
    ]
}
```

## Adding Pauses with Break Tags

HeyGen supports SSML-style `<break>` tags to add pauses in scripts.

### Break Tag Format

```
<break time="Xs"/>
```

Where `X` is the duration in seconds (e.g., `1s`, `1.5s`, `0.5s`).

### Requirements

| Rule | Example |
|------|---------|
| Use seconds with "s" suffix | `<break time="1.5s"/>` |
| Must have space before tag | `word <break time="1s"/>` |
| Must have space after tag | `<break time="1s"/> word` |
| Self-closing tag | `<break time="1s"/>` |

**Incorrect:** `word<break time="1s"/>word` (no spaces)
**Correct:** `word <break time="1s"/> word`

### Examples

```typescript
// Single pause
const script1 = "Hello and welcome. <break time=\"1s\"/> Let me introduce our product.";

// Multiple pauses
const script2 = "First point. <break time=\"1.5s\"/> Second point. <break time=\"1s\"/> Third point.";

// Pause at start (dramatic opening)
const script3 = "<break time=\"0.5s\"/> Welcome to our presentation.";

// Longer pause for emphasis
const script4 = "And the winner is... <break time=\"2s\"/> You!";
```

### Full Example

```typescript
const scriptWithPauses = `
Welcome to our product demo. <break time="1s"/>
Today I'll show you three key features. <break time="0.5s"/>
First, let's look at the dashboard. <break time="1.5s"/>
As you can see, it's incredibly intuitive.
`;

const videoPayload = {
  scenes: [
    {
      avatar: {
        avatar_id: "josh_lite3_20230714",
        type: "avatar",
      },
      audio: {
        script: scriptWithPauses,
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### Consecutive Breaks

Multiple consecutive break tags are automatically combined:

```typescript
// These two breaks:
"Hello <break time=\"1s\"/> <break time=\"0.5s\"/> world"

// Are treated as a single 1.5s pause
```

### Best Practices

1. **Use for emphasis** - Add pauses before important points
2. **Keep pauses reasonable** - 0.5s to 2s is typical; longer feels unnatural
3. **Match natural speech** - Add pauses where a human would breathe or pause
4. **Test the output** - Listen to generated audio to verify timing feels right

## Using Custom Audio Instead of TTS

Instead of text-to-speech, you can provide your own audio via the `audio_url` field:

### curl

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "scenes": [
      {
        "avatar": {
          "avatar_id": "josh_lite3_20230714",
          "type": "avatar"
        },
        "audio": {
          "audio_url": "https://example.com/my-audio.mp3"
        }
      }
    ]
  }'
```

### TypeScript

```typescript
const videoPayload = {
  scenes: [
    {
      avatar: {
        avatar_id: "josh_lite3_20230714",
        type: "avatar",
      },
      audio: {
        audio_url: "https://example.com/my-audio.mp3",
      },
    },
  ],
};
```

### Python

```python
payload = {
    "scenes": [
        {
            "avatar": {
                "avatar_id": "josh_lite3_20230714",
                "type": "avatar",
            },
            "audio": {
                "audio_url": "https://example.com/my-audio.mp3",
            },
        }
    ]
}
```

## Filtering Voices

The v3 API supports server-side filtering via query parameters, eliminating the need for client-side filtering.

### Available Filter Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `"public"` \| `"private"` | Filter by voice type |
| `engine` | string | Filter by voice engine (e.g., `"starfish"`) |
| `language` | string | Filter by language (e.g., `"English"`) |
| `gender` | `"male"` \| `"female"` | Filter by gender |
| `limit` | 1-100 | Results per page |
| `token` | string | Cursor for next page |

### By Language

#### curl

```bash
curl -X GET "https://api.heygen.com/v3/voices?language=English&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

#### TypeScript

```typescript
async function getVoicesByLanguage(language: string): Promise<AudioVoiceItem[]> {
  const params = new URLSearchParams({ language, limit: "20" });
  const response = await fetch(
    `https://api.heygen.com/v3/voices?${params}`,
    {
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  const json: VoicesResponse = await response.json();
  return json.data;
}

const englishVoices = await getVoicesByLanguage("English");
const spanishVoices = await getVoicesByLanguage("Spanish");
```

#### Python

```python
def get_voices_by_language(language: str) -> list:
    response = requests.get(
        "https://api.heygen.com/v3/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        params={"language": language, "limit": 20},
    )
    return response.json()["data"]

english_voices = get_voices_by_language("English")
spanish_voices = get_voices_by_language("Spanish")
```

### By Gender

#### curl

```bash
curl -X GET "https://api.heygen.com/v3/voices?gender=female&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

#### TypeScript

```typescript
async function getVoicesByGender(
  gender: "male" | "female"
): Promise<AudioVoiceItem[]> {
  const params = new URLSearchParams({ gender, limit: "20" });
  const response = await fetch(
    `https://api.heygen.com/v3/voices?${params}`,
    {
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  const json: VoicesResponse = await response.json();
  return json.data;
}

const femaleVoices = await getVoicesByGender("female");
```

#### Python

```python
def get_voices_by_gender(gender: str) -> list:
    response = requests.get(
        "https://api.heygen.com/v3/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        params={"gender": gender, "limit": 20},
    )
    return response.json()["data"]

female_voices = get_voices_by_gender("female")
```

### By Engine (TTS-Compatible Voices)

To list only TTS-compatible voices, filter by `engine=starfish`:

```bash
curl -X GET "https://api.heygen.com/v3/voices?engine=starfish&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### Combined Filters

```bash
curl -X GET "https://api.heygen.com/v3/voices?language=English&gender=female&type=public&limit=50" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## Voice Selection Helper

Uses server-side filtering and cursor-based pagination to find matching voices across all pages.

### TypeScript

```typescript
interface VoiceSelectionCriteria {
  language?: string;
  gender?: "male" | "female";
  type?: "public" | "private";
  engine?: string;
}

async function findVoice(
  criteria: VoiceSelectionCriteria
): Promise<AudioVoiceItem | null> {
  const params = new URLSearchParams({ limit: "50" });
  if (criteria.language) params.set("language", criteria.language);
  if (criteria.gender) params.set("gender", criteria.gender);
  if (criteria.type) params.set("type", criteria.type);
  if (criteria.engine) params.set("engine", criteria.engine);

  const response = await fetch(
    `https://api.heygen.com/v3/voices?${params}`,
    {
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  const json: VoicesResponse = await response.json();
  return json.data[0] || null;
}

// Usage
const voice = await findVoice({
  language: "English",
  gender: "female",
  type: "public",
});
```

### Python

```python
def find_voice(
    language: str | None = None,
    gender: str | None = None,
    voice_type: str | None = None,
    engine: str | None = None,
) -> dict | None:
    params: dict = {"limit": 50}
    if language:
        params["language"] = language
    if gender:
        params["gender"] = gender
    if voice_type:
        params["type"] = voice_type
    if engine:
        params["engine"] = engine

    response = requests.get(
        "https://api.heygen.com/v3/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        params=params,
    )

    data = response.json()["data"]
    return data[0] if data else None

# Usage
voice = find_voice(language="English", gender="female", voice_type="public")
```

### Paginating Through All Results

```typescript
async function listAllVoices(
  criteria: VoiceSelectionCriteria = {}
): Promise<AudioVoiceItem[]> {
  const allVoices: AudioVoiceItem[] = [];
  let token: string | null = null;

  do {
    const params = new URLSearchParams({ limit: "100" });
    if (criteria.language) params.set("language", criteria.language);
    if (criteria.gender) params.set("gender", criteria.gender);
    if (criteria.type) params.set("type", criteria.type);
    if (criteria.engine) params.set("engine", criteria.engine);
    if (token) params.set("token", token);

    const response = await fetch(
      `https://api.heygen.com/v3/voices?${params}`,
      {
        headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
      }
    );

    const json: VoicesResponse = await response.json();
    allVoices.push(...json.data);
    token = json.has_more ? json.next_token : null;
  } while (token);

  return allVoices;
}
```

```python
def list_all_voices(**filters) -> list:
    all_voices = []
    token = None

    while True:
        params: dict = {"limit": 100, **filters}
        if token:
            params["token"] = token

        response = requests.get(
            "https://api.heygen.com/v3/voices",
            headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
            params=params,
        )

        result = response.json()
        all_voices.extend(result["data"])

        if not result.get("has_more"):
            break
        token = result.get("next_token")

    return all_voices
```

## Multi-Language Videos

Create videos with different languages per scene:

```typescript
const multiLanguagePayload = {
  scenes: [
    {
      avatar: {
        avatar_id: "josh_lite3_20230714",
        type: "avatar",
      },
      audio: {
        script: "Hello! Welcome to our global product launch.",
        voice_id: "english_voice_id",
      },
    },
    {
      avatar: {
        avatar_id: "josh_lite3_20230714",
        type: "avatar",
      },
      audio: {
        script: "Hola! Bienvenidos al lanzamiento global de nuestro producto.",
        voice_id: "spanish_voice_id",
      },
    },
  ],
};
```

## Matching Voice to Avatar

### Recommended: Use Avatar's Default Voice

Many avatars have a `default_voice_id` that is pre-matched. Use `GET /v3/avatars/looks` to find it.

#### curl

```bash
curl -X GET "https://api.heygen.com/v3/avatars/looks?limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

#### TypeScript

```typescript
const response = await fetch(
  "https://api.heygen.com/v3/avatars/looks?limit=20",
  { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
);
const { data } = await response.json();

// Find an avatar look with a default voice
const look = data.find((l: any) => l.default_voice_id);

if (look) {
  const videoPayload = {
    scenes: [
      {
        avatar: {
          avatar_id: look.avatar_id,
          type: "avatar",
        },
        audio: {
          script: "Hello! This voice was pre-matched to this avatar.",
          voice_id: look.default_voice_id,
        },
      },
    ],
  };
}
```

#### Python

```python
response = requests.get(
    "https://api.heygen.com/v3/avatars/looks",
    headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    params={"limit": 20},
)
looks = response.json()["data"]

# Find a look with a default voice
look = next((l for l in looks if l.get("default_voice_id")), None)

if look:
    payload = {
        "scenes": [
            {
                "avatar": {
                    "avatar_id": look["avatar_id"],
                    "type": "avatar",
                },
                "audio": {
                    "script": "Hello! This voice was pre-matched to this avatar.",
                    "voice_id": look["default_voice_id"],
                },
            }
        ]
    }
```

See [avatars.md](avatars.md) for complete examples.

### Fallback: Match Gender Manually

If the avatar has no default voice, use server-side gender filtering to find a match:

```typescript
async function findMatchingVoiceForAvatar(
  avatarGender: "male" | "female",
  language = "English"
): Promise<AudioVoiceItem | null> {
  const params = new URLSearchParams({
    gender: avatarGender,
    language,
    type: "public",
    limit: "1",
  });

  const response = await fetch(
    `https://api.heygen.com/v3/voices?${params}`,
    {
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  const json: VoicesResponse = await response.json();
  return json.data[0] || null;
}
```

```python
def find_matching_voice_for_avatar(
    avatar_gender: str, language: str = "English"
) -> dict | None:
    response = requests.get(
        "https://api.heygen.com/v3/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        params={
            "gender": avatar_gender,
            "language": language,
            "type": "public",
            "limit": 1,
        },
    )
    data = response.json()["data"]
    return data[0] if data else None
```

## Best Practices

1. **Match voice gender to avatar** - Always pair male voices with male avatars, female with female
2. **Use server-side filters** - Filter by `language`, `gender`, `type`, and `engine` in the query rather than fetching all voices and filtering client-side
3. **Use avatar default voices** - Prefer the `default_voice_id` from `GET /v3/avatars/looks` for the best avatar-voice pairing
4. **Test voice previews** - Listen to `preview_audio_url` before selecting a voice
5. **Consider locale** - Match voice accent to target audience
6. **Use natural pacing** - Adjust speed via `voice_settings.speed` for clarity, typically 0.9-1.1x
7. **Add pauses** - Use SSML `<break>` tags for more natural speech flow
8. **Paginate large results** - Use `token`/`has_more` to iterate through all available voices when needed
9. **Validate availability** - Always verify `voice_id` exists before using it in video generation
10. **Use engine filter for TTS** - When you need TTS-compatible voices only, pass `engine=starfish`
