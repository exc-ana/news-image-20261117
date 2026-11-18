[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![Rank](https://make.fun/badge/news-image-20261117/exc-ana/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![Reward](https://make.fun/badge/news-image-20261117/exc-ana/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

# Sum up 17 November's world news in one image

make.fun bounty entry (program only — NOT submitted).
Account: @exc-ana (Exc Ana). Bounty: $250, closes Thu 19 Nov 2026, 07:00 WIB.

## How to run

```bash
python3 main.py        # writes output.png in this folder
```

Python 3.12+ standard library only — no Pillow, no network, no fonts
from disk, no installs. (Pillow 10.2.0 is present on this machine but is
deliberately NOT used, to meet the stdlib-only requirement.) The image
is drawn with a built-in 5x7 bitmap font and the PNG is encoded by
hand (zlib, no metadata/timestamps), so the output is byte-identical
on every run.

## Output

- `output.png` — 1024 x 1024 px, 17,498 bytes (< 1 MiB)
- SHA-256: `0f8ffee18ddce133eba0b6a11fc6bd62771a9cc6857b09a4d708f31d05a44c45`
- Determinism: ran `python3 main.py` twice; both runs produced the
  identical SHA-256 above (`cmp` clean).

## The six events (all 17 November 2026)

1. **Middle East — US strikes Qeshm Island, Iran.** US warplanes hit a
   missile site on Qeshm after Iran targeted US personnel and assets,
   a US official told Reuters.
2. **Ukraine — Crimean Bridge hit for a second day.** Russia suspended
   road and rail traffic after a second Ukrainian strike in two days,
   Reuters reported.
3. **Asia-Pacific — Japan scrambles jets over airspace.** Two suspected
   Russian aircraft entered airspace near Okinoshima for about
   3 minutes each, Tokyo said (first confirmed violation since
   September 2024).
4. **Gaza — Winter rains deepen Gaza shelter crisis.** The UN warned
   rains were flooding makeshift shelters as more than 1.7 million
   people remain displaced.
5. **Health — US loses measles elimination status.** PAHO said the
   status ended after the same measles strain circulated for at
   least 12 months (also Mexico and Bolivia, same day).
6. **Markets — Wall Street falls as AI stocks slide.** Major US indexes
   closed lower on Tuesday, led by AI and tech stocks, the AP reported.

Wording stays close to what the sources reported. No forecasts, no
unverified claims presented as fact (e.g. the Crimean Bridge damage is
reported as a traffic suspension, not as a confirmed collapse; the
aircraft are "suspected" Russian, as Tokyo put it).

## Sources checked 19 Nov 2026 (all dated 17 Nov 2026)

- Profile News, "November 17 2026 World News" (Reuters/AP-sourced
  roundup): Qeshm strikes, Crimean Bridge, Gaza rains, measles, markets.
  https://www.profilenews.com/en/november-17-2026-world-news/
- Asas Press, "World News Digest: Top Stories of November 17, 2026":
  Gaza aid, Crimean Bridge, Japan jets.
  https://asaspress.com/en/news/world-news-digest-top-stories-of-november-17-2026
- PAHO, 17 Nov 2026: "PAHO urges countries to step up efforts to stop
  measles outbreaks..." — US, Mexico, Bolivia lost elimination status.
  https://www.paho.org/en/news/17-11-2026-paho-urges-countries-step-efforts-stop-measles-outbreaks-and-move-towards
- USA Today / UNICEF, 17 Nov 2026: PAHO announcement, 5,412 US cases
  in 2026 (CDC, as of 12 Nov).
- Japan airspace: Kyodo/Jiji via multiple outlets, 17 Nov 2026
  (e.g. https://asiadaily.org/news/18969/ and
  https://thelibraryestate.com/japan-protests-after-two-suspected-russian-aircraft-enter-territorial-airspace/)
- Crimean Bridge: Reuters reporting 17 Nov 2026 via
  https://www.insightflow.one/p/the-night-the-bridges-fell-ukraines and
  https://nexuseuropa.eu/en/article/part-of-crimea-bridge-collapses-after-ukrainian-strike-halting-road-and-rail-tra

## Verification done

- `python3 main.py` twice → identical SHA-256 (see above).
- PNG header parsed: 1024 x 1024, 17,498 bytes < 1 MiB.
- Image viewed: title "17 NOVEMBER 2026" prominent, all six cards
  legible, footer lists sources. Readable at ~300 px (title and
  headlines remain legible; body text is small but the headlines
  carry the story).

## Status

Built and verified only. NOT submitted to make.fun, no GitHub repo
created, no wallet linked, no money spent.
