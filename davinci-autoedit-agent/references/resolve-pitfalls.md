# Resolve Pitfalls And Required Audits

- MCP configured is not MCP connected. Verify a real tool call.
- Resolve writes are stateful. Repeated project creation can leave video
  successful while later audio appends fail. Build revisions in a new project
  or timeline and retry after Resolve becomes idle.
- Timeline frame origin may be `1`, not `0`. Derive it from actual items.
- Still images can land shorter than requested on some Resolve versions.
  Pre-render approved still sequences to fixed-rate video when exact timing is
  required; never fill gaps by repeating random tail frames.
- Audit adjacent source across section boundaries, not only inside sections.
- Apply camera LUTs only after checking metadata, representative frames,
  input color space, and LUT identity. Apply to the intended camera family
  only, then read back the node LUT.
- Resolve 19 scripting may reject item volume writes and does not expose full
  Fairlight automation or sidechain curves. Loudness measurement is not a
  successful write. Offer manual Fairlight, UI automation when available, or
  an explicitly approved offline bake.
- After interruption, stop and inspect background FFmpeg/Python jobs and
  half-built timelines before resuming.
- A report generated for an earlier timeline cannot validate the current one.
