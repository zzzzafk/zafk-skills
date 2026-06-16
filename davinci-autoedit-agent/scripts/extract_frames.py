from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip() or 0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract review frames at a fixed interval.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--interval", type=float, default=30.0)
    parser.add_argument("--width", type=int, default=1280)
    args = parser.parse_args()
    if args.interval <= 0:
        raise SystemExit("--interval must be positive")

    rows = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output.mkdir(parents=True, exist_ok=True)
    extracted = []
    for media_index, row in enumerate(rows, start=1):
        if row.get("media_type") != "video":
            continue
        source = Path(row["path"])
        item_dir = args.output / f"{media_index:04d}-{source.stem}"
        item_dir.mkdir(parents=True, exist_ok=True)
        total = duration(source)
        timestamp = 0.0
        frame_index = 1
        while timestamp < max(total, 0.001):
            output = item_dir / f"{frame_index:04d}-{timestamp:.3f}.jpg"
            command = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{timestamp:.3f}",
                "-i", str(source), "-frames:v", "1", "-vf",
                f"scale={args.width}:-2", "-y", str(output),
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            extracted.append({
                "source_path": str(source),
                "timestamp_seconds": timestamp,
                "image_path": str(output),
                "ok": result.returncode == 0 and output.exists(),
                "error": result.stderr.strip() if result.returncode else "",
            })
            frame_index += 1
            timestamp += args.interval

    index_path = args.output / "frames-index.json"
    index_path.write_text(json.dumps(extracted, ensure_ascii=False, indent=2), encoding="utf-8")
    print(index_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
