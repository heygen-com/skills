---
name: video-compare
description: |
  Compare video quality using SSIM, PSNR, and VMAF metrics. Generate side-by-side and difference visualizations.
  Use when the user says "compare videos", "quality metrics", "SSIM", "PSNR", "VMAF", "side by side", "before after", "compression quality".
argument-hint: "<reference-video> <distorted-video>"
version: 1.0.0
---

# Video Compare — Quality Metrics & Visual Comparison

Compute SSIM, PSNR, and VMAF quality metrics between two videos. Generate side-by-side and difference visualizations for visual inspection.

## Step 0: Prerequisites

```bash
if ! command -v ffmpeg &>/dev/null; then
  echo "ffmpeg not found. Install via: brew install ffmpeg"
  exit 1
fi

# Check VMAF availability (optional)
ffmpeg -filters 2>/dev/null | grep -q libvmaf && echo "VMAF: available" || echo "VMAF: not available (install via: brew install ffmpeg --with-libvmaf or use a full build)"
```

**Important input order conventions**:
- **SSIM/PSNR**: Reference is first input (`-i reference`), distorted is second — ffmpeg compares second against first
- **VMAF**: **Opposite!** Distorted is first input, reference is second — `libvmaf` expects `main=distorted:reference`

## Step 1: SSIM Quality Metric

SSIM (Structural Similarity Index) — ranges from 0 to 1, where 1 = identical:

```bash
ffmpeg -i "$REFERENCE" -i "$DISTORTED" \
  -lavfi "ssim=stats_file=/tmp/ssim_per_frame.log" \
  -f null - 2>&1 | grep "SSIM"
```

Output example: `SSIM Y:0.952843 (13.264) U:0.972338 (15.578) V:0.975337 (16.082) All:0.960038 (13.982)`

**SSIM quality guide**:
| SSIM | Quality |
|-|-|
| > 0.98 | Imperceptible difference |
| 0.95–0.98 | Excellent — minor artifacts |
| 0.90–0.95 | Good — visible on close inspection |
| 0.80–0.90 | Fair — noticeable degradation |
| < 0.80 | Poor |

Per-frame SSIM is saved to `/tmp/ssim_per_frame.log` for analysis:

```bash
# Find worst frames
sort -t' ' -k5 -n /tmp/ssim_per_frame.log | head -10
```

## Step 2: PSNR Quality Metric

PSNR (Peak Signal-to-Noise Ratio) — measured in dB, higher is better:

```bash
ffmpeg -i "$REFERENCE" -i "$DISTORTED" \
  -lavfi "psnr=stats_file=/tmp/psnr_per_frame.log" \
  -f null - 2>&1 | grep "PSNR"
```

Output example: `PSNR y:38.52 u:43.27 v:44.31 average:39.83 min:32.15 max:inf`

**PSNR quality guide**:
| PSNR (dB) | Quality |
|-|-|
| > 45 | Excellent — near lossless |
| 40–45 | Very good |
| 35–40 | Good — acceptable for streaming |
| 30–35 | Fair — visible compression |
| < 30 | Poor |

## Step 3: VMAF Perceptual Quality

VMAF (Video Multimethod Assessment Fusion) — Netflix's perceptual quality metric, 0–100 scale:

**CRITICAL**: VMAF input order is reversed from SSIM/PSNR — distorted is first, reference is second:

```bash
# Note: $DISTORTED is the FIRST input, $REFERENCE is the SECOND
ffmpeg -i "$DISTORTED" -i "$REFERENCE" \
  -lavfi "libvmaf=log_path=/tmp/vmaf.json:log_fmt=json:model=version=vmaf_v0.6.1" \
  -f null - 2>&1 | grep "VMAF"
```

**VMAF quality guide**:
| VMAF | Quality |
|-|-|
| > 93 | Excellent — broadcast quality |
| 80–93 | Good — acceptable streaming |
| 60–80 | Fair — mobile/low-bandwidth |
| < 60 | Poor |

If videos have different resolutions, scale to match:

```bash
ffmpeg -i "$DISTORTED" -i "$REFERENCE" \
  -lavfi "[0:v]scale=1920:1080:flags=bicubic[dist];[1:v]scale=1920:1080:flags=bicubic[ref];[dist][ref]libvmaf" \
  -f null - 2>&1 | grep "VMAF"
```

## Step 4: All Metrics at Once

Compute SSIM, PSNR, and VMAF in a single pass (efficient for large files):

```bash
# SSIM and PSNR (same input order: reference first)
ffmpeg -i "$REFERENCE" -i "$DISTORTED" \
  -lavfi "[0:v][1:v]ssim=stats_file=/tmp/ssim.log;[0:v][1:v]psnr=stats_file=/tmp/psnr.log" \
  -f null - 2>&1 | grep -E "SSIM|PSNR"
```

Note: VMAF must be run separately due to its reversed input order.

## Step 5: Side-by-Side Comparison Video

### Horizontal stack (left = reference, right = distorted)

```bash
ffmpeg -i "$REFERENCE" -i "$DISTORTED" \
  -filter_complex "[0:v]drawtext=text='Reference':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5[ref];[1:v]drawtext=text='Distorted':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5[dist];[ref][dist]hstack=inputs=2" \
  -c:v libx264 -crf 18 -y side_by_side.mp4
```

### Vertical stack (top = reference, bottom = distorted)

```bash
ffmpeg -i "$REFERENCE" -i "$DISTORTED" \
  -filter_complex "[0:v]drawtext=text='Reference':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5[ref];[1:v]drawtext=text='Distorted':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5[dist];[ref][dist]vstack=inputs=2" \
  -c:v libx264 -crf 18 -y stacked.mp4
```

If resolutions differ, scale first:

```bash
ffmpeg -i "$REFERENCE" -i "$DISTORTED" \
  -filter_complex "[0:v]scale=640:360[ref];[1:v]scale=640:360[dist];[ref]drawtext=text='Reference':x=10:y=10:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.5[reflbl];[dist]drawtext=text='Distorted':x=10:y=10:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.5[distlbl];[reflbl][distlbl]hstack" \
  -c:v libx264 -crf 18 -y side_by_side.mp4
```

## Step 6: Difference Visualization

Show only the pixels that differ between two videos (amplified for visibility):

```bash
ffmpeg -i "$REFERENCE" -i "$DISTORTED" \
  -filter_complex "blend=all_mode=difference,curves=all='0/0 0.1/1'" \
  -c:v libx264 -crf 18 -y difference.mp4
```

- `blend=all_mode=difference`: Subtracts pixel values — identical pixels become black
- `curves=all='0/0 0.1/1'`: Amplifies small differences so they're visible (maps 10% difference to white)

Without amplification (raw difference):

```bash
ffmpeg -i "$REFERENCE" -i "$DISTORTED" \
  -filter_complex "blend=all_mode=difference" \
  -c:v libx264 -crf 18 -y raw_difference.mp4
```

## Step 7: Frame-by-Frame Comparison at Specific Timestamps

Extract and compare frames at a particular time:

```bash
TIMESTAMP="00:00:05"

# Extract one frame from each video
ffmpeg -ss "$TIMESTAMP" -i "$REFERENCE" -vframes 1 -y /tmp/ref_frame.png
ffmpeg -ss "$TIMESTAMP" -i "$DISTORTED" -vframes 1 -y /tmp/dist_frame.png

# Side-by-side single frame
ffmpeg -i /tmp/ref_frame.png -i /tmp/dist_frame.png \
  -filter_complex "[0]drawtext=text='Reference':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5[r];[1]drawtext=text='Distorted':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5[d];[r][d]hstack" \
  -y comparison_frame.png

# Difference of single frame
ffmpeg -i /tmp/ref_frame.png -i /tmp/dist_frame.png \
  -filter_complex "blend=all_mode=difference,curves=all='0/0 0.1/1'" \
  -y diff_frame.png
```

## Common Workflows

1. **Check compression quality**: Run SSIM + PSNR (Step 4) to get numbers, then interpret with the quality guides
2. **A/B encode comparison**: Side-by-side video (Step 5) for visual review + SSIM for objective score
3. **Find worst frames**: Run SSIM with per-frame log, sort to find lowest-quality frames
4. **Verify lossless encode**: SSIM should be 1.000, PSNR should be `inf`
5. **Netflix-grade quality check**: Use VMAF (Step 3) — target > 93 for broadcast

## Error Handling

- **"Input dimensions don't match"**: Scale both inputs to the same resolution before comparing (see Step 3 scaling example)
- **VMAF scores seem inverted**: Check input order — distorted MUST be first, reference second (opposite of SSIM/PSNR)
- **"No such filter: libvmaf"**: VMAF model not compiled in — check with `ffmpeg -filters | grep vmaf`. Install a full ffmpeg build or skip VMAF
- **Very slow on large files**: Add `-t 30` to analyze only first 30 seconds for quick comparison
- **Different frame counts**: ffmpeg compares frame-by-frame and stops at the shorter video — trim to same duration first if needed
- **Per-frame log is empty**: Check that the `stats_file` path is writable
