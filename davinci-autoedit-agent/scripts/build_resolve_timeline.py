from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def load_resolve_module():
    try:
        return importlib.import_module("DaVinciResolveScript")
    except ImportError:
        module_path = os.getenv("RESOLVE_SCRIPT_API", "")
        if module_path:
            sys.path.insert(0, module_path)
            return importlib.import_module("DaVinciResolveScript")
        raise RuntimeError(
            "DaVinciResolveScript is unavailable. Configure Resolve scripting "
            "or use davinci-resolve-mcp."
        )


def frames(seconds: float, fps: float) -> int:
    return int(round(seconds * fps))


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Build a new Resolve timeline from an approved blueprint.")
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--timeline-name")
    args = parser.parse_args()
    plan = json.loads(args.blueprint.read_text(encoding="utf-8"))
    project_config = plan["project"]
    fps = float(project_config["fps"])
    project_name = args.project_name or project_config["name"]
    timeline_name = args.timeline_name or f"{project_name} Assembly"

    resolve_script = load_resolve_module()
    resolve = resolve_script.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError("Cannot connect to Resolve. Open Resolve Studio and enable Local scripting.")
    manager = resolve.GetProjectManager()
    project = manager.CreateProject(project_name)
    if not project:
        raise RuntimeError(f"Cannot create project {project_name!r}; choose a new name.")

    project.SetSetting("timelineFrameRate", str(project_config["fps"]))
    project.SetSetting("timelineResolutionWidth", str(project_config["width"]))
    project.SetSetting("timelineResolutionHeight", str(project_config["height"]))
    media_pool = project.GetMediaPool()
    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    if not timeline:
        raise RuntimeError("Cannot create timeline.")
    project.SetCurrentTimeline(timeline)

    imported: dict[str, object] = {}
    for source in sorted({str(clip["source_path"]) for clip in plan.get("clips", [])}):
        items = media_pool.ImportMedia([source]) or []
        if not items:
            raise RuntimeError(f"Resolve could not import {source}")
        imported[source] = items[0]

    failures = []
    for clip in sorted(plan.get("clips", []), key=lambda item: item["timeline_in_seconds"]):
        media_type = 1 if clip.get("media_type", "video") in {"video", "image"} else 2
        request = {
            "mediaPoolItem": imported[str(clip["source_path"])],
            "startFrame": frames(float(clip["source_in_seconds"]), fps),
            "endFrame": frames(float(clip["source_out_seconds"]), fps) - 1,
            "recordFrame": frames(float(clip["timeline_in_seconds"]), fps),
            "mediaType": media_type,
            "trackIndex": int(clip.get("video_track" if media_type == 1 else "audio_track", 1)),
        }
        if not media_pool.AppendToTimeline([request]):
            failures.append(clip.get("id", str(clip["source_path"])))

    manager.SaveProject()
    report = {
        "project": project.GetName(),
        "timeline": timeline.GetName(),
        "expected_clips": len(plan.get("clips", [])),
        "failed_clips": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
