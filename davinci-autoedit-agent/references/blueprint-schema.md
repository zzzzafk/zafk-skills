# Blueprint Schema

Use UTF-8 JSON with this minimum shape:

```json
{
  "schema_version": "1.0",
  "project": {
    "name": "Example",
    "fps": 30,
    "width": 1920,
    "height": 1080,
    "target_duration_seconds": 480
  },
  "tracks": {
    "video": ["V1"],
    "audio": ["A1", "A2"]
  },
  "clips": [
    {
      "id": "clip-001",
      "media_type": "video",
      "source_path": "/absolute/path/source.mp4",
      "source_in_seconds": 12.5,
      "source_out_seconds": 19.0,
      "timeline_in_seconds": 0.0,
      "timeline_out_seconds": 6.5,
      "video_track": 1,
      "audio_track": 1,
      "purpose": "Open on the central action",
      "source_group": "camera-a",
      "confidence": 0.9
    }
  ],
  "narration": [],
  "music": [],
  "captions": [],
  "notes": []
}
```

Rules:

- Use absolute source paths at build time.
- Keep `source_out_seconds` within probed duration.
- Require positive duration and matching source/timeline duration unless a
  speed change is declared.
- Declare still-image duration explicitly.
- Record music, LUT, retime, crop, stabilization, and audio processing as
  explicit authorized operations.
