# Pickup-Shot And Missing-Material Report

Generate this report only after comparing the approved script, finished cut,
and complete reviewed inventory.

## Summary

- Finished timeline:
- Script version:
- Inventory/review version:
- Required missing shots:
- Strongly recommended shots:
- Optional enhancements:
- Existing unused alternatives found:

## Priority Definitions

- `P0 Required`: omission makes the video unsupported, misleading, confusing,
  incomplete, unsafe, or noncompliant.
- `P1 Strongly Recommended`: omission materially weakens comprehension,
  continuity, credibility, or emotional payoff.
- `P2 Optional Enhancement`: improves texture, rhythm, variety, or polish.

## Recommendation Fields

Use one entry per missing editorial function:

```markdown
### P0-01: Show the completed result

- Script reference: Section 5, line 3
- Timeline location: 00:06:42-00:06:51
- Missing function: The narration claims the repair succeeded, but the cut
  never shows the working result.
- Existing-media check: No reviewed clip shows the device operating after the
  repair; clip C014 ends before the test.
- Capture:
  - Subject/action: Operator powers on the repaired device and completes one
    visible test cycle.
  - Framing: 5-second medium shot, then 4-second close-up of the indicator.
  - Movement: Locked or slow push-in.
  - Orientation/continuity: Match the operator's screen-left position and
    wardrobe from the preceding scene.
  - Location/time: Original workbench; match practical lighting if possible.
  - Sound: Record clean switch, motor, and confirmation sound for room tone.
  - Minimum usable duration: 12 seconds before trimming.
- Requirements: Original device required; original operator preferred.
- Safety/practical notes: Do not recreate unsafe failure conditions.
- Editorial placement: Replace generic cutaway at 00:06:44 and bridge into the
  reaction shot.
- If reshooting is impossible: Use the existing status log and close-up photo
  as an on-screen proof graphic, or rewrite the narration to avoid claiming a
  demonstrated result.
```

## Required Analysis Rules

1. Map every script beat to actual timeline coverage.
2. Check unused reviewed media before requesting a reshoot.
3. Combine requests that can be captured in one setup.
4. Specify editorial function before camera technique.
5. Avoid prescribing expensive gear when a simple shot solves the problem.
6. Flag impossible continuity recreation and propose an honest alternative.
7. Do not request reenactment that could be mistaken for documentary reality
   unless it will be clearly disclosed.
8. Recommend script removal or rewrite when that is more truthful than a
   fabricated pickup.

## JSON Shape

```json
{
  "timeline": "Approved Cut v3",
  "script_version": "script-v2",
  "items": [
    {
      "id": "P0-01",
      "priority": "P0",
      "script_reference": "Section 5, line 3",
      "timeline_in_seconds": 402,
      "timeline_out_seconds": 411,
      "missing_function": "Proof of completed result",
      "existing_media_check": "No adequate reviewed source",
      "capture": {
        "subject_action": "Show the completed test cycle",
        "framing": ["medium", "close-up"],
        "movement": "locked",
        "minimum_usable_seconds": 12,
        "continuity": "Match preceding scene"
      },
      "requirements": ["original device"],
      "editorial_placement": "Replace generic cutaway",
      "fallback": "Use status-log graphic or rewrite unsupported claim"
    }
  ]
}
```
