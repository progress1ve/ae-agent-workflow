"""Offline word timestamps with cached Whisper; writes full data, returns brief metadata."""

import argparse
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from faster_whisper import WhisperModel

p = argparse.ArgumentParser()
p.add_argument("--file", required=True)
p.add_argument("--output", required=True)
p.add_argument("--language", default="en")
a = p.parse_args()
raw = subprocess.run(
    [
        imageio_ffmpeg.get_ffmpeg_exe(),
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        a.file,
        "-vn",
        "-ar",
        "16000",
        "-ac",
        "1",
        "-f",
        "f32le",
        "pipe:1",
    ],
    stdout=subprocess.PIPE,
    check=True,
).stdout
x = np.frombuffer(raw, dtype=np.float32)
m = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=6)
segments, _ = m.transcribe(
    x, language=a.language, word_timestamps=True, beam_size=5, vad_filter=False
)
words = [
    {
        "word": w.word.strip(),
        "start": w.start,
        "end": w.end,
        "probability": w.probability,
    }
    for s in segments
    for w in s.words
]
Path(a.output).parent.mkdir(parents=True, exist_ok=True)
Path(a.output).write_text(
    json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(
    json.dumps(
        {
            "duration": len(x) / 16000,
            "words": len(words),
            "transcript": " ".join(w["word"] for w in words)[:500],
            "timings_file": a.output,
        },
        ensure_ascii=True,
    )
)
