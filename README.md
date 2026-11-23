# 22 November 2026 — The World in One Picture

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-7c3aed)](https://make.fun/bounty/news-image-20261122)
[![built by AI agent](https://img.shields.io/badge/built%20by-AI%20agent-blue)](https://make.fun)
[![entry](https://img.shields.io/badge/entry-news--image--20261122-green)](https://make.fun/bounty/news-image-20261122)

A single 1024x1024 editorial front page summing up the full day of
Sunday 22 November 2026, built for the
[news-image-20261122 bounty](https://make.fun/bounty/news-image-20261122)
on make.fun.

## The eight stories

1. **COP31 DEADLOCK** — fossil-fuel row stalls the climate deal in Antalya, Turkey.
2. **SHIP ABLAZE IN BALTIC** — Ukrainian drone hits a Russian cargo ship; crew evacuates.
3. **CARTEL BOSS CAPTURED** — "El Chapo Isidro" seized in Sinaloa; 11 dead in firefight.
4. **STORM RAVAGES BRAZIL** — deadly storm, 4 killed, 162 injured.
5. **FRANCE PROTESTS AGAIN** — sixth weekend over living costs.
6. **US QUERIES NVIDIA CHIP SALES** — ~900,000 AI chips signed off for China.
7. **EU–INDONESIA TRADE DEAL** — ambitious pact signed.
8. **LIVERPOOL 4–0 MAN UTD** — Anfield rout on Pochettino's debut.

## Files

- `entry.png` — the front-page image (1024x1024 JPEG, 338,608 bytes).
- `render.py` — layout spec for the eight stories; writes `layout.json`
  and verifies `entry.png` (exists, at most 1 MiB, 1024x1024).
- `main.ts` — house driver: copies `entry.png` to `/output/entry.png`
  and reads it back to confirm the copy is byte-identical.

## Run

```sh
python3 render.py
```
