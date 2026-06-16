---
name: davinci-resolve-editor
description: Safe DaVinci Resolve Studio editing through davinci-resolve-mcp or the official Resolve Python API. Use when Codex must inspect Resolve state, create or revise projects and timelines, import approved media, place source ranges, apply authorized LUTs or effects, prepare rendering, and verify gaps, tracks, source bounds, frame origin, and actual write success.
---

# DaVinci Resolve Editor

Operate only from an approved blueprint. Read `references/mcp-operations.md` for
the tool map and `references/verification.md` before delivery.

For deeper operations, load only the relevant bundled reference:

- `references/compound-tool-reference.md`
- `references/prompt-patterns.md`
- `references/page-capabilities.md`
- `references/keyboard-shortcuts.md`

## Connect

1. Confirm Resolve Studio is open and external scripting is set to `Local`.
2. Call `resolve -> get_version`.
3. If the tool is unavailable, distinguish missing registration from a server
   failure. An MCP config file alone is not proof of connection.
4. Offer blueprint-only delivery or the official Python API fallback.

Install the upstream MCP server when the user approves configuration:

```bash
npx davinci-resolve-mcp setup
```

## Write Contract

Before changing Resolve, state:

- project and timeline name
- tracks to create or modify
- media and derivative paths
- color, audio, subtitle, and render operations

Obtain explicit approval. Use a new project or duplicated timeline for
substantial revisions. Preserve existing user tracks, audio, grades, and
manual work unless the user explicitly authorizes modification.

## Build

- Import only blueprint media.
- Convert seconds to frames using the actual project FPS.
- Set source in/out and record frame deliberately.
- Keep source ranges within probed bounds.
- Use explicit track roles rather than assuming A1/A2/A3 universally.
- Add BGM, LUTs, stabilization, retiming, audio processing, and renders only
  when the current request authorizes them.
- Apply LUTs to verified camera/color-space groups and read back the node LUT.

## Resolve API Boundaries

- Resolve writes are stateful; wait and retry in a fresh project/timeline when
  a batch partially fails.
- Derive frame origin from actual timeline items.
- Still-image duration may differ by Resolve version; use approved pre-rendered
  still video for frame-exact delivery.
- Resolve 19 may reject item volume writes and does not expose complete
  Fairlight sidechain automation. Measurement is not a successful write.
- Never report an unsupported or rejected operation as completed.

## Verify

Read back and report:

- active project and timeline
- item counts by track
- timeline start frame/origin
- gaps, overlaps, and one-frame errors
- each source path and source range
- source group/camera duration ratios
- adjacent repeated source, including section boundaries
- missing or offline media
- LUT/effect/property readback
- render settings and job status, when requested

A failed report or a report for an older timeline is not delivery.

Export or report enough timeline information for the parent pipeline to compare
the finished cut with the approved script: clip time ranges, source paths,
track roles, markers, captions, and narration/dialogue placement. Do not make
pickup-shot recommendations from the blueprint alone when a finished timeline
exists.
