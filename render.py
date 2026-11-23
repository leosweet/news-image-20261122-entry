#!/usr/bin/env python3
"""render.py — layout spec + verification for the 22 Nov 2026 front page.

The front-page image itself (entry.png) is the competition artifact: a
1024x1024 editorial front page summing up Sunday 22 November 2026.
This script documents the eight stories it covers, computes the page
geometry, writes layout.json, and verifies entry.png meets the gate
(1024x1024, at most 1 MiB).
"""

import json
import os
import sys

PAGE = 1024            # square front page, pixels
MASTHEAD_H = 80        # top masthead band
HERO_H = 420           # hero story block
GRID_ROWS = 2          # two rows of story cells under the hero
GRID_COLS = 4          # four cells per row (7 stories use grid-1..grid-7;
                       # grid-8 is spare space in the layout)
FOOTER_H = 104         # bottom footer band
GAP = 12               # gutter between blocks

STORIES = [
    {
        "id": "cop31",
        "slot": "hero",
        "headline": "COP31 DEADLOCK",
        "caption": "Fossil-fuel row stalls the climate deal in Antalya, Turkey.",
    },
    {
        "id": "baltic-ship",
        "slot": "grid-1",
        "headline": "SHIP ABLAZE IN BALTIC",
        "caption": "Ukrainian drone hits a Russian cargo ship; crew evacuates.",
    },
    {
        "id": "cartel-boss",
        "slot": "grid-2",
        "headline": "CARTEL BOSS CAPTURED",
        "caption": "\u201cEl Chapo Isidro\u201d seized in Sinaloa; 11 dead in firefight.",
    },
    {
        "id": "brazil-storm",
        "slot": "grid-3",
        "headline": "STORM RAVAGES BRAZIL",
        "caption": "Deadly storm, 4 killed, 162 injured.",
    },
    {
        "id": "france-protests",
        "slot": "grid-4",
        "headline": "FRANCE PROTESTS AGAIN",
        "caption": "Sixth weekend over living costs.",
    },
    {
        "id": "nvidia-chips",
        "slot": "grid-5",
        "headline": "US QUERIES NVIDIA CHIP SALES",
        "caption": "~900,000 AI chips signed off for China.",
    },
    {
        "id": "eu-indonesia",
        "slot": "grid-6",
        "headline": "EU\u2013INDONESIA TRADE DEAL",
        "caption": "Ambitious pact signed.",
    },
    {
        "id": "liverpool",
        "slot": "grid-7",
        "headline": "LIVERPOOL 4\u20130 MAN UTD",
        "caption": "Anfield rout on Pochettino's debut.",
    },
]


def layout_boxes():
    """Return the pixel box for every slot on the 1024x1024 page."""
    boxes = {}
    y = 0
    boxes["masthead"] = {"x": 0, "y": y, "w": PAGE, "h": MASTHEAD_H}
    y += MASTHEAD_H + GAP
    boxes["hero"] = {"x": 0, "y": y, "w": PAGE, "h": HERO_H}
    y += HERO_H + GAP
    cell_w = (PAGE - (GRID_COLS - 1) * GAP) // GRID_COLS
    grid_h = PAGE - y - FOOTER_H - GAP
    cell_h = (grid_h - (GRID_ROWS - 1) * GAP) // GRID_ROWS
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            n = r * GRID_COLS + c + 1
            boxes[f"grid-{n}"] = {
                "x": c * (cell_w + GAP),
                "y": y + r * (cell_h + GAP),
                "w": cell_w,
                "h": cell_h,
            }
    boxes["footer"] = {"x": 0, "y": PAGE - FOOTER_H, "w": PAGE, "h": FOOTER_H}
    return boxes


def verify_entry(path="entry.png"):
    """Check the artifact: exists, at most 1 MiB, 1024x1024."""
    if not os.path.exists(path):
        raise SystemExit(f"missing: {path}")
    size = os.path.getsize(path)
    if size > 1024 * 1024:
        raise SystemExit(f"{path}: {size} bytes, over the 1 MiB limit")
    with open(path, "rb") as fh:
        head = fh.read(2)
        fh.seek(-2, os.SEEK_END)
        tail = fh.read(2)
    if head != b"\xff\xd8" or tail != b"\xff\xd9":
        raise SystemExit(f"{path}: not a complete JPEG")
    # Read dimensions from the SOF0 marker without Pillow.
    with open(path, "rb") as fh:
        data = fh.read()
    i = 2
    width = height = None
    while i < len(data) - 1:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height = (data[i + 5] << 8) | data[i + 6]
            width = (data[i + 7] << 8) | data[i + 8]
            break
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = (data[i + 2] << 8) | data[i + 3]
        i += 2 + seg_len
    if (width, height) != (PAGE, PAGE):
        raise SystemExit(f"{path}: {width}x{height}, expected 1024x1024")
    return size, width, height


def main():
    boxes = layout_boxes()
    spec = {
        "page": PAGE,
        "date": "2026-11-22",
        "masthead": "THE WORLD IN ONE PICTURE",
        "stories": [
            {**s, "box": boxes[s["slot"]]} for s in STORIES
        ],
        "footer": boxes["footer"],
    }
    with open("layout.json", "w", encoding="utf-8") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=2)
    print(f"layout.json: {len(STORIES)} story boxes written")
    size, w, h = verify_entry("entry.png")
    print(f"entry.png: {size} bytes, {w}x{h} \u2014 OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
