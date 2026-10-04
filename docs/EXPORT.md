# Export

Use the user's requested AE renderer when suitable. The included frame fallback is useful when headless rendering stalls. It is explicit and requires export authorization.

1. Save the project and identify its exact alpha composition.
2. Set `COMP_NAME` and a new `OUTPUT_DIR` in a copy of `scripts/export_frames.jsx`.
3. Run that reviewed JSX in AE. It writes numbered PNGs and a marker.
4. Encode after the marker exists and every expected frame is readable:

```bash
python scripts/encode_frames.py --frames output/frames --fps 30 --audio output/mix.wav --out output/deliverable
```

The script creates black-backed preview MP4, green-backed chroma MP4, and lossless qtrle alpha MOV. MOV is large by design; use another alpha codec when your delivery target needs it. MP4 does not carry alpha. Chroma encoding in4:2:0 can soften boundaries or shift pure green slightly; the alpha master avoids that keying loss.

Check decoded frame count, fps, dimensions, sound peaks, initial/hold/final alpha and safe edges. Listen to the final encoded file. Duration is derived from frame count/fps; avoid accidental voice-tail cuts. The JSX does not reopen a different project or call aerender automatically.
