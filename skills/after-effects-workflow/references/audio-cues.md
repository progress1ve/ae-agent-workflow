# Local sound design

`audio/server.py` exposes three tools over stdio: `inspect_audio`, `mix_audio_timeline`, and `align_voice_words`. The first two require the base requirements; alignment additionally needs faster-whisper and downloads a model on first use. There are no API credentials.

```json
{
  "duration": 5,
  "cues": [
    {"time": 0.04, "file": "assets/whoosh.wav", "length": 0.28, "peak_db": -19},
    {"time": 3.55, "file": "assets/whoosh.wav", "length": 0.48, "peak_db": -10, "pan": "left-to-center"}
  ]
}
```

Each file path is resolved against the plan's directory. `time` and `length` are seconds. `peak_db` controls each processed cue before summation and limiting; it does not promise the encoded peak. Optional `highpass`/`lowpass` values are Hz. Leading silence is trimmed to the first measurable transient, with a short preroll; fades avoid clicks. The mixer runs at48kHz stereo and writes24-bit PCM WAV with a nominal-2dBFS ceiling.

The optional voice receives high-pass filtering and gentle compression before mixing. Check the result against the actual voice, particularly short high-frequency sounds. Increasing an effect by10dB before the limiter will not always produce10dB of perceived increase after summation.

If AE locks a WAV, mix to a new filename and relink it. Do not overwrite an open source. Source sound packs and generated voices are not distributed here.

Word alignment writes detailed timing JSON to disk and returns short metadata. Estimates can miss initial phonemes or extend beyond the apparent word. Use waveform/listening checks before trimming the final syllable. Silent-pause cuts are preferable to unnecessary speech speed changes.
