# news-image-20261122 — notes

This entry is a pure-stdlib Python program (`main.py`) that draws a
1024x1024 front-page image summing up Sunday 22 November 2026.
The page follows the previous days' shape: one wide lead story on
top, four stories in a 2x2 grid, and an also-today strip along the
bottom.

## The six stories (researched 2026-11-22 ~09:00 WIB, from that day's reporting)

1. MIDDLE EAST - GULF (lead): Iran's IRGC launches a combined
   missile and drone strike on US Patriot air-defence radars at
   military assets in Bahrain; multiple tankers are hit off the
   Oman coast as Iran-US naval tensions escalate.
2. UKRAINE - LVIV: A Russian missile strike hits Lviv, killing at
   least two and injuring ten, in one of the war's largest attacks
   (400 drones, 110 missiles); debris from the barrage also comes
   down in Poland.
3. TRADE - EU/INDONESIA: After ten years of negotiations the EU and
   Indonesia sign a major trade agreement eliminating 98.5% of
   tariffs between Brussels and Southeast Asia's largest economy.
4. CLIMATE - COP31: The climate summit runs into overtime, deadlocked
   over the future of fossil fuels and international finance.
5. ISRAEL - NEW TURN: President Herzog taps former army chief Gadi
   Eisenkot to try to form the next government, bypassing sitting
   PM Netanyahu; Eisenkot invites Likud to coalition talks.
6. ALSO TODAY (strip): France sees a fourth weekend of protests over
   rising living costs; Hong Kong votes for its Election Committee;
   Democrats reclaim the US Congress in the midterms; a 6.7 quake
   shakes Peru's Andes; Brazil's Bolsonaro is admitted to ICU;
   the EU launches a search for a new ECB chief as Lagarde resigns;
   Norway's supreme court voids climate-disputed oil licences.

## Local verification (2026-11-22 ~09:05 WIB)

- `python3 -m py_compile main.py`: OK.
- Two runs into different output dirs: byte-identical entry.png,
  sha256 9c58df282b597c59a393305c7ffb92be65ce3ea5d6db424c1e65cc699e5b4c06.
- PNG valid (signature + IHDR 1024x1024), 22,036 bytes (cap 1,048,576).
- Rendered image inspected visually: masthead date legible, all six
  headlines + subheads legible, scenes read (Gulf tanker + missile
  arcs + burst under a crescent moon, Lviv skyline + missile streaks
  + smoke, EU + Indonesian flags + 98.5%, globe + thermometer +
  OVERTIME, Knesset dome + columns + Israeli flag).
- Fix during the build: the 5x7 bitmap font holds capitals only, so
  the first render dropped every lowercase letter from the subheads
  (only scattered capitals showed). draw_text now folds text to
  upper case before rendering; re-rendered and verified legible.

## Repo

- jekglory/news-image-20261122, PUBLIC, MIT (SPDX line), created
  after the 2026-11-22T00:00:00Z opening.
- Files: main.py, LICENSE, README.md, NOTES.md, .makefun/owner.json.
