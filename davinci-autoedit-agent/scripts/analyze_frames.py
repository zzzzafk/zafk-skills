from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def analyze(endpoint: str, api_key: str, model: str, image: Path, topic: str) -> dict:
    encoded = base64.b64encode(image.read_bytes()).decode("ascii")
    prompt = (
        "Analyze this frame objectively for a video editor. Return JSON with "
        "description, visible_text, people, actions, setting, emotion, "
        "technical_quality, continuity_clues, suggested_uses, and tags. "
        "Do not invent details. Project topic: " + topic
    )
    payload = {
        "model": model,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}},
            ],
        }],
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    response = requests.post(
        f"{endpoint.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=int(os.getenv("LLM_TIMEOUT_SECONDS", "300")),
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Analyze approved review frames with an OpenAI-compatible vision API.")
    parser.add_argument("--frames-index", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    endpoint = os.getenv("LLM_BASE_URL", "")
    model = os.getenv("LLM_MODEL", "")
    if not endpoint or not model:
        raise SystemExit("Set LLM_BASE_URL and LLM_MODEL before API analysis.")

    rows = json.loads(args.frames_index.read_text(encoding="utf-8"))
    rows = [row for row in rows if row.get("ok")]
    if args.limit > 0:
        rows = rows[: args.limit]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in rows:
            try:
                result = analyze(
                    endpoint,
                    os.getenv("LLM_API_KEY", ""),
                    model,
                    Path(row["image_path"]),
                    args.topic,
                )
                payload = {**row, "analysis": result, "error": ""}
            except Exception as exc:
                payload = {**row, "analysis": {}, "error": str(exc)}
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
            handle.flush()
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
