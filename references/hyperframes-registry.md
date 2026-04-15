# Registry — HyperFrames

Install and wire reusable blocks and components into HyperFrames compositions.

## Overview

The registry provides 50+ pre-built items installable via `npx hyperframes add <name>`.

- **Blocks** — standalone sub-compositions with own dimensions, duration, and timeline. Included via `data-composition-src`.
- **Components** — effect snippets (no own dimensions). Pasted directly into host composition HTML.

## Installing

```bash
npx hyperframes add data-chart              # install a block
npx hyperframes add grain-overlay           # install a component
npx hyperframes add shimmer-sweep --dir .   # target a specific project
npx hyperframes add data-chart --json       # machine-readable output
npx hyperframes add data-chart --no-clipboard  # skip clipboard (CI/headless)
```

After install, the CLI prints which files were written and a snippet to paste into your host composition.

**Note:** `hyperframes add` is for blocks and components only. For project templates, use `npx hyperframes init <dir> --example <name>`.

## Install Locations

Default paths (configurable in `hyperframes.json`):

| Type | Default path |
|------|-------------|
| Blocks | `compositions/<name>.html` |
| Components | `compositions/components/<name>.html` |
| Assets | `assets/` |

Configuration in `hyperframes.json`:
```json
{
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

## Wiring Blocks

Blocks are standalone compositions — include them via `data-composition-src` in your host `index.html`:

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Key attributes:

| Attribute | Purpose |
|-----------|---------|
| `data-composition-src` | Path to the block HTML file |
| `data-composition-id` | Must match the block's internal ID |
| `data-start` | When the block appears in the host timeline (seconds) |
| `data-duration` | How long the block plays |
| `data-width` / `data-height` | Block canvas dimensions |
| `data-track-index` | Layer ordering (higher = in front) |

## Wiring Components

Components are snippets — merge their content into your composition:

1. Read the installed file (e.g., `compositions/components/grain-overlay.html`)
2. Copy the HTML elements into your composition's `<div data-composition-id="...">`
3. Copy the `<style>` block into your composition's styles
4. Copy any `<script>` content into your script (before timeline code)
5. If the component exposes GSAP timeline integration, add those calls to your timeline

## Discovery

Browse available items:

```bash
# Read the registry manifest
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

Each item's `registry-item.json` contains: name, type, title, description, tags, dimensions (blocks only), duration (blocks only), and file list.

Filter by type (block/component) and tags to find what you need.

## Example Components

| Name | Type | Description |
|------|------|-------------|
| `flash-through-white` | block | Shader transition effect |
| `instagram-follow` | component | Social media overlay |
| `data-chart` | block | Animated data visualization |
| `grain-overlay` | component | Film grain texture |
| `shimmer-sweep` | component | Shimmer highlight effect |
