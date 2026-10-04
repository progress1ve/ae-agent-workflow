# Installation

## For agents

When the user asks to install this repository or its skill:

1. Inspect README.md and scripts/install.py. Detect the local OS, client, Git, Python and Node prerequisites; ask only if the client cannot be determined.
2. Clone into a stable tools directory outside the user's project, or reuse an existing matching clone. Inspect local changes before updating it.
3. For a complete AE workflow, run `python scripts/install.py --client codex --register --audio` (or `--client claude`). If the user explicitly requests only the skill, omit `--register --audio` and explain that AE control still needs a bridge. Other clients use `--client generic --skill-dir <supported skill directory>` and the printed MCP configuration.
4. Preserve existing settings and registrations. Review an existing skill before using `--update`. Report missing prerequisites or client limitations instead of claiming setup succeeded.
5. Verify installed files and available MCP tools. If AE is running, inspect its project without changing it. Otherwise explain how to open AE and reconnect; do not claim an untested connection works.
6. Read the installed `after-effects-workflow/SKILL.md` and apply it to subsequent AE tasks. Setup alone does not authorize changing projects or rendering.

The user needs only a short installation request and the repository URL. This guide supplies the procedure; they do not need to copy a long prompt.

The installer copies the skill to `~/.agents/skills` for Codex or `~/.claude/skills` for Claude Code. A custom `--skill-dir` takes precedence. Existing skill content requires `--update`. Only `--register` calls your client's MCP registration command; it preserves existing server names.

AE bridge package pinned here: `@kumoproductions/mcp-aftereffects@0.3.1`. The author maintains its installation and platform requirements in the [upstream README](https://github.com/kumoproductions/mcp-aftereffects). No upstream code is vendored.

```bash
codex mcp add aftereffects -- npx -y @kumoproductions/mcp-aftereffects@0.3.1
claude mcp add aftereffects -- npx -y @kumoproductions/mcp-aftereffects@0.3.1
```

The installer prints optional audio registration using the absolute virtualenv interpreter and server path. This avoids reliance on shell activation. Other clients can use the equivalent `mcpServers` JSON it emits. Keep the clone at its configured path; move it only after updating the registration.

If `npx` invocation fails on Windows, follow your client's subprocess guidance or configure the actual `npx.cmd` path. If AE is installed outside the default locations, supply `AE_MCP_EXE` through your MCP client's environment configuration. Inspect the server version and active instance after connecting.

Use the client UI/CLI to reconnect. A newly configured server is not necessarily visible in an already running chat. The first acceptance check is project inspection on an actual running AE instance; installer success alone is not that check.

Optional offline alignment:

```bash
.venv-audio/Scripts/python.exe -m pip install -r requirements-align.txt
# macOS: .venv-audio/bin/python -m pip install -r requirements-align.txt
```

Whisper's model downloads on first use and is cached under the usual user cache. Use `--language en` or another supported code. Uncertain words still require listening.

Sources: [Codex MCP configuration](https://developers.openai.com/codex/mcp/), [Codex skill locations](https://developers.openai.com/codex/skills/), [Claude Code skills](https://code.claude.com/docs/en/skills). This repository is an independently distributed skill/tool kit, not an official marketplace plugin.
