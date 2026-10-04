# After Effects Agent Workflow

[![Helper checks](https://github.com/progress1ve/ae-agent-workflow/actions/workflows/check.yml/badge.svg)](https://github.com/progress1ve/ae-agent-workflow/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Make editable motion graphics with **Codex, Claude Code, or another local coding agent**—and keep the artist in control of the composition.

This repository packages a reusable agent skill, a local sound-design MCP, installation helpers, and practical lessons from a short advertising-banner production. It connects to the independent [mcp-aftereffects](https://github.com/kumoproductions/mcp-aftereffects) project by kumo.productions; it does not replace Adobe After Effects or supply an Adobe license.

## Install from your chat

Paste this into a **local agent with terminal access**:

```text
Install https://github.com/progress1ve/ae-agent-workflow for my local
After Effects workflow. Read README.md and scripts/install.py first.
Clone the repository into a separate tools directory, run its installer
for my client, register the AE MCP and optional local audio MCP, and
preserve existing configuration. Verify the connection with project
inspection. Do not modify my project or render anything during setup.
```

Tell the agent whether you use Codex or Claude Code. Installation may download npm/Python dependencies. A browser-only chat cannot operate your local AE through this stdio setup.

## Manual quick start

Prerequisites: licensed AE, Node.js **24+**, Python **3.10+**, Git, and a local MCP-capable client. The tested combination is **Windows, After Effects 2025, and mcp-aftereffects 0.3.1**. macOS and other clients are documented paths, not locally verified combinations.

```bash
git clone https://github.com/progress1ve/ae-agent-workflow.git
cd ae-agent-workflow
python scripts/install.py --client codex --register --audio
```

For Claude Code, replace `--client codex` with `--client claude`. For a different client, use `--client generic --skill-dir /your/skills/after-effects-workflow` and copy the generated MCP JSON into that client's configuration.

Open AE normally, open a disposable project or a saved copy, and enable **Preferences → Scripting & Expressions → Allow Scripts to Write Files and Access Network**. Restart/reconnect your agent after MCP configuration changes. Ask it to inspect the active project and list composition names.

The installer refuses to overwrite an existing skill unless `--update` is supplied. Existing MCP server registrations are retained. `--skip-deps` skips audio dependency installation; `--audio` otherwise creates a repository-local virtual environment. `--register` is optional: without it, the installer prints configuration and makes no client configuration changes.

## What you get

| Component | Purpose |
| --- | --- |
| `skills/after-effects-workflow` | Asset handling, AE editing, review, revision and export guidance |
| Upstream AE MCP | Project/layer inspection, supported edits, frame previews and save operations |
| `audio/server.py` | Local cue mixing, audio inspection, optional offline word alignment |
| `scripts/run-jsx.ps1` | Explicit Windows fallback for a reviewed JSX file |
| `scripts/export_frames.jsx` | Explicitly requested alpha frame export from an existing composition |
| `scripts/encode_frames.py` | Preview, chroma and lossless alpha exports from those frames |
| `docs/CASE_STUDY.md` | What actually worked, failed and changed during production |

There is no bundled voice, music, advertising footage, font, logo pack or customer screenshot. Use assets you own or are licensed to use. No paid AI API is required by these helper scripts; your agent and Adobe licensing remain separate.

## A productive editing loop

1. Agree on duration, scene content, asset placement and export requirements.
2. Inspect the current AE project. Save a new revision before meaningful changes.
3. Build native editable text, masks, shapes and keyframes. Keep original footage linked.
4. Review in AE. Use a few representative frame previews only when useful and authorized.
5. Apply specific feedback without rebuilding unrelated approved sections.
6. Render after the user requests export. Check decoded duration, sound peaks, alpha and chroma boundaries.

**Review mode** means no video export. If the artist says “no rendering”, inspect metadata and let them scrub AE; do not substitute a contact-sheet render without clarification.

Example request:

```text
Create a 5-second, 1920×800, 30fps banner in my open AE project.
Keep text editable. Use the supplied phone image and logo exactly.
Use four scenes: hook, benefit, price/product, brand/contact.
Show the phone's full upper rim and crop only the lower part.
Use square grid cells behind objects and soft blue edge lighting.
Preserve alpha, reveal the card from a circle, then collapse it.
Do not render yet. Save a new AEP and open its review composition.
```

## Sound design

```bash
python audio/audio_ops.py --timeline examples/sound-plan.json --out output/mix.wav
python audio/audio_ops.py --timeline my-plan.json --out output/mix.wav --voice voice.wav
python audio/audio_ops.py --inspect output/mix.wav
```

Paths in a cue plan are relative to the **plan file**, or absolute. See [the audio guide](docs/AUDIO.md). Optional Whisper alignment needs `requirements-align.txt`; its first run downloads a model. Alignment is an estimate: inspect the voice before making tight edits.

## Troubleshooting and limitations

See [installation](docs/INSTALLATION.md), [AE pitfalls](skills/after-effects-workflow/references/ae-pitfalls.md), [export](docs/EXPORT.md), and [collaboration](skills/after-effects-workflow/references/collaboration.md).

MCP makes repeated operations compact, but does not guarantee lower model usage. Short tool results, focused reads, retained project context and fewer unnecessary renders are the practical savings. Motion-design judgment still requires review.

## Contributing

Small reproducible fixes are welcome. Include the OS, AE version, MCP version, exact operation and expected/actual behavior. Never attach credentials or unlicensed project assets. Read [CONTRIBUTING.md](CONTRIBUTING.md).

MIT licensed original code and documentation. Third-party packages retain their own licenses. See [NOTICE.md](NOTICE.md).
