# Ranger video, version 3 (expo cut)

1:27, 1920x1080, 30 fps, 75.5 MB. A fast, energetic cut for people walking past an expo stand:
what Ranger is, how it works, features, use cases and how it's built, in quick 1.5 to 3 s cuts.
The build section gives extra time to the work behind the device, especially the custom PCB.
Built in CutWire Drift 0.8.0 (headless) with the `cutwire-drift` skill.

| Path | What it is |
|---|---|
| `exports/ranger_v3_1080p.mp4` | Finished video, H.264 (CRF 12, near-lossless, straight from Drift) + AAC, -14.5 LUFS, 75.5 MB |
| `exports/ranger_v3.srt` | Subtitles of the voice-over |
| `drift_project/ranger_v3.drift` | Editable Drift project with all media packed inside |
| `drift_project/new_assets/` | New v3 media: sped-up scene clips, voice-over lines, music |
| `build_tools/` | `vo3.py` (voice-over), `audio3.py` (music), `build_v3.py` (timeline; uses `../v2/build_tools/build.py` helpers and the v1/v2 assets) |

## Scene timing

| Time | Section | Voice-over |
|---|---|---|
| 0:00-0:04.5 | Hook: three 1.5 s cuts (trail, collapsed building, phone in the rain) | "No signal. No network. No way to call for help." |
| 0:04.5-0:12 | Reveal: logo hit on the music drop, then the device | "Meet Ranger! A pocket radio that keeps you connected. No towers, no sim card, no internet!" |
| 0:12-0:24 | How it works: 8 km range, then the mesh map | "Rangers talk directly to each other over long range LoRa radio. Up to eight kilometers! And every Ranger relays for the others..." |
| 0:24-0:42 | Features, 3 s each: texts, push to talk, track, location, SOS, join from phone | One short line each |
| 0:42-0:53 | Use cases: rescue teams, remote patrols, lost hikers, anyone | One short line each |
| 0:53-0:55.5 | Breadboard prototype: "It started on a breadboard" | "It all started on a breadboard." |
| 0:55.5-0:58 | Schematic: "Schematic, designed from scratch" | "Then came the schematic, and a custom four-layer PCB, designed from scratch!" |
| 0:58-1:02 | The custom PCB layout, large with a slow push in: "Custom 4-layer PCB" | (continues) |
| 1:02-1:04.5 | Front and back 3D renders: "Designed & built by NadeeshaNJ" | (music) |
| 1:04.5-1:07 | The real assembled devices: "Real, working devices" | "From design, to real, working devices!" |
| 1:07-1:14.5 | What's inside: the six part cards | "Packed with an ESP32, a LoRa radio, GPS, and a battery that lasts for days on standby." |
| 1:14.5-1:17.5 | Cost flash: about Rs. 3,000 per unit (estimate) | "All for around three thousand rupees!" |
| 1:17.5-1:27.5 | End card with the QR code | "Ranger. Stay connected, anywhere. Scan the code to learn more!" |

## What changed from v2

- 3:15 cut down to 1:27: cuts are 1.5 to 3 s, and each part has only one short line.
- Voice-over is faster (1.15x) with short, punchy lines.
- New energetic music: a 4.5 s build into an impact on the logo, then a 120 BPM groove with claps, 16th-note hats and pumping bass.
- Hard cuts with a pop on each feature beat; whooshes between use cases.
- Dropped for time: the long range/data-rate explanation (202 kbps), the phone-join detail, the low-power feature, the "built for" stories' long lines, and the long parts narration.
- The build section is now 21.5 s and walks through the build journey: breadboard, schematic, the custom 4-layer PCB (the longest and largest shot), front and back renders, the real devices, then the parts.
