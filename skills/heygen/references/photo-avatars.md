---
name: photo-avatars
description: Creating avatars from photos (talking photos) for HeyGen
---

# Photo Avatars (Talking Photos)

Photo avatars allow you to animate a static photo and make it speak. This is useful for creating personalized video content from portraits, headshots, or any suitable image.

## Creating a Photo Avatar from an Uploaded Image

The workflow is: **Upload Image → Create Avatar Group → Use in Video**

### Step 1: Upload the Image

Upload a portrait photo using the asset upload endpoint. The response includes an `image_key` which you'll use in the next step.

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

> **Important:** Save the `image_key` field (not the `id`). The `image_key` is the S3 path used to create the photo avatar.

See [assets.md](assets.md) for full upload details.

### Step 2: Create Photo Avatar Group

Use the `image_key` from the upload response to create a photo avatar group. This processes the image and creates a usable photo avatar.

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
| `generation_id` | string | | If using AI-generated photo (see below) |

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

The `id` (same as `group_id`) is your `talking_photo_id` for video generation.

### Step 3: Wait for Processing

The photo avatar starts with `status: "pending"` and transitions to `"completed"` within seconds. Poll the status endpoint:

**Endpoint:** `GET https://api.heygen.com/v2/photo_avatar/{id}`

```bash
curl "https://api.heygen.com/v2/photo_avatar/045c260bc0364727b2cbe50442c3a5bf" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Wait until `status` is `"completed"` before using in video generation.

### Step 4: Use in Video Generation

Use the photo avatar `id` as `talking_photo_id`:

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "talking_photo",
        talking_photo_id: "045c260bc0364727b2cbe50442c3a5bf",
      },
      voice: {
        type: "text",
        input_text: "Hello! This is my photo avatar speaking.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
  dimension: { width: 1920, height: 1080 },
};
```

## TypeScript: Complete Workflow

```typescript
import fs from "fs";

interface AssetUploadResponse {
  code: number;
  data: {
    id: string;
    image_key: string;
    url: string;
  };
}

interface PhotoAvatarResponse {
  error: string | null;
  data: {
    id: string;
    group_id: string;
    image_url: string;
    name: string;
    status: string;
    is_motion: boolean;
    business_type: string;
  };
}

async function createPhotoAvatar(
  imagePath: string,
  name: string
): Promise<string> {
  // 1. Upload image
  const fileBuffer = fs.readFileSync(imagePath);
  const uploadResponse = await fetch("https://upload.heygen.com/v1/asset", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "image/jpeg",
    },
    body: fileBuffer,
  });

  const uploadJson: AssetUploadResponse = await uploadResponse.json();
  if (uploadJson.code !== 100) {
    throw new Error("Upload failed");
  }

  const imageKey = uploadJson.data.image_key;

  // 2. Create avatar group
  const createResponse = await fetch(
    "https://api.heygen.com/v2/photo_avatar/avatar_group/create",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image_key: imageKey, name }),
    }
  );

  const createJson: PhotoAvatarResponse = await createResponse.json();
  if (createJson.error) {
    throw new Error(createJson.error);
  }

  const photoAvatarId = createJson.data.id;

  // 3. Wait for processing
  await waitForPhotoAvatar(photoAvatarId);

  return photoAvatarId;
}

async function waitForPhotoAvatar(id: string): Promise<void> {
  for (let i = 0; i < 30; i++) {
    const response = await fetch(
      `https://api.heygen.com/v2/photo_avatar/${id}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );

    const json: PhotoAvatarResponse = await response.json();

    if (json.data.status === "completed") return;
    if (json.data.status === "failed") {
      throw new Error("Photo avatar processing failed");
    }

    await new Promise((r) => setTimeout(r, 2000));
  }

  throw new Error("Photo avatar processing timed out");
}

async function createVideoFromPhoto(
  photoPath: string,
  script: string,
  voiceId: string
): Promise<string> {
  // 1. Create photo avatar
  const talkingPhotoId = await createPhotoAvatar(photoPath, "Video Avatar");

  // 2. Generate video
  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_inputs: [
        {
          character: {
            type: "talking_photo",
            talking_photo_id: talkingPhotoId,
          },
          voice: {
            type: "text",
            input_text: script,
            voice_id: voiceId,
          },
        },
      ],
      dimension: { width: 1920, height: 1080 },
    }),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

## Python: Complete Workflow

```python
import requests
import os
import time

def create_photo_avatar(image_path: str, name: str) -> str:
    api_key = os.environ["HEYGEN_API_KEY"]

    # 1. Upload image
    with open(image_path, "rb") as f:
        upload_resp = requests.post(
            "https://upload.heygen.com/v1/asset",
            headers={
                "X-Api-Key": api_key,
                "Content-Type": "image/jpeg",
            },
            data=f,
        )

    upload_data = upload_resp.json()
    if upload_data.get("code") != 100:
        raise Exception("Upload failed")

    image_key = upload_data["data"]["image_key"]

    # 2. Create avatar group
    create_resp = requests.post(
        "https://api.heygen.com/v2/photo_avatar/avatar_group/create",
        headers={
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
        },
        json={"image_key": image_key, "name": name},
    )

    create_data = create_resp.json()
    if create_data.get("error"):
        raise Exception(create_data["error"])

    photo_avatar_id = create_data["data"]["id"]

    # 3. Wait for processing
    for _ in range(30):
        status_resp = requests.get(
            f"https://api.heygen.com/v2/photo_avatar/{photo_avatar_id}",
            headers={"X-Api-Key": api_key},
        )
        status = status_resp.json()["data"]["status"]
        if status == "completed":
            return photo_avatar_id
        if status == "failed":
            raise Exception("Photo avatar processing failed")
        time.sleep(2)

    raise Exception("Photo avatar processing timed out")
```

## Listing Existing Talking Photos

Retrieve all talking photos in your account:

**Endpoint:** `GET https://api.heygen.com/v1/talking_photo.list`

```bash
curl "https://api.heygen.com/v1/talking_photo.list" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Response:
```json
{
  "code": 100,
  "data": [
    {
      "id": "ef0ed70f72c6497793e5e36e434d2aea",
      "image_url": "https://files2.heygen.ai/talking_photo/.../image.WEBP",
      "circle_image": ""
    }
  ]
}
```

Each `id` can be used as `talking_photo_id` in video generation.

## Adding Photos to an Existing Group

Add additional photo looks to an existing avatar group:

**Endpoint:** `POST https://api.heygen.com/v2/photo_avatar/avatar_group/add`

```typescript
async function addPhotosToGroup(
  groupId: string,
  imageKeys: string[],
  name: string
): Promise<void> {
  const response = await fetch(
    "https://api.heygen.com/v2/photo_avatar/avatar_group/add",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        group_id: groupId,
        image_keys: imageKeys,
        name,
      }),
    }
  );

  const json = await response.json();
  if (json.error) {
    throw new Error(json.error);
  }
}
```

## Training a Photo Avatar Group

Train the avatar group for improved animation quality:

**Endpoint:** `POST https://api.heygen.com/v2/photo_avatar/train`

```bash
curl -X POST "https://api.heygen.com/v2/photo_avatar/train" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_id": "045c260bc0364727b2cbe50442c3a5bf"}'
```

Check training status:

**Endpoint:** `GET https://api.heygen.com/v2/photo_avatar/train/status/{group_id}`

## Avatar IV Video Generation

Avatar IV is HeyGen's latest photo avatar technology with improved quality and natural motion. It generates a video directly from an uploaded image, bypassing the avatar group creation step.

**Endpoint:** `POST https://api.heygen.com/v2/video/av4/generate`

```bash
curl -X POST "https://api.heygen.com/v2/video/av4/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_key": "image/741299e941764988b432ed3a6757878f/original.jpg",
    "script": "Hello! This is Avatar IV with enhanced quality.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "video_orientation": "landscape",
    "video_title": "My Avatar IV Video"
  }'
```

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `image_key` | string | ✓ | S3 image key from asset upload |
| `script` | string | ✓ | Text for the avatar to speak |
| `voice_id` | string | ✓ | Voice to use |
| `video_orientation` | string | | `"portrait"`, `"landscape"`, or `"square"` |
| `video_title` | string | | Title for the video |
| `fit` | string | | `"cover"` or `"contain"` |
| `custom_motion_prompt` | string | | Motion/expression description |
| `enhance_custom_motion_prompt` | boolean | | Enhance the motion prompt with AI |

### TypeScript

```typescript
interface AvatarIVRequest {
  image_key: string;
  script: string;
  voice_id: string;
  video_orientation?: "portrait" | "landscape" | "square";
  video_title?: string;
  fit?: "cover" | "contain";
  custom_motion_prompt?: string;
  enhance_custom_motion_prompt?: boolean;
}

interface AvatarIVResponse {
  error: null | string;
  data: {
    video_id: string;
  };
}

async function generateAvatarIVVideo(
  config: AvatarIVRequest
): Promise<string> {
  const response = await fetch(
    "https://api.heygen.com/v2/video/av4/generate",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    }
  );

  const json: AvatarIVResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.video_id;
}
```

### Avatar IV Options

| Orientation | Dimensions | Use Case |
|-------------|------------|----------|
| `portrait` | 720x1280 | TikTok, Stories |
| `landscape` | 1280x720 | YouTube, Web |
| `square` | 720x720 | Instagram Feed |

| Fit | Description |
|-----|-------------|
| `cover` | Fill the frame, may crop edges |
| `contain` | Fit entire image, may show background |

### Custom Motion Prompts

```typescript
const videoId = await generateAvatarIVVideo({
  image_key: "image/.../original.jpg",
  script: "Let me tell you about our product.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  custom_motion_prompt: "nodding head and smiling",
  enhance_custom_motion_prompt: true,
});
```

## Generating AI Photo Avatars

Generate synthetic photo avatars from text descriptions instead of uploading a photo.

**Endpoint:** `POST https://api.heygen.com/v2/photo_avatar/photo/generate`

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

### TypeScript

```typescript
interface GeneratePhotoAvatarRequest {
  name: string;
  age: "Young Adult" | "Early Middle Age" | "Late Middle Age" | "Senior" | "Unspecified";
  gender: "Woman" | "Man" | "Unspecified";
  ethnicity: "White" | "Black" | "Asian American" | "East Asian" | "South East Asian" | "South Asian" | "Middle Eastern" | "Pacific" | "Hispanic" | "Unspecified";
  orientation: "square" | "horizontal" | "vertical";
  pose: "half_body" | "close_up" | "full_body";
  style: "Realistic" | "Pixar" | "Cinematic" | "Vintage" | "Noir" | "Cyberpunk" | "Unspecified";
  appearance: string;
}

interface GeneratePhotoAvatarResponse {
  error: string | null;
  data: {
    generation_id: string;
  };
}

interface PhotoGenerationStatus {
  error: string | null;
  data: {
    id: string;
    status: "pending" | "processing" | "success" | "failed";
    msg: string | null;
    image_url_list?: string[];
    image_key_list?: string[];
  };
}

async function generatePhotoAvatar(
  config: GeneratePhotoAvatarRequest
): Promise<string> {
  const response = await fetch(
    "https://api.heygen.com/v2/photo_avatar/photo/generate",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    }
  );

  const json: GeneratePhotoAvatarResponse = await response.json();

  if (json.error) {
    throw new Error(`Photo avatar generation failed: ${json.error}`);
  }

  return json.data.generation_id;
}

async function waitForPhotoGeneration(
  generationId: string
): Promise<string[]> {
  for (let i = 0; i < 60; i++) {
    const response = await fetch(
      `https://api.heygen.com/v2/photo_avatar/generation/${generationId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );

    const json: PhotoGenerationStatus = await response.json();

    if (json.error) throw new Error(json.error);

    if (json.data.status === "success") {
      return json.data.image_key_list!;
    }

    if (json.data.status === "failed") {
      throw new Error(json.data.msg ?? "Photo generation failed");
    }

    await new Promise((r) => setTimeout(r, 5000));
  }

  throw new Error("Photo generation timed out");
}
```

### AI Photo → Avatar Group → Video

Use a generated AI photo to create an avatar group, then generate a video:

```typescript
// 1. Generate AI photo
const generationId = await generatePhotoAvatar({
  name: "Product Demo Host",
  age: "Young Adult",
  gender: "Woman",
  ethnicity: "Unspecified",
  orientation: "horizontal",
  pose: "half_body",
  style: "Realistic",
  appearance: "Professional woman, navy blazer, friendly smile, soft lighting",
});

// 2. Wait for generation and pick first result
const imageKeys = await waitForPhotoGeneration(generationId);
const selectedImageKey = imageKeys[0];

// 3. Create avatar group from the AI photo
const createResponse = await fetch(
  "https://api.heygen.com/v2/photo_avatar/avatar_group/create",
  {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      image_key: selectedImageKey,
      name: "Product Demo Host",
      generation_id: generationId,
    }),
  }
);

const { data } = await createResponse.json();
const talkingPhotoId = data.id;

// 4. Generate video (after status is "completed")
const videoId = await generateVideo({
  video_inputs: [{
    character: {
      type: "talking_photo",
      talking_photo_id: talkingPhotoId,
    },
    voice: {
      type: "text",
      input_text: "Welcome to our product demo!",
      voice_id: "1bd001e7e50f421d891986aad5158bc8",
    },
  }],
  dimension: { width: 1920, height: 1080 },
});
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

## Managing Photo Avatars

### Get Photo Avatar Details

**Endpoint:** `GET https://api.heygen.com/v2/photo_avatar/{id}`

```typescript
async function getPhotoAvatar(id: string): Promise<PhotoAvatarResponse> {
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

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `upload.heygen.com/v1/asset` | POST | Upload image (returns `image_key`) |
| `/v2/photo_avatar/avatar_group/create` | POST | Create photo avatar from `image_key` |
| `/v2/photo_avatar/avatar_group/add` | POST | Add photos to existing group |
| `/v2/photo_avatar/train` | POST | Train avatar group |
| `/v2/photo_avatar/train/status/{group_id}` | GET | Check training status |
| `/v2/photo_avatar/{id}` | GET | Get photo avatar details/status |
| `/v2/photo_avatar/{id}` | DELETE | Delete photo avatar |
| `/v2/photo_avatar_group/{id}` | DELETE | Delete avatar group |
| `/v2/photo_avatar/photo/generate` | POST | Generate AI photo from text |
| `/v2/photo_avatar/generation/{id}` | GET | Check AI generation status |
| `/v2/video/av4/generate` | POST | Avatar IV video from `image_key` |
| `/v1/talking_photo.list` | GET | List all existing talking photos |
| `/v2/video/generate` | POST | Generate video with `talking_photo_id` |

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

1. **Use high-quality photos** - Better input = better output
2. **Front-facing portraits** - Work best for animation
3. **Neutral expressions** - Allow for more natural animation
4. **Use Avatar IV for best quality** - Latest generation technology
5. **Train avatar groups** - Improves animation quality
6. **Reuse photo avatar IDs** - Once created, use the same `talking_photo_id` across multiple videos

## Limitations

- Photo quality significantly affects output
- Side-profile photos have limited support
- Full-body photos may not animate properly
- Some expressions may look unnatural
- Processing time varies by complexity
