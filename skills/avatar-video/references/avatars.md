---
name: avatars
description: Listing avatar groups and looks, filtering by type and ownership, and selecting the right avatar_id for video generation using the v3 API
---

# HeyGen Avatars

The v3 API organizes avatars into two levels:

- **Groups** represent a character (e.g., "Josh", "Angela"). A group has a name, preview images, and a default voice.
- **Looks** represent a specific outfit, style, or pose within a group. Each look has an `id` that you pass as `avatar_id` when creating a video via `POST /v3/videos`.

A single group can have multiple looks. For example, the "Josh" group might have looks for business attire, casual wear, and seasonal outfits.

## Previewing Avatars Before Generation

Always preview avatars before generating a video to ensure they match user preferences. Both groups and looks include preview URLs that can be opened directly in the browser.

### Preview Fields

| Level | Field | Description |
|-------|-------|-------------|
| Group | `preview_image_url` | Static image of the character (publicly accessible) |
| Group | `preview_video_url` | Short video clip showing the character |
| Look | `preview_image_url` | Static image of this specific look/outfit |
| Look | `preview_video_url` | Short video clip of this look in action |

Both URLs are publicly accessible -- no authentication needed to view them.

### Workflow: Preview Before Generate

1. **List avatar groups** -- browse available characters
2. **List looks for a group** -- see available outfits/styles
3. **Show preview URLs to user** -- share `preview_image_url` for visual check
4. **User selects** a look by name or ID
5. **Use `look.id` as `avatar_id`** and `look.default_voice_id` as `voice_id` in `POST /v3/videos`

## Listing Avatar Groups

List all avatar groups (characters) available to your account.

### curl

```bash
# List public avatar groups
curl -X GET "https://api.heygen.com/v3/avatars?ownership=public&limit=10" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# List your private avatar groups
curl -X GET "https://api.heygen.com/v3/avatars?ownership=private&limit=10" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface AvatarGroupItem {
  id: string;
  name: string;
  preview_image_url: string | null;
  preview_video_url: string | null;
  gender: string | null;
  created_at: number;
  looks_count: number;
  default_voice_id: string | null;
}

interface AvatarGroupsResponse {
  data: AvatarGroupItem[];
  has_more: boolean;
  next_token: string | null;
}

async function listAvatarGroups(
  ownership: "public" | "private" = "public",
  limit: number = 50,
  token?: string
): Promise<AvatarGroupsResponse> {
  const params = new URLSearchParams({
    ownership,
    limit: limit.toString(),
  });
  if (token) {
    params.set("token", token);
  }

  const response = await fetch(
    `https://api.heygen.com/v3/avatars?${params}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  if (!response.ok) {
    throw new Error(`Failed to list avatar groups: ${response.status}`);
  }

  return response.json();
}

// Usage
const { data: groups, has_more, next_token } = await listAvatarGroups("public", 10);
for (const group of groups) {
  console.log(`${group.name} (${group.gender}) - ${group.looks_count} looks`);
  console.log(`  ID: ${group.id}`);
  console.log(`  Preview: ${group.preview_image_url}`);
}
```

### Python

```python
import requests
import os


def list_avatar_groups(
    ownership: str = "public",
    limit: int = 50,
    token: str | None = None,
) -> dict:
    params = {"ownership": ownership, "limit": limit}
    if token:
        params["token"] = token

    response = requests.get(
        "https://api.heygen.com/v3/avatars",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        params=params,
    )
    response.raise_for_status()
    return response.json()


# Usage
result = list_avatar_groups("public", limit=10)
for group in result["data"]:
    print(f"{group['name']} ({group['gender']}) - {group['looks_count']} looks")
    print(f"  ID: {group['id']}")
    print(f"  Preview: {group['preview_image_url']}")
```

### Response Format

```json
{
  "data": [
    {
      "id": "ag_abc123",
      "name": "Josh",
      "preview_image_url": "https://files.heygen.ai/...",
      "preview_video_url": "https://files.heygen.ai/...",
      "gender": "male",
      "created_at": 1710000000,
      "looks_count": 3,
      "default_voice_id": "1bd001e7e50f421d891986aad5158bc8"
    },
    {
      "id": "ag_def456",
      "name": "Angela",
      "preview_image_url": "https://files.heygen.ai/...",
      "preview_video_url": "https://files.heygen.ai/...",
      "gender": "female",
      "created_at": 1710100000,
      "looks_count": 2,
      "default_voice_id": "2d5b0e6a8c3f47d9a1b2c3d4e5f60718"
    }
  ],
  "has_more": true,
  "next_token": "eyJsYXN0X2lkIjoiYWdfZGVmNDU2In0="
}
```

## Get Avatar Group Details

Retrieve details for a single avatar group by its ID.

### curl

```bash
curl -X GET "https://api.heygen.com/v3/avatars/ag_abc123" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
async function getAvatarGroup(groupId: string): Promise<AvatarGroupItem> {
  const response = await fetch(
    `https://api.heygen.com/v3/avatars/${groupId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  if (!response.ok) {
    throw new Error(`Failed to get avatar group: ${response.status}`);
  }

  return response.json();
}
```

### Python

```python
def get_avatar_group(group_id: str) -> dict:
    response = requests.get(
        f"https://api.heygen.com/v3/avatars/{group_id}",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    )
    response.raise_for_status()
    return response.json()
```

## Listing Avatar Looks

Looks are the specific outfits, styles, or poses within a group. The look `id` is what you pass as `avatar_id` to `POST /v3/videos`.

### curl

```bash
# List all public looks
curl -X GET "https://api.heygen.com/v3/avatars/looks?ownership=public&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# List looks for a specific group
curl -X GET "https://api.heygen.com/v3/avatars/looks?group_id=ag_abc123&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# List only studio avatars
curl -X GET "https://api.heygen.com/v3/avatars/looks?avatar_type=studio_avatar&ownership=public&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_id` | string | No | Filter looks by avatar group |
| `avatar_type` | string | No | `"studio_avatar"`, `"video_avatar"`, or `"photo_avatar"` |
| `ownership` | string | No | `"public"` or `"private"` |
| `limit` | integer | No | 1-50, number of results per page |
| `token` | string | No | Cursor token for pagination |

### TypeScript

```typescript
interface AvatarLookItem {
  id: string;
  name: string;
  avatar_type: "studio_avatar" | "video_avatar" | "photo_avatar";
  group_id: string | null;
  preview_image_url: string | null;
  preview_video_url: string | null;
  gender: string | null;
  tags: string[];
  default_voice_id: string | null;
  supported_api_engines: string[];
}

interface AvatarLooksResponse {
  data: AvatarLookItem[];
  has_more: boolean;
  next_token: string | null;
}

async function listAvatarLooks(options: {
  group_id?: string;
  avatar_type?: "studio_avatar" | "video_avatar" | "photo_avatar";
  ownership?: "public" | "private";
  limit?: number;
  token?: string;
} = {}): Promise<AvatarLooksResponse> {
  const params = new URLSearchParams();

  if (options.group_id) params.set("group_id", options.group_id);
  if (options.avatar_type) params.set("avatar_type", options.avatar_type);
  if (options.ownership) params.set("ownership", options.ownership);
  if (options.limit) params.set("limit", options.limit.toString());
  if (options.token) params.set("token", options.token);

  const response = await fetch(
    `https://api.heygen.com/v3/avatars/looks?${params}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  if (!response.ok) {
    throw new Error(`Failed to list avatar looks: ${response.status}`);
  }

  return response.json();
}

// List all public looks
const { data: looks } = await listAvatarLooks({ ownership: "public", limit: 20 });

// List looks for a specific group
const { data: groupLooks } = await listAvatarLooks({ group_id: "ag_abc123" });

// List only studio avatars
const { data: studioLooks } = await listAvatarLooks({
  avatar_type: "studio_avatar",
  ownership: "public",
});
```

### Python

```python
def list_avatar_looks(
    group_id: str | None = None,
    avatar_type: str | None = None,
    ownership: str | None = None,
    limit: int = 50,
    token: str | None = None,
) -> dict:
    params: dict = {"limit": limit}
    if group_id:
        params["group_id"] = group_id
    if avatar_type:
        params["avatar_type"] = avatar_type
    if ownership:
        params["ownership"] = ownership
    if token:
        params["token"] = token

    response = requests.get(
        "https://api.heygen.com/v3/avatars/looks",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        params=params,
    )
    response.raise_for_status()
    return response.json()


# List all public looks
result = list_avatar_looks(ownership="public", limit=20)
for look in result["data"]:
    print(f"{look['name']} ({look['avatar_type']}) - ID: {look['id']}")

# List looks for a specific group
result = list_avatar_looks(group_id="ag_abc123")

# List only studio avatars
result = list_avatar_looks(avatar_type="studio_avatar", ownership="public")
```

### Response Format

```json
{
  "data": [
    {
      "id": "lk_josh_business",
      "name": "Josh - Business",
      "avatar_type": "studio_avatar",
      "group_id": "ag_abc123",
      "preview_image_url": "https://files.heygen.ai/...",
      "preview_video_url": "https://files.heygen.ai/...",
      "gender": "male",
      "tags": ["business", "professional"],
      "default_voice_id": "1bd001e7e50f421d891986aad5158bc8",
      "supported_api_engines": ["avatar_4_quality", "avatar_4_turbo"]
    },
    {
      "id": "lk_josh_casual",
      "name": "Josh - Casual",
      "avatar_type": "studio_avatar",
      "group_id": "ag_abc123",
      "preview_image_url": "https://files.heygen.ai/...",
      "preview_video_url": "https://files.heygen.ai/...",
      "gender": "male",
      "tags": ["casual", "lifestyle"],
      "default_voice_id": "1bd001e7e50f421d891986aad5158bc8",
      "supported_api_engines": ["avatar_4_quality", "avatar_4_turbo"]
    }
  ],
  "has_more": false,
  "next_token": null
}
```

## Get Look Details

Retrieve details for a single look by its ID.

### curl

```bash
curl -X GET "https://api.heygen.com/v3/avatars/looks/lk_josh_business" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
async function getAvatarLook(lookId: string): Promise<AvatarLookItem> {
  const response = await fetch(
    `https://api.heygen.com/v3/avatars/looks/${lookId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  if (!response.ok) {
    throw new Error(`Failed to get avatar look: ${response.status}`);
  }

  return response.json();
}

// Usage
const look = await getAvatarLook("lk_josh_business");
console.log(`${look.name} (${look.avatar_type})`);
console.log(`Engines: ${look.supported_api_engines.join(", ")}`);
console.log(`Default voice: ${look.default_voice_id}`);
```

### Python

```python
def get_avatar_look(look_id: str) -> dict:
    response = requests.get(
        f"https://api.heygen.com/v3/avatars/looks/{look_id}",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    )
    response.raise_for_status()
    return response.json()


# Usage
look = get_avatar_look("lk_josh_business")
print(f"{look['name']} ({look['avatar_type']})")
print(f"Engines: {', '.join(look['supported_api_engines'])}")
print(f"Default voice: {look['default_voice_id']}")
```

## Avatar Types

The `avatar_type` field on looks distinguishes three categories:

| Type | Description | Best For |
|------|-------------|----------|
| `studio_avatar` | Professionally produced studio-quality avatars | Corporate videos, product demos, training content |
| `video_avatar` | Avatars trained from uploaded video footage | Custom brand representatives, personalized content |
| `photo_avatar` | Avatars generated from a still photo | Quick prototyping, low-effort personalization |

### Filtering by Type

```typescript
// Get only studio avatars (highest quality)
const { data: studioLooks } = await listAvatarLooks({
  avatar_type: "studio_avatar",
  ownership: "public",
});

// Get only photo avatars (from uploaded photos)
const { data: photoLooks } = await listAvatarLooks({
  avatar_type: "photo_avatar",
  ownership: "private",
});
```

```python
# Get only video avatars (trained from video footage)
result = list_avatar_looks(avatar_type="video_avatar", ownership="private")
```

## Using Avatar's Default Voice

Each look has a `default_voice_id` that is pre-matched for natural results. This is the recommended approach rather than manually selecting voices.

### Recommended Flow

```
1. GET /v3/avatars/looks      -> Pick a look
2. Use look.id as avatar_id   -> Pass to POST /v3/videos
3. Use look.default_voice_id  -> Pass as voice_id to POST /v3/videos
```

### Complete Example: Generate Video with a Look's Default Voice

#### TypeScript

```typescript
async function generateWithDefaultVoice(
  lookId: string,
  script: string
): Promise<string> {
  // 1. Get look details to find default voice
  const look = await getAvatarLook(lookId);

  if (!look.default_voice_id) {
    throw new Error(`Look ${look.name} has no default voice`);
  }

  console.log(`Using ${look.name} with default voice: ${look.default_voice_id}`);

  // 2. Generate video with the look's default voice
  const response = await fetch("https://api.heygen.com/v3/videos", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_inputs: [{
        character: {
          type: "avatar",
          avatar_id: look.id,       // The look ID is the avatar_id
          avatar_style: "normal",
        },
        voice: {
          type: "text",
          input_text: script,
          voice_id: look.default_voice_id,
        },
      }],
      dimension: { width: 1920, height: 1080 },
    }),
  });

  if (!response.ok) {
    throw new Error(`Video generation failed: ${response.status}`);
  }

  const { data } = await response.json();
  return data.video_id;
}
```

#### Python

```python
def generate_with_default_voice(look_id: str, script: str) -> str:
    # 1. Get look details to find default voice
    look = get_avatar_look(look_id)

    if not look.get("default_voice_id"):
        raise ValueError(f"Look {look['name']} has no default voice")

    print(f"Using {look['name']} with default voice: {look['default_voice_id']}")

    # 2. Generate video with the look's default voice
    response = requests.post(
        "https://api.heygen.com/v3/videos",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json={
            "video_inputs": [{
                "character": {
                    "type": "avatar",
                    "avatar_id": look["id"],       # The look ID is the avatar_id
                    "avatar_style": "normal",
                },
                "voice": {
                    "type": "text",
                    "input_text": script,
                    "voice_id": look["default_voice_id"],
                },
            }],
            "dimension": {"width": 1920, "height": 1080},
        },
    )
    response.raise_for_status()
    return response.json()["data"]["video_id"]
```

### Why Use Default Voice?

1. **Guaranteed gender match** -- avatar and voice are pre-paired
2. **Natural lip sync** -- default voices are optimized for the avatar
3. **Simpler code** -- no need to fetch and match voices separately
4. **Better quality** -- HeyGen has tested this combination

## Filtering and Searching

The v3 API supports server-side filtering across multiple dimensions.

### By Group

```typescript
// Get all looks for a specific character
const { data: looks } = await listAvatarLooks({ group_id: "ag_abc123" });
```

### By Avatar Type

```typescript
// Only studio-quality avatars
const { data: looks } = await listAvatarLooks({ avatar_type: "studio_avatar" });
```

### By Ownership

```typescript
// Public avatars provided by HeyGen
const { data: publicLooks } = await listAvatarLooks({ ownership: "public" });

// Your custom/private avatars
const { data: privateLooks } = await listAvatarLooks({ ownership: "private" });
```

### By Gender (Client-Side)

Gender is available on the response but not as a query parameter. Filter client-side:

```typescript
const { data: looks } = await listAvatarLooks({ ownership: "public" });
const femaleLooks = looks.filter((look) => look.gender === "female");
const maleLooks = looks.filter((look) => look.gender === "male");
```

```python
result = list_avatar_looks(ownership="public")
female_looks = [look for look in result["data"] if look["gender"] == "female"]
male_looks = [look for look in result["data"] if look["gender"] == "male"]
```

### Combining Filters

```typescript
// Private studio avatars for a specific group
const { data: looks } = await listAvatarLooks({
  group_id: "ag_abc123",
  avatar_type: "studio_avatar",
  ownership: "private",
  limit: 10,
});
```

### Search by Name (Client-Side)

```typescript
function searchLooksByName(looks: AvatarLookItem[], query: string): AvatarLookItem[] {
  const lowerQuery = query.toLowerCase();
  return looks.filter((look) =>
    look.name.toLowerCase().includes(lowerQuery)
  );
}

const { data: allLooks } = await listAvatarLooks({ ownership: "public" });
const results = searchLooksByName(allLooks, "josh");
```

## Cursor-Based Pagination

Both the groups and looks endpoints use cursor-based pagination. The response includes `has_more` (boolean) and `next_token` (string or null). Pass `next_token` as the `token` query parameter to fetch the next page.

### TypeScript

```typescript
async function listAllAvatarLooks(
  options: { ownership?: "public" | "private"; avatar_type?: string } = {}
): Promise<AvatarLookItem[]> {
  const allLooks: AvatarLookItem[] = [];
  let token: string | undefined;

  do {
    const response = await listAvatarLooks({
      ...options,
      limit: 50,
      token,
    });

    allLooks.push(...response.data);
    token = response.has_more && response.next_token
      ? response.next_token
      : undefined;
  } while (token);

  return allLooks;
}

// Fetch every public look across all pages
const allPublicLooks = await listAllAvatarLooks({ ownership: "public" });
console.log(`Total public looks: ${allPublicLooks.length}`);
```

### Python

```python
def list_all_avatar_looks(
    ownership: str | None = None,
    avatar_type: str | None = None,
) -> list[dict]:
    all_looks: list[dict] = []
    token: str | None = None

    while True:
        result = list_avatar_looks(
            ownership=ownership,
            avatar_type=avatar_type,
            limit=50,
            token=token,
        )

        all_looks.extend(result["data"])

        if not result["has_more"] or not result.get("next_token"):
            break
        token = result["next_token"]

    return all_looks


# Fetch every public look across all pages
all_public_looks = list_all_avatar_looks(ownership="public")
print(f"Total public looks: {len(all_public_looks)}")
```

### curl (Manual Pagination)

```bash
# First page
curl -X GET "https://api.heygen.com/v3/avatars/looks?ownership=public&limit=50" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# Next page (use next_token from previous response)
curl -X GET "https://api.heygen.com/v3/avatars/looks?ownership=public&limit=50&token=eyJsYXN0X2lkIjoiLi4uIn0=" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## Selecting the Right Avatar

### Avatar Categories

HeyGen avatars fall into distinct categories. Match the category to your use case:

| Category | Best For |
|----------|----------|
| **Business/Professional** | Corporate videos, product demos, training |
| **Casual/Friendly** | Social media, informal content |
| **Themed/Seasonal** | Specific campaigns, seasonal content |
| **Expressive** | Engaging storytelling, dynamic content |

### Selection Guidelines

**For business/professional content:**
- Choose looks with neutral attire (business casual or formal)
- Avoid themed or seasonal looks (holiday costumes, casual clothing)
- Preview the look to verify professional appearance
- Consider your audience demographics when selecting gender and appearance
- Prefer `studio_avatar` type for highest quality

**For casual/social content:**
- More flexibility in look choice
- Themed looks can work for specific campaigns
- Match avatar energy to content tone

### Common Mistakes to Avoid

1. **Using themed looks for business content** -- a holiday-themed look appears unprofessional in a product demo
2. **Not previewing before generation** -- always check the preview URL to verify appearance
3. **Mismatched voice gender** -- always use the look's `default_voice_id` or match genders manually
4. **Using a group ID instead of a look ID** -- `POST /v3/videos` requires a look `id`, not a group `id`

### Selection Checklist

Before generating a video:
- [ ] Previewed look image/video in browser
- [ ] Look appearance matches content tone (professional vs casual)
- [ ] Voice gender matches avatar gender
- [ ] Using `default_voice_id` when available
- [ ] Passing the look `id` (not the group `id`) as `avatar_id`
- [ ] Checked `supported_api_engines` if targeting a specific rendering engine

## Best Practices

1. **Always use look IDs for video generation.** The look `id` is the `avatar_id` you pass to `POST /v3/videos`. Group IDs are for browsing and organization only.
2. **Prefer `default_voice_id`.** Each look has a pre-matched voice. Use it unless the user explicitly requests a different voice.
3. **Preview before generating.** Share `preview_image_url` with the user to confirm the look matches their expectations.
4. **Use server-side filters.** Filter by `ownership`, `avatar_type`, and `group_id` at the API level rather than fetching everything and filtering client-side.
5. **Paginate large result sets.** Use `limit` and `token` to page through results. The maximum `limit` is 50.
6. **Check `supported_api_engines`.** Some looks support `avatar_4_quality` (higher quality, slower) and `avatar_4_turbo` (faster). Choose based on your latency and quality requirements.
7. **Cache group and look lists.** Avatar catalogs change infrequently. Cache the results for a reasonable period to reduce API calls.
