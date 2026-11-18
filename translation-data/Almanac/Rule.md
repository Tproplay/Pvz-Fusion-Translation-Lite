# Suburban Almanac Translation Rules

This document outlines the strict formatting, styling, and nomenclature rules for all files under `translation-data/Almanac/` (`LawnStringsTranslate.json`, `ZombieStringsTranslate.json`, and `DetailStringsTranslate.json`).

---

## 1. No Italics (`<i>` / `</i>`)
- **Strict Prohibition**: Never use `<i>` or `</i>` formatting tags in any plant or zombie name, title, introduction, or trait description.
- **Why**: Unity TextMeshPro handles malformed, nested, or unclosed italic tags unpredictably, often causing italic formatting to bleed across entire dialogue cards and UI windows.
- **Boss Titles**: Use clean underline tags `<u>...</u>` for boss titles without italics (e.g. `<u>Dr. Zomboss</u>`, `<u>Channeler Pozeidon</u>`).

---

## 2. Remove Redundant "Zombie" Suffix from Zombie Titles
- **No Redundant Suffix**: In `ZombieStringsTranslate.json`, remove redundant `" Zombie"` from the titles of hybrid, evolved, armored, and specialized zombies.
  - **Examples**:
    - `Ducky Tube Conehead` (not `Ducky Tube Conehead Zombie`)
    - `Frost Legion Blockhead` (not `Frost Legion Blockhead Zombie`)
    - `Dolphinhead Newspaper` (not `Dolphinhead Newspaper Zombie`)
    - `Olympic Pole Vaulter` (not `Olympic Pole Vaulting Zombie`)
    - `Giga Dolphin-nut` (not `Giga Dolphin-nut Zombie`)
    - `Tinfoilhead` (not `Tinfoilhead Zombie`)
    - `Zombizilla` (not `Zombizilla Zombie`)
    - `Bucknut-copter` (not `Bucknut-copter Zombie`)
    - `Giga Trident-nut Captain` (not `Giga Trident-nut Captain Zombie`)
    - `Superstar` (not `Superstar Zombie`)
    - `Miner` (not `Miner Zombie`)
- **Exceptions**: Only retain `"Zombie"` for:
  1. Base classic vanilla zombies (`Zombie`, `Flag Zombie`, `Conehead Zombie`, `Buckethead Zombie`, `Football Zombie`, etc.).
  2. Plant-based zombies where removing `"Zombie"` creates direct confusion with plant names (`Peashooter Zombie`, `Wall-nut Zombie`, `Squash Zombie`, `Jalapeno Zombie`, `Doom-shroom Zombie`, `Gatling Pea Zombie`, `Hypno Pepper Zombie`).

---

## 3. Spacing & Indentation
- **No Tab Characters (`\t`)**: Never use tab characters (`\t`) inside description or trait strings. Unity TextMeshPro's default tab stops are excessively wide, causing bullet points to indent into the center of the text box while subsequent wrapped lines return to the left margin. Use direct bullets (`<color=black>•</color>`) or spaces (`  `).
- **No Leading Newlines in Recipes (`cost`)**: The `cost` field must never begin with `\r` or `\n`. The game engine automatically injects vertical spacing between the description and fusion formula; leading newlines cause an awkward double-blank-line gap.
- **Travel Synergies**: Keep spacing to a single blank line (`\n<color=red>Travel Synergies:\n`).

---

## 4. Harvest Mode Plants (Seed IDs 300–313)
- **No Color Tags in `introduce`**: Strip all `<color=...>` tags from Harvest Mode plant introductions to preserve clean, unified styling.
- **Naming**: Always use **Harvest Mode** (never "Mystery Mode").
