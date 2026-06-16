from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

VIDEO = {".mp4", ".mov", ".mkv", ".avi", ".mts", ".m2ts", ".webm", ".mpg", ".mpeg", ".mxf"}
AUDIO = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".aiff", ".wma"}
IMAGE = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp", ".heic"}


def probe(path: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate,channels,sample_rate",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        return {"error": result.stderr.strip()}
    return json.loads(result.stdout or "{}")


def quick_hash(path: Path) -> str:
    digest = hashlib.sha256()
    size = path.stat().st_size
    with path.open("rb") as handle:
        digest.update(handle.read(1024 * 1024))
        if size > 1024 * 1024:
            handle.seek(max(0, size - 1024 * 1024))
            digest.update(handle.read(1024 * 1024))
    digest.update(str(size).encode("ascii"))
    return digest.hexdigest()


def collect(inputs: list[Path]) -> list[Path]:
    found: set[Path] = set()
    allowed = VIDEO | AUDIO | IMAGE
    for item in inputs:
        if item.is_file() and item.suffix.lower() in allowed:
            found.add(item.resolve())
        elif item.is_dir():
            found.update(p.resolve() for p in item.rglob("*") if p.is_file() and p.suffix.lower() in allowed)
    return sorted(found, key=lambda p: str(p).lower())


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan arbitrary video, audio, and image paths.")
    parser.add_argument("--input", action="append", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    rows = []
    for path in collect(args.input):
        suffix = path.suffix.lower()
        media_type = "video" if suffix in VIDEO else "audio" if suffix in AUDIO else "image"
        metadata = probe(path) if media_type != "image" else {}
        rows.append({
            "path": str(path),
            "media_type": media_type,
            "extension": suffix,
            "size_bytes": path.stat().st_size,
            "quick_hash": quick_hash(path),
            "probe": metadata,
        })

    manifest = args.output / "media-manifest.json"
    manifest.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = Counter(row["media_type"] for row in rows)
    summary = {"inputs": [str(p.resolve()) for p in args.input], "file_count": len(rows), "counts": dict(counts)}
    (args.output / "scan-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
