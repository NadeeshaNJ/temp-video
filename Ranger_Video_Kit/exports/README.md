# Ranger main video: exports

Built in CutWire Drift 0.8.0 (nightly AppImage, run headless) with the
`cutwire-drift` skill from CutWire-Studios/Drift-SKILL, following `../VIDEO_BRIEF.md`.

| File | What it is |
|---|---|
| `ranger_main_1080p.mp4` | Main video, 1920x1080, 30 fps, 2:10, H.264 + AAC, mastered to -14 LUFS |
| `ranger_main.srt` | Captions file (the on-screen text, with times) |
| `ranger_thumbnail.jpg` | 1920x1080 thumbnail ("WORKS WITHOUT SIGNAL") |

## Scene timing

| Time | Scene |
|---|---|
| 0:00-0:10 | Hook: "No signal. / No internet. / No help?" (rain, phone with no service) |
| 0:10-0:20 | Reveal: device hero, then the OLED logo with the real "Ranger" startup voice |
| 0:20-0:32 | How it works: 3 Rangers, encrypted message relayed on a map |
| 0:32-1:20 | 8 features, each with real footage + the matching OLED screen |
| 1:20-1:44 | Phones join over Wi-Fi (dark phone screens + OLED screens) |
| 1:44-1:54 | Who it is for (6 quick cuts) |
| 1:54-2:00 | Breadboard, PCB, finished board |
| 2:00-2:10 | End card with the scannable QR (about 50% of frame height, 9 s on screen) |

## Notes

- No voice-over: no TTS key was available, so the story is told with short on-screen captions, as the brief prefers.
- Music and sound effects are synthesised by `../drift_project/build_tools/audio.py` (no licence needed).
- The startup voice clip is the kit's own file; see the licence note in the brief (section 10).

## Editing

The editable Drift project, its media and the build scripts are in `../drift_project/`.
