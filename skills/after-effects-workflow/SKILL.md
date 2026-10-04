---
name: after-effects-workflow
description: Build, revise and export editable motion graphics in a local Adobe After Effects project using an AE MCP or reviewed JSX, with asset fidelity, sound timing and artist-led review.
---

# After Effects Workflow

Inspect the active project before editing. Identify the target composition, current revision, linked assets, duration/fps, and whether this is review or export work. Preserve unrelated layers and user edits. Save a new revision for substantial changes; small approved fixes may stay in the requested revision.

For a new or restructured piece, agree on scene content and timing before building. Reuse approved sections and original assets. Preserve logos, phone screens, proportions and brand spelling; generative assets are optional and never a substitute for exact typography or geometry.

Use the available AE MCP for supported operations. Read tool schemas rather than guessing arguments. Use inspected, local JSX only when the needed operation is unavailable; keep an undo group and save marker. Never guess effect property indices: inspect match names and skip properties with `NO_VALUE`. Read [AE pitfalls](references/ae-pitfalls.md) before effect, mask, script-launch or export work.

Prefer native text/shapes/masks/keyframes. Treat a camera move as coherent movement of scene content, not isolated random layer motion. Maintain reading time and safe edges. Keep backgrounds and grid layers beneath product imagery. Uniform scaling preserves square grid cells. Soft glows are broad light fields with falloff; a blurred thin rectangle is not a convincing edge light.

For voice sync, use word timestamps only as a starting estimate. Trim silence before speeding up speech. Mix transition sounds against the voice and check peaks after encoding. Use local audio tools when available; read [audio cues](references/audio-cues.md) for cue-plan details.

Review before export. If the user says no rendering, save/open the AEP and inspect metadata; do not export frames or video. Otherwise sample representative transition/hold/exit frames proportionally. State what was inspected. Do not claim visual verification from a save marker alone.

Render only when requested or already authorized for the current revision. Prefer alpha as the master, then derive preview/chroma copies. Verify decoded frame count, duration/fps/dimensions, audio headroom and transparent/keyed boundaries. Keep dependencies when cleaning old versions; remove only the authorized class.

Keep replies short when the artist prefers it. Ask for missing decisions only when they affect the outcome; use annotated frames and timestamps as concrete feedback. Read [collaboration](references/collaboration.md) for the working loop and handoff template.
