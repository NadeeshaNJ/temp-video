# RANGER: Video Brief and Production Kit

> **For the video editing agent:** this file is your complete brief. It describes the product, its features, the audience and the story. It also gives a scene-by-scene storyboard with voice-over, and a list of every asset in this folder with what to do with it (crop, remove background, overlay, animate). Read it top to bottom before editing. All paths are relative to this folder.

---

## 1. The product in one breath

**Ranger is a pocket-sized radio messenger that works when everything else is down.**
It needs no cell towers, no SIM, no internet and no subscription. Rangers talk directly to each other over long-range LoRa radio, so you can send encrypted text messages, push-to-talk voice, live GPS locations and an SOS. They also pass messages along for each other, which extends the reach. Any smartphone can join a Ranger over Wi-Fi and use the network from its browser, with no app.

**Tagline options** (pick one for the title card and end card):
- *"When the network goes down, Ranger keeps you connected."*
- *"No towers. No SIM. No silence."*
- *"Your team's lifeline, off the grid."*

---

## 2. Why it matters (the story hook)

Cell networks fail exactly when people need them most: floods, landslides, earthquakes, blackouts, remote trails, or networks being shut down. Walkie-talkies have no privacy, because anyone can listen in, and they can't tell you *where* your team is.

Ranger fixes all of that:

| Problem | Ranger's answer |
|---|---|
| Towers and power go down in a disaster | Device-to-device radio; every Ranger also relays for the others |
| Networks can be throttled or shut off | No infrastructure to switch off |
| SIMs, plans, monthly bills | Free to use forever |
| Walkie-talkies can be overheard | AES-128 encryption on every packet (tamper and replay protected) |
| "Where are you?" | Live GPS sharing, compass arrow, distance, plus radio ranging when there is no GPS |
| Not everyone has a Ranger | Up to 3 phones per Ranger join over Wi-Fi, no app needed |

---

## 3. Who it is for: where it is useful

Use these as quick B-roll captions or a montage of use cases:

1. **Disaster response and rescue teams**: coordinate search teams in flood or earthquake zones after the towers fail. SOS with location.
2. **Families and communities**: a Ranger in every home becomes an instant neighbourhood network in a blackout.
3. **Hikers, campers and expeditions**: stay in touch and find each other on trails with no coverage.
4. **Field work**: surveyors, farmers, forestry, wildlife and research teams in remote areas.
5. **Events and security**: private, encrypted team chat and voice at festivals, sites and campuses.
6. **Volunteers and NGOs**: a cheap, rugged, subscription-free network that anyone can carry.

---

## 4. Tone and style
- **Content** Always try to use more videos an images with animations in the video instead of lots of words and paragraphes. when using words try to stick with list structure
- **Mood:** confident, hopeful, a little cinematic. Start tense (a disaster or no signal), then resolve into empowerment and calm control.
- **Pace:** quick cuts (1.5–3 s) in the hook and the feature montage. Slower (4–6 s) on how-to steps so viewers can follow.
- **Look:** dark backgrounds that let the white OLED pixels glow. Accent colour **forest green `#2F6D4F`** (the phone page's colour) with **alert red `#B3261E`** only for SOS.
- **Typography:** clean geometric sans (e.g. Inter, Montserrat). Large, short captions of 6 words or fewer.
- **Music:** modern cinematic or electronic with a pulse. Dark and sparse in the hook, building at the reveal, upbeat in the features, warm at the end.
- **Sound design:** soft UI "blip" on each OLED screen change. Radio "chirp" whooshes when a message flies between devices. Use the real Ranger startup voice at the product reveal (see §8).

---

## 5. Storyboard (main video, about 2:00)

Each scene lists: **visuals** (asset files), **on-screen text**, **voice-over (VO)**, and **editing notes**.
Times are targets; stretch or trim to the music.

### Scene 1: Hook: "No signal" (0:00–0:10)
- **Visuals:** dark stock-style mood: a phone showing "No Service" or an SOS-only status bar, rain, a flicker or blackout (generate or use simple motion graphics if no footage exists).
- **Text:** `No signal.` → `No internet.` → `No help?`
- **VO:** "When disaster strikes, the first thing to go is the network."
- **Notes:** desaturated, slow push-in, low drone sound.

### Scene 2: Reveal (0:10–0:20)
- **Visuals:** `raw_footage/` hero shot of the device (best-lit photo or video of the Ranger), or `product_images/Top_3D.png` with a slow 3D-like parallax. Cut to `oled_screens/black_background/01_startup_logo.png` glowing on.
- **Audio:** play `audio/ranger_startup_voice_8khz.wav` ("Ranger") exactly as the logo appears.
- **Text:** `RANGER`, then the tagline.
- **VO:** "Meet Ranger. A radio messenger that works with no towers, no SIM, and no internet."
- **Notes:** remove the background from the device photo (§9), place it on a dark mat color with a soft green rim light.

### Scene 3: How it works (0:20–0:32)
- **Visuals:** motion graphic: 3 Ranger devices as icons spread on a map. A message hops Ranger → Ranger (relay) with radio-wave rings. A small lock icon on each packet.
- **Text:** `Device to device` · `Relays for each other` · `Encrypted`
- **VO:** "Rangers talk straight to each other over long-range LoRa radio, and pass messages on for each other, encrypted end to end."

### Scene 4: Feature montage (0:32–1:20), about 6 s per feature
For each feature, show the device or hands footage, then a picture-in-picture or full-screen **OLED screen PNG**, with a short caption.

| # | Feature | OLED / phone asset | Caption | VO line |
|---|---|---|---|---|
| 4a | Find your people | `04_people_list.png` | `See who's nearby` | "See everyone in range at a glance." |
| 4b | Text messaging | `17_chat.png` → `18_chat_typing_t9.png` | `Text without towers` | "Send messages to one person or to everyone, with delivery confirmations." |
| 4c | Push-to-talk voice | `21_talk_ready.png` → `22_talk_talking.png` | `Hold to talk` | "Hold VOICE to talk, like a walkie-talkie, but private." |
| 4d | Track and navigate | `07_track_gps_compass.png` | `Arrow points to them` | "Track a teammate: the arrow points the way and shows the distance." |
| 4e | No GPS? Radio ranging | `08_track_radio_ranging_no_gps.png` | `Distance by radio` | "No GPS? Ranger measures distance using the radio signal itself." |
| 4f | Your location | `10_location_gps_compass.png` → `15_location_shared.png` | `Share your position` | "Check your coordinates and compass, and share your position in one press." |
| 4g | SOS | `19_broadcast.png` → `20_broadcast_sos_sent.png` | `SOS to everyone` (red) | "In an emergency, one press sends an SOS with your location to every Ranger." |
| 4h | Long battery | `26_settings_auto_sleep.png` (then fade to black) | `Sleeps, still listening` | "It sleeps to save power, and wakes the instant a message arrives." |

**Notes:** animate OLED screens with a quick "power-on" (scale 98%→100%, brightness 0→100% over 6 frames). Add the blip sound. Each screen should sit *inside* the device's display area when footage allows (§9.3).

### Scene 5: Phones join the network (1:20–1:45)
- **Visuals:** a phone next to the Ranger. Sequence through `phone_screens/` (light or dark, keep it consistent):
  `01_join_enter_name` → `02_messages_everyone` → `03_messages_private_chat` → `04_people_distance_direction` → `05_sos_share_location_phone_gps` → `06_gps_page_sharing_phone_location`. In parallel, show `oled_screens/.../25_settings_phone_wifi_on.png` and `05_people_list_phone_selected.png` (the phone appears as "Nimal@R1" on every Ranger).
- **Text:** `No app. Just Wi-Fi.` → `Your phone joins the network` → `Lend your phone's GPS & clock`
- **VO:** "Don't have a Ranger? Join one with your phone. Connect to its Wi-Fi, type your name, and you're on the network: messages, people, SOS, all in the browser. Your phone can even lend the Ranger its GPS and clock."
- **Notes:** place screenshots inside a clean phone mockup frame with a soft shadow. Animate scrolling or tapping with a simple finger-tap ripple.

### Scene 6: Use cases montage (1:45–1:55)
- **Visuals:** quick 1.5 s cuts with captions from §3 (rescue teams, families, hikers, field workers, events). Use footage or photos from `raw_footage/` where suitable; otherwise generated or stock imagery and simple icons.
- **VO:** "For rescue teams, families, hikers and field crews: anywhere the network can't reach."

### Scene 7: End card (1:55–2:05)
- **Visuals:** device hero shot (background removed) on dark gradient + `01_startup_logo.png` glow.
- **QR code (required):** place `qr_code/qr_end_card_nadeeshanj_ranger.png` (white rounded card, QR + "nadeeshanj.dev/ranger") on the right third of the frame, devices on the left. Keep it on screen for **at least 4 seconds** and at least **25% of the frame height** so a phone can scan it from the video. Pop it in with a quick scale (90%→100%, 8 frames) and a soft shadow. Never recolour, invert, crop or blur the QR itself.
- **Text:** tagline + `nadeeshanj.dev/ranger` + `Hackster: hackster.io/nadeeshanj/ranger-421e83` + `Open-source hardware & firmware` (optional).
- **VO:** "Ranger. When the network goes down, you stay connected. Scan the code to see how it's built."

### Short version (about 30 s, vertical 9:16, for Reels, TikTok and Shorts)
Scene 1 (3 s) → Scene 2 (4 s, with the startup voice) → 4b, 4d, 4g, 5 (about 4 s each, captions only, no VO needed) → End card with the QR code (5 s, QR at least 30% of the frame width in 9:16).

**Corner QR (optional, both versions):** during the feature montage and the phone scene, a small `qr_code/qr_nadeeshanj_ranger_dark.png` (about 12% of the frame height, white card behind it, bottom-right, 80% opacity) with `nadeeshanj.dev/ranger` under it.

---

## 6. How to use Ranger (instructional section)

Use this section for the "how-to" part of the video, on-screen callouts, or a separate tutorial video. Each step lists the OLED screen to show.

### 6.1 The controls

Point at these on `product_images/Top_3D.png` or the real device with animated callout lines:

| Control | What it does |
|---|---|
| **Power switch** (ON/OFF, top right) | Turns the Ranger on. It greets you by saying **"Ranger"** and shows the logo. |
| **Knob: turn** | Moves through lists. **On the main menu, it changes the volume.** |
| **Knob: press** | Select / OK. While typing: **send**. |
| **Knob: hold 1.5 s** | Low-power mode (screen off, radio still listening). Press again to wake. |
| **Key 2 / 8** | Up / Down |
| **Key 4 / 6** | Back (left) / Action (right) |
| **Key 5** | Select (Enter) |
| **Keys 0–9** | Type letters, old-phone style (T9 multi-tap) |
| **VOICE button** (big, bottom left) | Hold to talk, release to listen |

### 6.2 Getting started
1. Slide the power switch to **ON**. You'll hear "Ranger" → `01_startup_logo.png`.
2. The **main menu** appears: People, Location, Messages, Broadcast, Settings → `02_main_menu.png`.
3. Turn the knob to set the volume → `03_main_menu_volume_knob.png`.
4. The top bar always shows GPS signal (left), time (centre) and battery (right).

### 6.3 Find people and act on them
1. Main menu → **People** → `04_people_list.png`. A pin icon means that person is sharing a GPS position.
2. Select a person → **Track / Ping / Message / Share / Talk** → `06_person_actions.png`.

### 6.4 Send a text message
1. People → person → **Message**, or **Messages** for past chats → `16_messages_list.png` (a dot means unread).
2. Open a chat → `17_chat.png`. Press select to **Reply**.
3. Type with the number keys: press **2** once for *a*, twice for *b*, three times for *c* → `18_chat_typing_t9.png`.
   - **Knob left** = delete a letter. **Knob press** = send. **Hold 4** = go back (your draft is kept).
4. Messages are confirmed when delivered; if someone is out of reach, Ranger retries.

### 6.5 Talk (push-to-talk)
1. **Hold VOICE** on anyone's screen to talk to that person; from the main menu it talks to everyone → `21_talk_ready.png`, `22_talk_talking.png`, `23_talk_everyone.png`.
2. Release to listen. A beep marks the start and end.

### 6.6 Track a teammate
1. People → person → **Track** → `07_track_gps_compass.png`.
2. The **arrow points to them** as you turn, with the distance and compass bearing. Bars show the signal.
3. Without GPS, Ranger measures the distance by **radio time-of-flight** ("~42m", "RF 42m") → `08_track_radio_ranging_no_gps.png`.
4. Press **6** to **Ping** them → `09_track_ping_sent.png`.

### 6.7 Your location and compass
1. Main menu → **Location** → `10_location_gps_compass.png`: your coordinates on the left, compass on the right.
2. Press **6** to share your location with everyone → `15_location_shared.png`.
3. First time: press **0** and turn the Ranger one full round, held flat, to calibrate the compass → `13_location_compass_calibrate.png`.
4. Point the Ranger to true north and press **8** to set north → `14_location_north_set.png`.
5. No GPS signal yet → `12_location_no_fix.png`. With a phone's GPS → `11_location_gps_from_phone.png`.

### 6.8 Broadcast and SOS
1. Main menu → **Broadcast** → **Talk**, **Message** or **SOS** to everyone → `19_broadcast.png`.
2. **SOS** sends an alert with your position to every Ranger, with an alarm tone → `20_broadcast_sos_sent.png`.

### 6.9 Settings
Main menu → **Settings** → `24_settings.png`. Select a row to edit it (`<value>`), turn the knob to change it, then select again to save.
- **Volume** 0–100 · **Brightness** 1–5 · **Channel** 0–15 (radio frequency; all team devices must match)
- **Auto sleep**: 5 min / Off → `26_settings_auto_sleep.png`
- **Phone WiFi**: On / Off (off by default) → `25_settings_phone_wifi_on.png`

### 6.10 Low-power mode
- **Hold the knob 1.5 s**: the screen turns off and Ranger sleeps, but **the radio keeps listening**.
- It wakes on a **knob press** or when **a message arrives**.
- With Auto sleep on, it sleeps by itself after **5 minutes** without a key press.

### 6.11 Phones: join a Ranger with your phone (no app)
1. On the Ranger: **Settings → Phone WiFi → On** → `25_settings_phone_wifi_on.png`.
2. On the phone: open Wi-Fi and join the network named after the Ranger, e.g. **"Ranger-1"** (open network).
3. A sign-in page pops up, or open **http://192.168.4.1** in Safari or Chrome. Type your name and tap **Join** → `phone_screens/01_join_enter_name_*.png`.
4. **Messages tab**: chat with everyone or pick a person from the list. You'll see *sending → delivered* → `02_messages_everyone_*.png`, `03_messages_private_chat_*.png`.
5. **People tab**: everyone on the network with distance, direction and signal → `04_people_distance_direction_*.png`.
6. **SOS tab**: **Share location**, **Send SOS**, or **Use this phone's GPS** → `05_sos_share_location_phone_gps_*.png`.
7. Your phone shows up on every Ranger as **"YourName@R1"** (name @ which Ranger you joined) → `oled_screens/.../05_people_list_phone_selected.png`.
8. **Lend your GPS:** tap **Open GPS page**, accept the certificate warning once, allow location and keep the page open → `06_gps_page_sharing_phone_location_*.png`. The Ranger now knows where it is and shows "GPS from a phone" (`11_location_gps_from_phone.png`). The phone also sets the Ranger's **clock** automatically.
- Up to **3 phones** per Ranger. Phones that leave the Wi-Fi are removed from People automatically.
- **iPhone tips** (good as a small on-screen note): Settings → Privacy → Location Services → *Safari Websites* → **While Using** and **Precise** on. In Wi-Fi → (i) → *Private Wi-Fi Address* set to **Fixed**.

---

## 7. Key facts and specs (for captions, lower-thirds and an optional spec card)

- **Radio:** 2.4 GHz LoRa (Semtech SX1280) with power amplifier; built for kilometre-range links in open terrain
- **Network:** device-to-device; every Ranger relays for others; up to 16 channels
- **Security:** AES-128-CCM encryption, with fake and replayed packets rejected; team key from a shared passphrase
- **Messaging:** text (private or everyone, with delivery confirmation), push-to-talk digital voice, ping, SOS
- **Location:** GPS, digital compass, live tracking arrow; **radio time-of-flight ranging** without GPS
- **Phones:** built-in Wi-Fi hotspot, browser page, up to 3 phones, no app or internet; phones can lend GPS and time
- **Display and controls:** 0.96" OLED (128×64), T9 keypad, rotary knob, push-to-talk button
- **Brain:** ESP32 dual-core; custom PCB with USB-C charging
- **Power:** low-power sleep with the radio still listening; auto-sleep after 5 minutes
- **Cost to use:** zero: no SIM, no plan, no infrastructure

> Do not invent other numbers (battery hours, exact km range, weight, price). If a spec card needs them, leave a placeholder like `[__ km]`.

---

## 8. Asset manifest

```
Ranger_Video_Kit/
├── VIDEO_BRIEF.md                ← this file
├── cover_images/                finished covers (Hackster 4:3, clean 4:3, 16:9): thumbnail or end-card backgrounds
├── qr_code/
│   ├── qr_end_card_nadeeshanj_ranger.png       QR on a white rounded card + "nadeeshanj.dev/ranger" (end card)
│   ├── qr_nadeeshanj_ranger_dark.png           plain QR (corner overlay)
│   └── qr_nadeeshanj_ranger_black_on_white.png plain QR, maximum contrast
├── audio/
│   └── ranger_startup_voice_8khz.wav   the real "Ranger" power-on voice (1 s)
├── oled_screens/
│   ├── black_background/         27 OLED screens, 1024×512 PNG, black bg, pixel-glow look
│   └── transparent_overlay/      the same 27 screens, white pixels on transparent (alpha) for compositing
├── phone_screens/                phone web page screenshots, 1170×2532 PNG (iPhone size), _light and _dark
│   └── html_source/              the real phone page as standalone HTML (open in a browser to screen-record or scroll)
├── product_images/               3D renders, PCB, schematic, first prototype, early screen photo
└── raw_footage/
    ├── videos/                   ← the owner's real device videos (to crop or clean up)
    └── photos/                   ← the owner's real device photos (to crop or remove backgrounds)
```

### 8.1 OLED screens (rendered from the real firmware, pixel-exact)
| File | Shows |
|---|---|
| 01_startup_logo | Boot logo "RANGER" (pair with the startup voice) |
| 02_main_menu | Main menu: People, Location, Messages, Broadcast, Settings |
| 03_main_menu_volume_knob | Turning the knob on the main menu: "Volume 75" |
| 04_people_list | People nearby; pin = has GPS, plus message and mic icons |
| 05_people_list_phone_selected | A phone user "Nimal@R1" selected in People |
| 06_person_actions | Track / Ping / Message / Share / Talk |
| 07_track_gps_compass | Tracking Kasun: 1.2 km, SW 205°, arrow, signal bars |
| 08_track_radio_ranging_no_gps | Tracking without GPS: radio distance ~42 m |
| 09_track_ping_sent | "Ping sent" pop-up |
| 10_location_gps_compass | Own coordinates + compass needle (25° NE) |
| 11_location_gps_from_phone | Position borrowed from a phone: "GPS from a phone" |
| 12_location_no_fix | Searching for GPS |
| 13_location_compass_calibrate | "Turn me 1 round flat" compass calibration |
| 14_location_north_set | "North set" pop-up |
| 15_location_shared | "Location sent" pop-up |
| 16_messages_list | Chat list with times and unread dot |
| 17_chat | A conversation (mine on the right) |
| 18_chat_typing_t9 | Typing a reply with T9: `<Del · Send · 4:Back` |
| 19_broadcast | Broadcast: Talk / Message / SOS |
| 20_broadcast_sos_sent | "SOS sent" pop-up |
| 21_talk_ready | "Hold VOICE to talk" |
| 22_talk_talking | TALKING 0:07 to Kasun |
| 23_talk_everyone | TALKING to Everyone |
| 24_settings | Settings list |
| 25_settings_phone_wifi_on | Editing Phone WiFi `<On>` |
| 26_settings_auto_sleep | Editing Auto sleep `<5 min>` |
| 27_people_empty | "No one nearby" |

### 8.2 Phone screens (from the real page served by the Ranger)
| File | Shows |
|---|---|
| 01_join_enter_name | Join page: enter a name |
| 02_messages_everyone | Group chat to Everyone, typing "On my way" |
| 03_messages_private_chat | Private chat with Kasun (sending / delivered) |
| 04_people_distance_direction | People: distance, direction, radio distance, signal, "here" |
| 05_sos_share_location_phone_gps | Share location, Send SOS (red), Use this phone's GPS |
| 06_gps_page_sharing_phone_location | "Sharing your position" ±12 m |

Use **one theme consistently** (dark matches the OLED mood; light reads better on small screens).

### 8.3 Product images
| File | Use |
|---|---|
| Top_3D.png | Hero render, front: OLED, keypad, VOICE button, knob. Use for the controls callout (§6.1). |
| Bottom_3D.png | Back: ESP32, radio module, USB-C ("under the hood" shot) |
| PCB_design.png | PCB layout: "custom-designed hardware" B-roll |
| Esp32_schematic.png | Schematic: quick engineering flash (1 s, with a slow zoom) |
| First_Setup.jpeg | Breadboard prototype: "from prototype…" (before/after with the finished device) |
| tracker_screen.jpeg | Early OLED tracking screen on a breadboard: crop to the screen |

---

## 9. Editing instructions for the raw footage and photos

The owner will place real footage in `raw_footage/videos/` and `raw_footage/photos/`. These are **unedited phone recordings and photos**: expect clutter (desk, cables, breadboard), uneven light and vertical framing.

### 9.1 For every photo
1. **Inspect** each file and choose the best 1–3 hero shots of the device (sharp, screen visible, good angle).
2. **Remove the background** (subject = device + hands if present). Keep clean edges around the antenna and the OLED. Export as PNG with alpha.
3. **Crop** tightly to the device; leave about 8% margin. Make 16:9 and 9:16 versions.
4. **Colour:** lift shadows slightly, neutral white balance, add a little clarity. Keep the OLED pixels pure white, not blown into a blob.
5. Place on a **dark gradient** (`#0E1210` → `#1C221F`) with a subtle green rim light and a soft floor shadow.
6. Add a gentle **Ken Burns** move (3–5% zoom, slight pan) when used as stills in the video.

### 9.2 For every video clip
1. **Trim** to the useful action: pressing keys, turning the knob, a message arriving, the screen changing, the startup voice.
2. **Crop or reframe** to the device (16:9 main, 9:16 short). Track the device if the camera moves.
3. **Stabilise** handheld shots.
4. **Background:** blur or darken distracting backgrounds, or rotoscope the device onto the dark gradient for hero moments.
5. Keep the **original audio** where the device speaks ("Ranger") or beeps; duck the music under it.
6. Speed ramps are fine for B-roll; keep how-to actions at real speed.

### 9.3 Putting OLED screens on the real device
- Where the device's screen is visible but blurry, glare-washed or showing the wrong screen, **replace the screen** with the matching PNG from `oled_screens/transparent_overlay/`. Corner-pin it to the display (aspect 2:1), add a 1–2 px blur and a soft glow so it looks emissive, not pasted.
- For full-screen feature shots, use `oled_screens/black_background/` scaled up on a black frame with slow push-in. The pixel-gap texture is intentional (real OLED look); keep **nearest-neighbour or no resampling blur** if scaling further.
- The OLED is **monochrome white on black**. Do not colourise it.

### 9.4 Phone screenshots
- Put them in a modern **phone frame mockup** (rounded, thin bezel), or float them with rounded corners (radius about 5% of the width) and a soft shadow.
- Show a phone and a Ranger side by side when the phone joins (Scene 5) to make the link obvious; draw a subtle animated Wi-Fi arc between them.

---

## 10. Audio and voice-over

- **VO voice:** warm, confident, clear (male or female); neutral or British English accent fits the startup voice.
- **Startup voice:** `audio/ranger_startup_voice_8khz.wav` is the real power-on sound of the device. Use it at the reveal (Scene 2) and optionally the end card. It is 8 kHz; it is meant to sound like it comes from the device's small speaker. *Licence note:* it was generated with a Piper TTS voice whose training data is "all rights reserved" (Mycroft AI). For a public or commercial upload, the owner may prefer to **re-record "Ranger"** or use a licence-clear TTS voice, with the same deep, slow, about 1 s delivery.
- **Music:** royalty-free cinematic or electronic track, 100–120 BPM, with a clear build at 0:10 (the reveal).
- **Mix:** VO at −14 LUFS integrated for the master; music ducked −10 dB under VO.

---

## 11. Captions and export

- Burn-in captions for the short version; supply an `.srt` for the main version.
- **Main:** 1920×1080 (or 3840×2160), 30 fps, H.264/H.265, high bitrate.
- **Short:** 1080×1920, 30 fps, 30 s max.
- **Thumbnail:** device hero (background removed) + glowing OLED + text "WORKS WITHOUT SIGNAL" in large bold type, with a green accent.

---

## 12. Accuracy guardrails (please respect these)

- **Links:** the website is **https://nadeeshanj.dev/ranger** (what the QR code opens); the Hackster project is **https://www.hackster.io/nadeeshanj/ranger-421e83**. Use these exactly.

- The phone feature is a **web page served by the Ranger**; there is **no app** to download, and phones need **no internet or mobile data**.
- Phones talk to their own Ranger over Wi-Fi; **Ranger-to-Ranger is radio** (LoRa). Don't show phones talking to each other directly over long distances.
- Voice is **push-to-talk** (one person at a time), not a phone call.
- A Ranger that borrows a phone's GPS uses it for **itself**. Other Rangers get the time from the network, but each uses its own position.
- Don't claim certifications, waterproofing, battery life, exact range, weight or price.
