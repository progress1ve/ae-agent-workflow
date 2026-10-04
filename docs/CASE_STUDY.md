# Production notes: a five-second banner

This workflow was extracted from a real local AE2025 production with repeated artist feedback. Private project assets, voice files and sound packs are excluded.

## Result

Four scenes: an animated hook, bypass benefit, price with a phone, then a large brand/contact lockup. Native editable text and masks; an exact logo rendered with Blender; a supplied phone image; cold blue lighting; square grid; word highlights; local voice/SFX mixing; rounded alpha reveal/collapse; preview, chroma and alpha exports.

## What helped

| Tool or skill | Actual contribution |
| --- | --- |
| kumo.productions AE MCP | Project inspection, modal diagnostics and representative frame/contact-sheet capture |
| Reviewed local JSX | Deterministic native layers, keyframes, masks, revision saves and alpha-frame export |
| Custom local sound-design MCP/CLI | Cue mixing, peak/RMS inspection, timestamp JSON and reproducible sound plans |
| Remotion timing guidance | Explicit timing and settling/camera principles; the final piece remained in AE, not a Remotion project |
| Blender | Exact extruded two-part logo and reusable transparent motion frames |
| FFmpeg, Pillow and OpenCV | Container normalization, encoding and decoded-frame/alpha/audio checks |
| Skill Creator | Packaging the learned workflow into this portable skill |

MCP and CLI usage were complementary. Some tools were configured through MCP, but local command invocation was still needed when a tool was not exposed in the active session. Do not claim a connector was used merely because it was installed.

## Lessons from revisions

- Text-to-3D generation distorted a geometric brand mark. Exact extrusion from the vector worked better.
- Video generation repeatedly cropped the logo despite framing instructions. Native composition gave predictable margins and timing.
- A thick rounded CTA slab looked like soap. Clear editable typography served the contact message better.
- A small phone made account details unreadable; a larger image with its top rim preserved and lower edge cropped worked better.
- Non-uniform grid scaling and incorrect stacking were visible immediately. Uniform native cells below the product solved both.
- Global icon tint flattened multicolor symbols. Original color, larger scale and restrained radial blur preserved identity.
- The artist wanted price/product and contacts separated. A fourth scene with a downward transition made the final message clearer.
- Centering only the text did not center the icon/title group. Combined visible bounds must define the lockup center.
- Quiet effects disappeared under voice. A louder cue mix with headroom, including a3.55s transition whoosh, completed the rhythm.

## Working with this artist

The artist preferred short communication, annotated screenshots, retained original assets, explicit native-AE review before rendering, and progressively concrete revisions. These are recorded as collaboration preferences, not universal defaults for all users. Low token usage was supported by compact tool results and local JSON artifacts; no measured token-saving percentage is claimed.

Tested exports used150 decoded frames at30fps,1920×800,5seconds, with corner alpha0 and opaque center255 in a hold frame. Final deliverables need their own evidence; this case study is not a blanket guarantee for every project.
