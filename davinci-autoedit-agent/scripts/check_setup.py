from __future__ import annotations

import json
import os
import shutil
import sys

from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    report = {
        "python": sys.version.split()[0],
        "ffmpeg": shutil.which("ffmpeg") or "",
        "ffprobe": shutil.which("ffprobe") or "",
        "node": shutil.which("node") or "",
        "npx": shutil.which("npx") or "",
        "llm": {
            "configured": bool(os.getenv("LLM_BASE_URL") and os.getenv("LLM_MODEL")),
            "has_api_key": bool(os.getenv("LLM_API_KEY")),
        },
        "tts": {
            "configured": bool(os.getenv("TTS_BASE_URL")),
            "has_api_key": bool(os.getenv("TTS_API_KEY")),
        },
    }
    print(json.dumps(report, indent=2))
    return 0 if report["ffmpeg"] and report["ffprobe"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
