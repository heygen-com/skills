---
name: photo-avatars
description: Animating photos into high-quality videos using HeyGen's v3 API with Avatar IV technology
---

# Photo Avatars

Animate a static photo into a speaking video. Use `POST /v3/videos` with `"type": "image"` and a nested `image` field (AssetInput discriminated union: `{ "type": "url", "url": "..." }` or `{ "type": "asset_id", "asset_id": "..." }`) — this uses Avatar IV technology automatically for high-quality results, no avatar group creation needed.

## Direct Image-to-Video (v3 API)

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `type` | string | ✓ | Must be `"image"` |
| `image` | AssetInput | ✓ | Image to animate. Either `{ "type": "url", "url": "..." }` for a public URL, or `{ "type": "asset_id", "asset_id": "..." }` for an uploaded asset. |
| `script` | string | ✓ | Text for the avatar to speak |
| `voice_id` | string | ✓ | Voice to use |
| `motion_prompt` | string | | Natural-language prompt controlling body motion (photo avatars only) |
| `expressiveness` | string | | `"high"`, `"medium"`, or `"low"` (photo avatars only, defaults to `"low"`) |
| `aspect_ratio` | string | | `"16:9"` or `"9:16"` |
| `resolution` | string | | `"1080p"` or `"720p"` |
| `remove_background` | boolean | | Remove background from the photo |

**AssetInput** is a discriminated union on the `type` field:
- URL variant: `{ "type": "url", "url": "https://example.com/photo.jpg" }`
- Asset ID variant: `{ "type": "asset_id", "asset_id": "uploaded_asset_id" }`

### curl Example

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "image": { "type": "url", "url": "https://example.com/portrait.jpg" },
    "script": "Hello! This is a high-quality photo avatar video.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "aspect_ratio": "16:9",
    "resolution": "1080p"
  }'
```

Response:
```json
{
  "error": null,
  "data": {
    "video_id": "abc123def456"
  }
}
```

### TypeScript Example

```typescript
type AssetInput =
  | { type: "url"; url: string }
  | { type: "asset_id"; asset_id: string };

interface PhotoVideoRequest {
  type: "image";
  image: AssetInput;
  script: string;
  voice_id: string;
  motion_prompt?: string;
  expressiveness?: "high" | "medium" | "low";
  aspect_ratio?: "16:9" | "9:16";
  resolution?: "1080p" | "720p";
  remove_background?: boolean;
}

interface VideoResponse {
  error: string | null;
  data: {
    video_id: string;
  };
}

interface VideoStatusResponse {
  error: string | null;
  data: {
    video_id: string;
    status: "pending" | "processing" | "completed" | "failed";
    video_url?: string;
    thumbnail_url?: string;
    duration?: number;
    error?: string;
  };
}

async function createPhotoVideo(config: PhotoVideoRequest): Promise<string> {
  const response = await fetch("https://api.heygen.com/v3/videos", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  const json: VideoResponse = await response.json();
  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.video_id;
}

async function pollVideoStatus(videoId: string): Promise<string> {
  for (let i = 0; i < 120; i++) {
    const response = await fetch(
      `https://api.heygen.com/v3/videos/${videoId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );

    const json: VideoStatusResponse = await response.json();

    if (json.data.status === "completed") {
      return json.data.video_url!;
    }
    if (json.data.status === "failed") {
      throw new Error(json.data.error ?? "Video generation failed");
    }

    await new Promise((r) => setTimeout(r, 5000));
  }

  throw new Error("Video generation timed out");
}

// Usage
const videoId = await createPhotoVideo({
  type: "image",
  image: { type: "url", url: "https://example.com/portrait.jpg" },
  script: "Hello! This is a high-quality photo avatar video.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  aspect_ratio: "16:9",
  resolution: "1080p",
});

const videoUrl = await pollVideoStatus(videoId);
console.log("Video ready:", videoUrl);
```

### Python Example

```python
import requests
import os
import time

def create_photo_video(
    script: str,
    voice_id: str,
    image_url: str | None = None,
    image_asset_id: str | None = None,
    motion_prompt: str | None = None,
    expressiveness: str | None = None,
    aspect_ratio: str = "16:9",
    resolution: str = "1080p",
    remove_background: bool = False,
) -> str:
    api_key = os.environ["HEYGEN_API_KEY"]

    # Build the AssetInput discriminated union
    if image_url:
        image_input = {"type": "url", "url": image_url}
    elif image_asset_id:
        image_input = {"type": "asset_id", "asset_id": image_asset_id}
    else:
        raise ValueError("Provide either image_url or image_asset_id")

    payload: dict = {
        "type": "image",
        "image": image_input,
        "script": script,
        "voice_id": voice_id,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    }

    if motion_prompt:
        payload["motion_prompt"] = motion_prompt
    if expressiveness:
        payload["expressiveness"] = expressiveness
    if remove_background:
        payload["remove_background"] = True

    resp = requests.post(
        "https://api.heygen.com/v3/videos",
        headers={
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
        },
        json=payload,
    )

    data = resp.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["video_id"]


def poll_video_status(video_id: str) -> str:
    api_key = os.environ["HEYGEN_API_KEY"]

    for _ in range(120):
        resp = requests.get(
            f"https://api.heygen.com/v3/videos/{video_id}",
            headers={"X-Api-Key": api_key},
        )
        data = resp.json()["data"]

        if data["status"] == "completed":
            return data["video_url"]
        if data["status"] == "failed":
            raise Exception(data.get("error", "Video generation failed"))

        time.sleep(5)

    raise Exception("Video generation timed out")


# Usage
video_id = create_photo_video(
    image_url="https://example.com/portrait.jpg",
    script="Hello! This is a high-quality photo avatar video.",
    voice_id="1bd001e7e50f421d891986aad5158bc8",
)
video_url = poll_video_status(video_id)
print(f"Video ready: {video_url}")
```

### Motion Prompts and Expressiveness

Use `motion_prompt` and `expressiveness` to control how the photo avatar moves and emotes:

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "image": { "type": "url", "url": "https://example.com/portrait.jpg" },
    "script": "Let me tell you about our exciting new product launch.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "motion_prompt": "nodding head and smiling, gesturing with hands while speaking",
    "expressiveness": "high",
    "aspect_ratio": "16:9"
  }'
```

| Expressiveness | Description |
|----------------|-------------|
| `low` | Subtle, minimal movement (default) |
| `medium` | Natural, moderate movement |
| `high` | Energetic, pronounced movement |

## Uploading Images

If your image is not publicly accessible via URL, upload it first using the asset upload endpoint. Then use the returned asset ID with the `asset_id` variant of the `image` field.

**Endpoint:** `POST https://upload.heygen.com/v1/asset`

```bash
curl -X POST "https://upload.heygen.com/v1/asset" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: image/jpeg" \
  --data-binary '@./portrait.jpg'
```

Response:
```json
{
  "code": 100,
  "data": {
    "id": "741299e941764988b432ed3a6757878f",
    "name": "741299e941764988b432ed3a6757878f",
    "file_type": "image",
    "url": "https://resource2.heygen.ai/image/.../original.jpg",
    "image_key": "image/741299e941764988b432ed3a6757878f/original.jpg"
  }
}
```

Then use the asset `id` in `POST /v3/videos`:

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "image": { "type": "asset_id", "asset_id": "741299e941764988b432ed3a6757878f" },
    "script": "Hello from an uploaded photo!",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8"
  }'
```

See [assets.md](assets.md) for full upload details.

## AI-Generated Photo Avatars

Generate synthetic photo avatars from text descriptions instead of uploading a photo.

**Endpoint:** `POST https://api.heygen.com/v2/photo_avatar/photo/generate`

> **Note:** This endpoint is still v2 (no v3 equivalent). After generating an image, use the resulting image URL in `POST /v3/videos` with `"type": "image"` and `"image": { "type": "url", "url": "..." }` for high-quality video generation.

> **IMPORTANT: All 8 fields are REQUIRED.** The API will reject requests missing any field.
> When a user asks to "generate an AI avatar of a professional man", you need to ask for or select values for ALL fields below.

### Required Fields (ALL must be provided)

| Field | Type | Allowed Values |
|-------|------|----------------|
| `name` | string | Name for the generated avatar |
| `age` | enum | `"Young Adult"`, `"Early Middle Age"`, `"Late Middle Age"`, `"Senior"`, `"Unspecified"` |
| `gender` | enum | `"Woman"`, `"Man"`, `"Unspecified"` |
| `ethnicity` | enum | `"White"`, `"Black"`, `"Asian American"`, `"East Asian"`, `"South East Asian"`, `"South Asian"`, `"Middle Eastern"`, `"Pacific"`, `"Hispanic"`, `"Unspecified"` |
| `orientation` | enum | `"square"`, `"horizontal"`, `"vertical"` |
| `pose` | enum | `"half_body"`, `"close_up"`, `"full_body"` |
| `style` | enum | `"Realistic"`, `"Pixar"`, `"Cinematic"`, `"Vintage"`, `"Noir"`, `"Cyberpunk"`, `"Unspecified"` |
| `appearance` | string | Text prompt describing appearance (clothing, mood, lighting, etc). Max 1000 chars |

### curl Example

```bash
curl -X POST "https://api.heygen.com/v2/photo_avatar/photo/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Product Demo",
    "age": "Young Adult",
    "gender": "Woman",
    "ethnicity": "White",
    "orientation": "horizontal",
    "pose": "half_body",
    "style": "Realistic",
    "appearance": "Professional woman with a friendly smile, wearing a navy blue blazer over a white blouse, soft studio lighting, clean neutral background"
  }'
```

Response:
```json
{
  "error": null,
  "data": {
    "generation_id": "6a7f7f2795de4599bec7cf1e06babe30"
  }
}
```

### Check Generation Status

**Endpoint:** `GET https://api.heygen.com/v2/photo_avatar/generation/{generation_id}`

The response includes multiple generated images to choose from:

```json
{
  "error": null,
  "data": {
    "id": "6a7f7f2795de4599bec7cf1e06babe30",
    "status": "success",
    "image_url_list": [
      "https://resource2.heygen.ai/photo_generation/.../image1.jpg",
      "https://resource2.heygen.ai/photo_generation/.../image2.jpg",
      "https://resource2.heygen.ai/photo_generation/.../image3.jpg",
      "https://resource2.heygen.ai/photo_generation/.../image4.jpg"
    ],
    "image_key_list": [
      "photo_generation/.../image1.jpg",
      "photo_generation/.../image2.jpg",
      "photo_generation/.../image3.jpg",
      "photo_generation/.../image4.jpg"
    ]
  }
}
```

### AI Photo to Video (Recommended Flow)

Generate an AI photo, then use the resulting image URL directly in `POST /v3/videos`:

```typescript
// 1. Generate AI photo
const genResponse = await fetch(
  "https://api.heygen.com/v2/photo_avatar/photo/generate",
  {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: "Product Demo Host",
      age: "Young Adult",
      gender: "Woman",
      ethnicity: "Unspecified",
      orientation: "horizontal",
      pose: "half_body",
      style: "Realistic",
      appearance:
        "Professional woman, navy blazer, friendly smile, soft lighting",
    }),
  }
);

const { data: genData } = await genResponse.json();
const generationId = genData.generation_id;

// 2. Poll until generation completes
let imageUrl: string | undefined;
for (let i = 0; i < 60; i++) {
  const statusResp = await fetch(
    `https://api.heygen.com/v2/photo_avatar/generation/${generationId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );
  const statusJson = await statusResp.json();

  if (statusJson.data.status === "success") {
    imageUrl = statusJson.data.image_url_list[0];
    break;
  }
  if (statusJson.data.status === "failed") {
    throw new Error("Photo generation failed");
  }
  await new Promise((r) => setTimeout(r, 5000));
}

if (!imageUrl) throw new Error("Photo generation timed out");

// 3. Create video using v3 API with the generated image URL
const videoResp = await fetch("https://api.heygen.com/v3/videos", {
  method: "POST",
  headers: {
    "X-Api-Key": process.env.HEYGEN_API_KEY!,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    type: "image" as const,
    image: { type: "url" as const, url: imageUrl },
    script: "Welcome to our product demo!",
    voice_id: "1bd001e7e50f421d891986aad5158bc8",
    aspect_ratio: "16:9",
    resolution: "1080p",
  }),
});

const { data: videoData } = await videoResp.json();
console.log("Video ID:", videoData.video_id);
```

### Pre-Generation Checklist

Before calling the AI generation API, ensure you have values for ALL fields:

| # | Field | Question to Ask / Default |
|---|-------|---------------------------|
| 1 | `name` | What should we call this avatar? |
| 2 | `age` | Young Adult / Early Middle Age / Late Middle Age / Senior? |
| 3 | `gender` | Woman / Man? |
| 4 | `ethnicity` | Which ethnicity? (see enum values above) |
| 5 | `orientation` | horizontal (landscape) / vertical (portrait) / square? |
| 6 | `pose` | half_body (recommended) / close_up / full_body? |
| 7 | `style` | Realistic (recommended) / Cinematic / other? |
| 8 | `appearance` | Describe clothing, expression, lighting, background |

**If the user only provides a vague request** like "create a professional looking man", ask them to specify the missing fields OR make reasonable defaults (e.g., "Early Middle Age", "Realistic" style, "half_body" pose, "horizontal" orientation).

### Appearance Prompt Tips

The `appearance` field is a text prompt - be descriptive:

**Good prompts:**
- "Professional woman with shoulder-length brown hair, wearing a light blue button-down shirt, warm friendly smile, soft studio lighting, clean white background"
- "Young man with short black hair, casual tech startup style, wearing a dark hoodie, confident expression, modern office background with plants"

**Avoid:**
- Vague descriptions: "a nice person"
- Conflicting attributes
- Requesting specific real people

## Legacy: Creating Photo Avatar Groups

> **Note:** This is the legacy workflow. For most use cases, prefer the direct `"type": "image"` approach with `POST /v3/videos` described above. The avatar group workflow is more complex and does not produce better results.

The legacy workflow is: **Upload Image -> Create Avatar Group -> Use in Video**

### Step 1: Upload the Image

Upload a portrait photo using the asset upload endpoint (see [Uploading Images](#uploading-images) above).

### Step 2: Create Photo Avatar Group

Use the `image_key` from the upload response to create a photo avatar group.

**Endpoint:** `POST https://api.heygen.com/v2/photo_avatar/avatar_group/create`

```bash
curl -X POST "https://api.heygen.com/v2/photo_avatar/avatar_group/create" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_key": "image/741299e941764988b432ed3a6757878f/original.jpg",
    "name": "My Photo Avatar"
  }'
```

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `image_key` | string | ✓ | S3 image key from upload response |
| `name` | string | ✓ | Display name for the avatar |
| `generation_id` | string | | If using AI-generated photo |

Response:
```json
{
  "error": null,
  "data": {
    "id": "045c260bc0364727b2cbe50442c3a5bf",
    "image_url": "https://files2.heygen.ai/...",
    "created_at": 1771798135.777256,
    "name": "My Photo Avatar",
    "status": "pending",
    "group_id": "045c260bc0364727b2cbe50442c3a5bf",
    "is_motion": false,
    "business_type": "uploaded"
  }
}
```

### Step 3: Wait for Processing

Poll `GET /v2/photo_avatar/{id}` until `status` is `"completed"`.

### Step 4: Use in Video Generation

Use the photo avatar look ID as `avatar_id` in `POST /v3/videos`:

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "avatar",
    "avatar_id": "045c260bc0364727b2cbe50442c3a5bf",
    "script": "Hello! This is my photo avatar speaking.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "aspect_ratio": "16:9"
  }'
```

### Adding Photos to an Existing Group

**Endpoint:** `POST https://api.heygen.com/v2/photo_avatar/avatar_group/add`

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `group_id` | string | ✓ | Existing avatar group ID |
| `image_keys` | string[] | ✓ | Array of S3 image keys |
| `name` | string | ✓ | Name for the new looks |

### Training a Photo Avatar Group

**Endpoint:** `POST https://api.heygen.com/v2/photo_avatar/train`

```bash
curl -X POST "https://api.heygen.com/v2/photo_avatar/train" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_id": "045c260bc0364727b2cbe50442c3a5bf"}'
```

Check training status: `GET /v2/photo_avatar/train/status/{group_id}`

## Managing Photo Avatars

### Get Photo Avatar Details

**Endpoint:** `GET https://api.heygen.com/v2/photo_avatar/{id}`

```typescript
async function getPhotoAvatar(id: string): Promise<any> {
  const response = await fetch(
    `https://api.heygen.com/v2/photo_avatar/${id}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );
  return response.json();
}
```

### Delete Photo Avatar

**Endpoint:** `DELETE https://api.heygen.com/v2/photo_avatar/{id}`

```typescript
async function deletePhotoAvatar(id: string): Promise<void> {
  const response = await fetch(
    `https://api.heygen.com/v2/photo_avatar/${id}`,
    {
      method: "DELETE",
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to delete photo avatar");
  }
}
```

### Delete Photo Avatar Group

**Endpoint:** `DELETE https://api.heygen.com/v2/photo_avatar_group/{group_id}`

```typescript
async function deletePhotoAvatarGroup(groupId: string): Promise<void> {
  const response = await fetch(
    `https://api.heygen.com/v2/photo_avatar_group/${groupId}`,
    {
      method: "DELETE",
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to delete photo avatar group");
  }
}
```

## Photo Requirements

### Technical Requirements

| Aspect | Requirement |
|--------|-------------|
| Format | JPEG, PNG |
| Resolution | Minimum 512x512px |
| File size | Under 10MB |
| Face visibility | Clear, front-facing |

### Quality Guidelines

1. **Lighting** - Even, natural lighting on face
2. **Expression** - Neutral or slight smile
3. **Background** - Simple, uncluttered
4. **Face position** - Centered, not cut off
5. **Clarity** - Sharp, in focus
6. **Angle** - Straight-on or slight angle

## Best Practices

1. **Use `POST /v3/videos` with `"type": "image"` for the best quality** - This is the recommended path and automatically uses Avatar IV technology
2. **Use `"image": { "type": "asset_id", ... }` for private images** - Upload first via `POST upload.heygen.com/v1/asset`, then pass the asset ID in the `image` field
3. **Use high-quality photos** - Better input = better output
4. **Front-facing portraits work best** - Clear face visibility produces the most natural animation
5. **Use `motion_prompt` for natural movement** - Describe the body language you want (e.g., "nodding and gesturing")
6. **Start with `expressiveness: "low"`** - Increase to `"medium"` or `"high"` only if you want more energetic movement
7. **Avoid the legacy avatar group workflow** - The direct `"type": "image"` approach is simpler and produces equivalent or better results

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v3/videos` | POST | **Recommended** - Create video from photo with `"type": "image"` and nested `image` AssetInput |
| `/v3/videos/{video_id}` | GET | Poll video generation status |
| `upload.heygen.com/v1/asset` | POST | Upload image (returns asset `id` and `image_key`) |
| `/v2/photo_avatar/photo/generate` | POST | Generate AI photo from text description |
| `/v2/photo_avatar/generation/{id}` | GET | Check AI photo generation status |
| `/v2/photo_avatar/{id}` | GET | Get photo avatar details/status |
| `/v2/photo_avatar/{id}` | DELETE | Delete photo avatar |
| `/v2/photo_avatar_group/{id}` | DELETE | Delete avatar group |
| `/v2/photo_avatar/avatar_group/create` | POST | Legacy: Create photo avatar group from `image_key` |
| `/v2/photo_avatar/avatar_group/add` | POST | Legacy: Add photos to existing group |
| `/v2/photo_avatar/train` | POST | Legacy: Train avatar group |
| `/v2/photo_avatar/train/status/{group_id}` | GET | Legacy: Check training status |

## Limitations

- Photo quality significantly affects output
- Side-profile photos have limited support
- Full-body photos may not animate properly
- Some expressions may look unnatural
- Processing time varies by complexity
