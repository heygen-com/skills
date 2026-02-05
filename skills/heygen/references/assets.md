---
name: assets
description: Uploading images, videos, and audio for use in HeyGen video generation
---

# Asset Upload and Management

HeyGen allows you to upload custom assets (images, videos, audio) for use in video generation, such as backgrounds, talking photo sources, and custom audio.

## Upload Flow

Asset uploads are a single-step process: POST the raw file binary directly to the upload endpoint. The Content-Type header must match the file's MIME type.

## Uploading an Asset

**Endpoint:** `POST https://upload.heygen.com/v1/asset`

### Request

| Header | Required | Description |
|--------|:--------:|-------------|
| `X-Api-Key` | ✓ | Your HeyGen API key |
| `Content-Type` | ✓ | MIME type of the file (e.g. `image/jpeg`) |

The request body is the raw binary file data. No JSON or form fields are needed.

### Response

| Field | Type | Description |
|-------|------|-------------|
| `code` | number | Status code (`100` = success) |
| `data.id` | string | Unique asset ID for use in video generation |
| `data.name` | string | Asset name |
| `data.file_type` | string | `image`, `video`, or `audio` |
| `data.url` | string | Accessible URL for the uploaded file |
| `data.image_key` | string \| null | Key for creating uploaded photo avatars (images only) |
| `data.folder_id` | string | Folder ID (empty if not in a folder) |
| `data.meta` | string \| null | Asset metadata |
| `data.created_ts` | number | Unix timestamp of creation |

### curl

```bash
curl -X POST "https://upload.heygen.com/v1/asset" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: image/jpeg" \
  --data-binary '@./background.jpg'
```

### TypeScript

```typescript
import fs from "fs";

interface AssetUploadResponse {
  code: number;
  data: {
    id: string;
    name: string;
    file_type: string;
    url: string;
    image_key: string | null;
    folder_id: string;
    meta: string | null;
    created_ts: number;
  };
  msg: string | null;
  message: string | null;
}

async function uploadAsset(filePath: string, contentType: string): Promise<AssetUploadResponse["data"]> {
  const fileBuffer = fs.readFileSync(filePath);

  const response = await fetch("https://upload.heygen.com/v1/asset", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": contentType,
    },
    body: fileBuffer,
  });

  const json: AssetUploadResponse = await response.json();

  if (json.code !== 100) {
    throw new Error(json.message ?? "Upload failed");
  }

  return json.data;
}

// Usage
const asset = await uploadAsset("./background.jpg", "image/jpeg");
console.log(`Uploaded asset: ${asset.id}`);
console.log(`Asset URL: ${asset.url}`);
```

### TypeScript (with streams for large files)

```typescript
import fs from "fs";
import { stat } from "fs/promises";

async function uploadLargeAsset(filePath: string, contentType: string): Promise<AssetUploadResponse["data"]> {
  const fileStats = await stat(filePath);
  const fileStream = fs.createReadStream(filePath);

  const response = await fetch("https://upload.heygen.com/v1/asset", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": contentType,
      "Content-Length": fileStats.size.toString(),
    },
    body: fileStream as any,
    // @ts-ignore - duplex is needed for streaming
    duplex: "half",
  });

  const json: AssetUploadResponse = await response.json();

  if (json.code !== 100) {
    throw new Error(json.message ?? "Upload failed");
  }

  return json.data;
}
```

### Python

```python
import requests
import os

def upload_asset(file_path: str, content_type: str) -> dict:
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://upload.heygen.com/v1/asset",
            headers={
                "X-Api-Key": os.environ["HEYGEN_API_KEY"],
                "Content-Type": content_type
            },
            data=f
        )

    data = response.json()
    if data.get("code") != 100:
        raise Exception(data.get("message", "Upload failed"))

    return data["data"]


# Usage
asset = upload_asset("./background.jpg", "image/jpeg")
print(f"Uploaded asset: {asset['id']}")
print(f"Asset URL: {asset['url']}")
```

## Supported Content Types

| Type | Content-Type | Use Case |
|------|--------------|----------|
| JPEG | `image/jpeg` | Backgrounds, talking photos |
| PNG | `image/png` | Backgrounds, overlays |
| MP4 | `video/mp4` | Video backgrounds |
| WebM | `video/webm` | Video backgrounds |
| MP3 | `audio/mpeg` | Custom audio input |
| WAV | `audio/wav` | Custom audio input |

## Uploading from URL

If your asset is already hosted online:

```typescript
async function uploadFromUrl(sourceUrl: string, contentType: string): Promise<AssetUploadResponse["data"]> {
  // 1. Download the file
  const sourceResponse = await fetch(sourceUrl);
  const buffer = Buffer.from(await sourceResponse.arrayBuffer());

  // 2. Upload directly to HeyGen
  const response = await fetch("https://upload.heygen.com/v1/asset", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": contentType,
    },
    body: buffer,
  });

  const json: AssetUploadResponse = await response.json();

  if (json.code !== 100) {
    throw new Error(json.message ?? "Upload failed");
  }

  return json.data;
}
```

## Using Uploaded Assets

### As Background Image

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hello, this is a video with a custom background!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: asset.url,  // Use the URL from the upload response
      },
    },
  ],
};
```

### As Talking Photo Source

```typescript
const talkingPhotoConfig = {
  video_inputs: [
    {
      character: {
        type: "talking_photo",
        talking_photo_id: asset.id,  // Use the ID from the upload response
      },
      voice: {
        type: "text",
        input_text: "Hello from my talking photo!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### As Audio Input

```typescript
const audioConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "audio",
        audio_url: asset.url,  // Use the URL from the upload response
      },
    },
  ],
};
```

## Complete Upload Workflow

```typescript
async function createVideoWithCustomBackground(
  backgroundPath: string,
  script: string
): Promise<string> {
  // 1. Upload background
  console.log("Uploading background...");
  const background = await uploadAsset(backgroundPath, "image/jpeg");

  // 2. Create video config
  const config = {
    video_inputs: [
      {
        character: {
          type: "avatar",
          avatar_id: "josh_lite3_20230714",
          avatar_style: "normal",
        },
        voice: {
          type: "text",
          input_text: script,
          voice_id: "1bd001e7e50f421d891986aad5158bc8",
        },
        background: {
          type: "image",
          url: background.url,
        },
      },
    ],
    dimension: { width: 1920, height: 1080 },
  };

  // 3. Generate video
  console.log("Generating video...");
  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

## Asset Limitations

- **File size**: 10MB maximum
- **Image dimensions**: Recommended to match video dimensions
- **Audio duration**: Should match expected video length
- **Retention**: Assets may be deleted after a period of inactivity

## Best Practices

1. **Optimize images** - Resize to match video dimensions before uploading
2. **Use appropriate formats** - JPEG for photos, PNG for graphics with transparency
3. **Validate before upload** - Check file type and size locally first
4. **Handle upload errors** - Implement retry logic for failed uploads
5. **Cache asset IDs** - Reuse assets across multiple video generations
