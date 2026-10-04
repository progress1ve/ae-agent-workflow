"""Small local MCP bridge for sound design. No network or paid account."""

import json
import subprocess
import sys
from pathlib import Path

engine = Path(__file__).with_name("audio_ops.py")
defs = [
    {
        "name": "inspect_audio",
        "description": "Inspect up to 12 local audio files: duration, peak and RMS levels.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 12,
                }
            },
            "required": ["files"],
        },
    },
    {
        "name": "mix_audio_timeline",
        "description": "Mix a local JSON cue timeline: trim, filter, gain, fades, pan and limiter. Optional narrator WAV. Returns short audio metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "timeline": {"type": "string"},
                "output": {"type": "string"},
                "voice": {"type": "string"},
            },
            "required": ["timeline", "output"],
        },
    },
]
defs.append(
    {
        "name": "align_voice_words",
        "description": "Optional offline word timestamps. Requires faster-whisper; first use downloads a model. Writes detailed JSON and returns compact metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string"},
                "output": {"type": "string"},
                "language": {"type": "string", "default": "en"},
            },
            "required": ["file", "output"],
        },
    }
)
for line in sys.stdin:
    req = {}
    try:
        req = json.loads(line)
        ident = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        if ident is None:
            continue
        if method == "initialize":
            result = {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "local-sound-design", "version": "1.0"},
            }
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": defs}
        elif method == "tools/call":
            args = params["arguments"]
            name = params["name"]
            cmd = [sys.executable, str(engine)]
            if name == "inspect_audio":
                cmd += ["--inspect", *args["files"]]
            elif name == "mix_audio_timeline":
                cmd += ["--timeline", args["timeline"], "--out", args["output"]]
                if args.get("voice"):
                    cmd += ["--voice", args["voice"]]
            elif name == "align_voice_words":
                cmd = [
                    sys.executable,
                    str(engine.with_name("align_voice.py")),
                    "--file",
                    args["file"],
                    "--output",
                    args["output"],
                    "--language",
                    args.get("language", "en"),
                ]
            else:
                raise ValueError("Unknown audio tool")
            p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": p.stdout if p.returncode == 0 else p.stderr[-1800:],
                    }
                ],
                "isError": p.returncode != 0,
            }
        else:
            raise ValueError("Unsupported method")
        response = {"jsonrpc": "2.0", "id": ident, "result": result}
    except Exception as e:
        response = {
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "error": {"code": -32603, "message": str(e)},
        }
    print(json.dumps(response, ensure_ascii=True), flush=True)
