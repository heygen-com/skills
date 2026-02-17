#!/usr/bin/env python3
"""Check video status via HeyGen API."""
import argparse
import json
import os
import sys
import time
import urllib.request

API_BASE = "https://api.heygen.com"


def get_status(video_id: str, api_key: str) -> dict:
    """Get video generation status."""
    url = f"{API_BASE}/v1/video_status.get?video_id={video_id}"
    req = urllib.request.Request(url, headers={"X-Api-Key": api_key})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def download_video(video_url: str, out_dir: str, video_id: str) -> str:
    """Download video to output directory."""
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{video_id}.mp4")
    urllib.request.urlretrieve(video_url, out_path)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Check video status via HeyGen API")
    parser.add_argument("--video-id", required=True, help="Video ID to check")
    parser.add_argument("--poll", action="store_true", help="Poll until complete")
    parser.add_argument("--download", action="store_true", help="Download video when complete")
    parser.add_argument("--out-dir", default="./heygen-output", help="Output directory")
    args = parser.parse_args()

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        print("Error: HEYGEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if args.poll:
        print(f"Polling video {args.video_id}...")
        while True:
            status = get_status(args.video_id, api_key)
            state = status.get("data", {}).get("status")
            print(f"  Status: {state}")
            if state == "completed":
                video_url = status["data"].get("video_url")
                print(f"Video URL: {video_url}")
                if args.download and video_url:
                    out_path = download_video(video_url, args.out_dir, args.video_id)
                    print(f"Downloaded to: {out_path}")
                break
            elif state == "failed":
                error = status.get("data", {}).get("error")
                print(f"Video generation failed: {error}", file=sys.stderr)
                sys.exit(1)
            time.sleep(5)
    else:
        status = get_status(args.video_id, api_key)
        print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
