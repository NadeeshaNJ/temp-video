# Ranger video: Drift working folder

Everything needed to keep editing the Ranger main video in CutWire Drift.

| Path | What it is |
|---|---|
| `ranger_main.drift` | The Drift project, **packaged with all media inside**. Open this in Drift (File → Open). It does not need the folders below. |
| `assets/` | Every media file the timeline uses, as loose files (PNG graphics, WebM footage cards with transparency, hook and network MP4s, music and sound effect WAVs). Use these to swap or re-import a piece. |
| `assets_lossless/` | Lossless FFV1 versions (`.mkv`, with transparency) of the 8 footage cards and the Wi-Fi link. The project uses the smaller WebM copies; replace a clip's source with the `.mkv` in Drift if you want the highest quality. |
| `build_tools/` | Python scripts that made the assets and laid out the timeline (see below). |

The finished renders are in `../exports/`.

## Timeline layout (top to bottom)

| Lane | Type | Used for |
|---|---|---|
| 0 to 3 | Text | Captions (0), kickers and second lines (1), list lines (2), "How it works" label (3) |
| 4 | Graphic | Corner QR code |
| 5 | Graphic | OLED screens in the phone scene, end-card QR |
| 6 | Video | Footage cards, Wi-Fi link |
| 7, 8 | Graphic | OLED screens, phones, icons, hero images (two lanes so they can overlap) |
| 9 | Video | Full-frame hook and network animations |
| 10 | Graphic | Dark background plate |
| 11, 12 | Audio | Sound effects (blips, chirps, pops, whooshes) |
| 13 | Audio | Real "Ranger" startup voice |
| 14 | Audio | Music |

Project: 1920x1080, 30 fps, 130 s. Colours: background `#0E1210` to `#1C221F`,
green `#2F6D4F` (text accent `#7CC4A0`), SOS red `#B3261E`. Font: Inter.

## Rebuilding from scratch

1. `kit.py`, `anim.py`, `audio.py` (and `cut.py` for the background-removed photos, needs `rembg`)
   write the assets.
2. Start Drift headless: `drift --headless --mcp-port 4731` (on a server with no screen:
   `QT_QPA_PLATFORM=xcb xvfb-run -a drift --headless --mcp-port 4731`).
3. `build.py` uses `drift_cli.py` and `keyframes.py` from the `cutwire-drift` skill
   (CutWire-Studios/Drift-SKILL) and lays out the whole timeline.

The scripts still use the paths of the session where they were made; change `W`, `A`
and `SKILL` at the top of each script to your own folders first.
