"""Install the skill; optionally set up audio and register local MCP servers."""

import argparse
import json
import os
import shutil
import subprocess
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install_skill(target, update=False):
    source = ROOT / "skills/after-effects-workflow"
    target = Path(target).expanduser().resolve()
    if target.exists() and not update:
        raise ValueError(
            "Skill already exists; use --update after reviewing local changes"
        )
    # Merge only files shipped by this repository; never recursively delete a user folder.
    target.mkdir(parents=True, exist_ok=True)
    for p in source.rglob("*"):
        if p.is_file():
            dest = target / p.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
    return target


def cli(name):
    result = shutil.which(name)
    if not result:
        raise RuntimeError(
            name + " CLI is not installed; use the printed configuration manually"
        )
    return result


def register(client, name, command, args):
    executable = cli(client)
    if (
        subprocess.run(
            [executable, "mcp", "get", name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    ):
        print("Kept existing MCP registration: " + name)
        return
    subprocess.run([executable, "mcp", "add", name, "--", command, *args], check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--client", choices=["codex", "claude", "generic"], default="codex")
    p.add_argument("--skill-dir", type=Path)
    p.add_argument("--update", action="store_true")
    p.add_argument("--register", action="store_true")
    p.add_argument("--audio", action="store_true")
    p.add_argument("--skip-deps", action="store_true")
    a = p.parse_args()
    if a.client == "generic" and not a.skill_dir:
        p.error("--client generic requires --skill-dir")
    target = (
        a.skill_dir
        or Path.home()
        / (".claude/skills" if a.client == "claude" else ".agents/skills")
        / "after-effects-workflow"
    )
    print("Installed skill: " + str(install_skill(target, a.update)))
    servers = {
        "aftereffects": {
            "command": "npx",
            "args": ["-y", "@kumoproductions/mcp-aftereffects@0.3.1"],
        }
    }
    if a.audio:
        env = ROOT / ".venv-audio"
        venv.EnvBuilder(with_pip=True).create(env)
        python = env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        if not a.skip_deps:
            subprocess.run(
                [
                    str(python),
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    str(ROOT / "requirements.txt"),
                ],
                check=True,
            )
        servers["ae-sound-design"] = {
            "command": str(python),
            "args": [str(ROOT / "audio/server.py")],
        }
    print(json.dumps({"mcpServers": servers}, indent=2))
    if a.register:
        if a.client == "generic":
            p.error("Generic clients need manual MCP configuration")
        for name, spec in servers.items():
            register(a.client, name, spec["command"], spec["args"])
    print(
        "Reconnect your client, open AE, then verify project inspection. No project was edited or rendered."
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as e:
        raise SystemExit(str(e))
