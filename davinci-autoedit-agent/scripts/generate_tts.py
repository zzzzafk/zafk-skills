from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Generate approved TTS segments through a configurable HTTP API.")
    parser.add_argument("--script", required=True, type=Path, help="JSON list with id and text fields.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--endpoint", default=os.getenv("TTS_BASE_URL", ""))
    parser.add_argument("--model", default=os.getenv("TTS_MODEL", ""))
    parser.add_argument("--reference-audio", type=Path, default=os.getenv("TTS_REFERENCE_AUDIO") or None)
    parser.add_argument("--mode", choices=("json", "multipart"), default="json")
    args = parser.parse_args()
    if not args.endpoint:
        raise SystemExit("TTS is not configured. Set TTS_BASE_URL or pass --endpoint.")

    segments = json.loads(args.script.read_text(encoding="utf-8"))
    args.output.mkdir(parents=True, exist_ok=True)
    headers = {}
    if os.getenv("TTS_API_KEY"):
        headers["Authorization"] = f"Bearer {os.environ['TTS_API_KEY']}"

    manifest = []
    for index, segment in enumerate(segments, start=1):
        segment_id = str(segment.get("id") or f"{index:03d}")
        payload = {"text": segment["text"], "model": args.model}
        if args.mode == "multipart":
            files = None
            handle = None
            if args.reference_audio:
                handle = args.reference_audio.open("rb")
                files = {"reference_audio": (args.reference_audio.name, handle, "audio/wav")}
            try:
                response = requests.post(args.endpoint, data=payload, files=files, headers=headers, timeout=1200)
            finally:
                if handle:
                    handle.close()
        else:
            response = requests.post(args.endpoint, json=payload, headers=headers, timeout=1200)
        response.raise_for_status()
        output = args.output / f"{segment_id}.wav"
        output.write_bytes(response.content)
        manifest.append({"id": segment_id, "text": segment["text"], "audio_path": str(output)})

    (args.output / "tts-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
