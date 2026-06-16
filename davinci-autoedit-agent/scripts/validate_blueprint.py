from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an approved edit blueprint.")
    parser.add_argument("blueprint", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.blueprint.read_text(encoding="utf-8"))
    clips = payload.get("clips", [])
    errors: list[str] = []
    warnings: list[str] = []
    groups: Counter[str] = Counter()
    previous_source = ""
    previous_out: float | None = None

    for index, clip in enumerate(clips, start=1):
        label = clip.get("id", f"clip-{index}")
        source = Path(str(clip.get("source_path", "")))
        source_in = float(clip.get("source_in_seconds", 0))
        source_out = float(clip.get("source_out_seconds", 0))
        timeline_in = float(clip.get("timeline_in_seconds", 0))
        timeline_out = float(clip.get("timeline_out_seconds", 0))
        if not source.exists():
            errors.append(f"{label}: missing source {source}")
        if source_out <= source_in:
            errors.append(f"{label}: non-positive source duration")
        if timeline_out <= timeline_in:
            errors.append(f"{label}: non-positive timeline duration")
        if abs((source_out - source_in) - (timeline_out - timeline_in)) > 0.05 and not clip.get("speed"):
            warnings.append(f"{label}: source/timeline duration mismatch without speed declaration")
        if previous_out is not None:
            delta = timeline_in - previous_out
            if delta > 0.001:
                warnings.append(f"{label}: timeline gap {delta:.3f}s")
            elif delta < -0.001:
                errors.append(f"{label}: timeline overlap {-delta:.3f}s")
        if previous_source and str(source) == previous_source:
            warnings.append(f"{label}: adjacent reuse of source {source.name}")
        groups[str(clip.get("source_group", "unclassified"))] += timeline_out - timeline_in
        previous_source = str(source)
        previous_out = timeline_out

    report = {
        "clip_count": len(clips),
        "errors": errors,
        "warnings": warnings,
        "duration_by_source_group_seconds": dict(groups),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
