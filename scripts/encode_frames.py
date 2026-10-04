"""Encode a completed alpha-frame export; never drives or edits After Effects."""

import argparse
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--frames", type=Path, required=True)
    p.add_argument("--fps", type=float, required=True)
    p.add_argument("--audio", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    files = sorted(a.frames.glob("frame_*.png"))
    if not files or not (a.frames / "complete.json").exists():
        raise ValueError("Missing frames or completion marker")
    metadata = json.loads((a.frames / "complete.json").read_text())
    fps = metadata["fps"]
    if len(files) != metadata["frames"] or abs(a.fps - fps) > 0.0001:
        raise ValueError("Incomplete export or fps mismatch")
    digits = len(files[0].stem.split("_")[-1])
    size = None
    for i, f in enumerate(files):
        if f.name != f"frame_{i:0{digits}d}.png":
            raise ValueError("Frames must be contiguous from zero")
        with Image.open(f) as im:
            im.load()
            if im.mode != "RGBA":
                raise ValueError("Expected RGBA frames for alpha export")
            if size is None:
                size = im.size
            if im.size != size:
                raise ValueError("Frame dimensions differ")
    duration = len(files) / fps
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    outputs = {
        kind: a.out.with_name(a.out.name + suffix)
        for kind, suffix in [
            ("preview", "-preview.mp4"),
            ("chroma", "-chroma.mp4"),
            ("alpha", "-alpha.mov"),
        ]
    }
    if any(f.exists() for f in outputs.values()):
        raise ValueError("Choose a new output prefix; refusing to overwrite")
    seq = str(a.frames / f"frame_%0{digits}d.png")
    w, h = size
    for kind, out in outputs.items():
        cmd = [ff, "-hide_banner", "-loglevel", "error"]
        if kind != "alpha":
            cmd += [
                "-f",
                "lavfi",
                "-i",
                f"color=c={'black' if kind == 'preview' else '0x00FF00'}:s={w}x{h}:r={fps}:d={duration}",
            ]
        cmd += ["-framerate", str(fps), "-i", seq]
        video_idx = 0 if kind == "alpha" else 1
        if a.audio:
            cmd += ["-i", str(a.audio)]
        if kind != "alpha":
            cmd += [
                "-filter_complex",
                "[0:v][1:v]overlay=shortest=1:format=auto,format=yuv420p[v]",
                "-map",
                "[v]",
            ]
        else:
            cmd += ["-map", "0:v"]
        if a.audio:
            cmd += [
                "-map",
                f"{video_idx + 1}:a",
                "-af",
                f"apad,atrim=duration={duration}",
            ]
        if kind == "alpha":
            cmd += ["-c:v", "qtrle", "-pix_fmt", "argb", "-c:a", "pcm_s16le"]
        else:
            cmd += [
                "-c:v",
                "libx264",
                "-crf",
                "16",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-movflags",
                "+faststart",
            ]
        cmd += ["-t", str(duration), str(out)]
        subprocess.run(cmd, check=True)
    print(
        json.dumps(
            {
                "frames": len(files),
                "fps": fps,
                "size": size,
                "seconds": duration,
                "outputs": {k: str(v) for k, v in outputs.items()},
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
