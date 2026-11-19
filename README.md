[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ImRevoltexee/makefun-news-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/ImRevoltexee/makefun-news-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# 19 November 2026 — The World in One Day

Entry for the [make.fun](https://make.fun) bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119):
one image summing up the world's news of Thursday 19 November 2026.

## The image

A newspaper-style infographic (1024×1024, drawn with code, no AI image
generator): a masthead naming the day, six stories, and an "ALSO TODAY"
strip.

- **Summit** — Trump, Xi & Putin meet in Shenzhen: first three-way summit;
  nuclear arms control, Ukraine and Iran.
- **Conflict** — U.S. strikes an Iran missile site; Tehran hits back with
  drones on a Kuwait air base; Bahrain intercepts.
- **Ukraine** — Crimea Bridge hit again; traffic closed as damage is assessed.
- **Gaza** — Israeli tanks cross the Gaza ceasefire line in a rare ground
  operation.
- **Justice** — Myanmar faces a historic genocide verdict at the world court
  over the Rohingya.
- **Culture** — Van Gogh sells for a record $190.4m after a Nazi-era
  ownership dispute.

Also today: Anthropic, maker of Claude, prepares a $1.4 trillion IPO;
GTA VI begins its global rollout; NASA's Voyager 1 passes one light-day
from Earth.

Sources: The New York Times, Reuters, BBC.

## How it works

- `draw.py` — draws `entry.png` from scratch with Pillow (deterministic:
  no network, no randomness, no timestamps). Run it to regenerate the image:
  `python3 draw.py`
- `main.py` — the entry point (Python 3.13, standard library only). It
  copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`)
  and validates the file first (PNG, at most 1 MiB, at most 1024×1024,
  copied bytes hash-checked).

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
