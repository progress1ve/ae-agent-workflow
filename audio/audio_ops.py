"""Local sound-design operations: inspect, trim, filter, pan and mix a cue timeline."""

import argparse
import json
from math import gcd
from pathlib import Path

import numpy as np
import soundfile as sf
from pedalboard import Compressor, HighpassFilter, Limiter, LowpassFilter, Pedalboard
from scipy.signal import resample_poly

RATE = 48000


def read(p):
    x, sr = sf.read(p, always_2d=True, dtype="float32")
    if sr != RATE:
        x = resample_poly(x, RATE // gcd(sr, RATE), sr // gcd(sr, RATE), axis=0)
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    return x[:, :2]


def stats(p):
    x = read(p)
    pk = float(np.max(np.abs(x)))
    rms = float(np.sqrt(np.mean(x * x)))
    return {
        "file": str(p),
        "seconds": len(x) / RATE,
        "peak_db": round(20 * np.log10(max(pk, 1e-9)), 1),
        "rms_db": round(20 * np.log10(max(rms, 1e-9)), 1),
    }


def render(timeline, out, voice=None):
    timeline = Path(timeline).resolve()
    plan = json.loads(timeline.read_text(encoding="utf-8-sig"))
    if not 0 < float(plan["duration"]) <= 3600:
        raise ValueError("Duration must be between zero and3600 seconds")
    mix = np.zeros((int(plan["duration"] * RATE), 2), np.float32)
    for cue in plan["cues"]:
        if not 0 <= cue["time"] < plan["duration"] or cue["length"] <= 0:
            raise ValueError("Cue start/length outside timeline")
        path = Path(cue["file"])
        path = path if path.is_absolute() else timeline.parent / path
        x = read(path)
        if len(x) == 0:
            raise ValueError("Empty cue audio")
        mag = np.max(np.abs(x), axis=1)
        ids = np.flatnonzero(mag > max(float(mag.max()) * 0.02, 0.0001))
        start = max(0, int(ids[0]) - int(0.015 * RATE)) if len(ids) else 0
        x = x[start : start + int(cue["length"] * RATE)]
        board = Pedalboard(
            [
                HighpassFilter(cue.get("highpass", 100)),
                LowpassFilter(cue.get("lowpass", 10000)),
            ]
        )
        x = board(x.T, RATE).T
        x *= 10 ** (cue["peak_db"] / 20) / max(float(np.max(np.abs(x))), 1e-6)
        fade = min(int(0.025 * RATE), len(x) // 4)
        x[:fade] *= np.linspace(0, 1, fade)[:, None]
        tail = min(int(0.13 * RATE), len(x) // 3)
        x[-tail:] *= np.linspace(1, 0, tail)[:, None]
        if cue.get("pan") == "left-to-center":
            pan = np.linspace(-0.85, 0, len(x))
            mono = x.mean(axis=1)
            x = np.stack(
                [
                    mono * np.cos((pan + 1) * np.pi / 4),
                    mono * np.sin((pan + 1) * np.pi / 4),
                ],
                axis=1,
            )
        pos = int(cue["time"] * RATE)
        n = min(len(x), len(mix) - pos)
        mix[pos : pos + n] += x[:n]
    if voice:
        x = read(voice)
        x = Pedalboard(
            [
                HighpassFilter(75),
                Compressor(threshold_db=-18, ratio=2.5),
                Limiter(threshold_db=-3),
            ]
        )(x.T, RATE).T
        n = min(len(x), len(mix))
        mix[:n] += x[:n]
    mix = Pedalboard([Limiter(threshold_db=-2)])(mix.T, RATE).T
    # Limiter threshold controls processing, not a guaranteed output ceiling.
    ceiling = 10 ** (-2 / 20)
    peak = float(np.max(np.abs(mix)))
    if peak > ceiling:
        mix *= ceiling / peak
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sf.write(out, mix, RATE, subtype="PCM_24")
    return stats(out)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--timeline")
    p.add_argument("--out")
    p.add_argument("--voice")
    p.add_argument("--inspect", nargs="*")
    a = p.parse_args()
    result = (
        [stats(x) for x in a.inspect]
        if a.inspect
        else render(a.timeline, a.out, a.voice)
    )
    print(json.dumps(result, ensure_ascii=True, indent=2))
