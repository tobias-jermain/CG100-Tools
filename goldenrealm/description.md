# 🌾 Golden Realm

A top-down medieval open-world adventure for the Casio fx-CG100. Explore a kingdom of 25 screens, gather gold from the golden wheat fields, dodge the wolves and bring the gold back to the king.

| | |
|---|---|
| **File** | [`goldenrealm.py`](goldenrealm.py) |
| **Type** | Game |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |
| **Size** | 294 lines (the calculator limit is 300) |

## Controls

| Key | Action |
|---|---|
| ⬅️ ⬆️ ⬇️ ➡️ | Walk |
| **EXE** | Start / pause / play again |
| **AC** | Quit |

## Features

- 120×55 tile world (5×5 screens) built when the game loads: river with bridges, lakes, roads, forests, flower meadows, villages, rocky borders and the king's castle
- Golden wheat fields with 24 gold nuggets hidden in them
- Pixel-art knight with a walking animation, and wolves that wander and chase you when you get close
- Three hearts. A wolf bite costs one, knocks you back and gives a moment of safety
- Talk to the king in the castle: he tells you how much gold is left, and you win when you bring it all
- Status bar with gold, hearts, messages and a 5×5 map of where you are
- Title screen carries the **tobias-jermain / CG100-Tools** badge

## Settings

```python
SPD=0;PS=2;NG=24;LV=3
```

| Setting | What it does |
|---|---|
| `SPD` | Extra delay every frame. Bigger is slower, `0` is no extra delay. |
| `PS` | Walking speed in pixels per frame. |
| `NG` | How much gold to find. |
| `LV` | Number of hearts. |

## Speed

- Walking around a screen costs about **340 pixel writes per frame** (sprites are erased by repainting only the tile pixels under them).
- Moving to a new screen redraws only the tiles that differ. Tiles that share a base colour (grass, trees, flowers, fences) only repaint their detail pixels. A screen change costs about 30,000–45,000 pixel writes, less than a full redraw (67,000).

Measured with a mock `casioplot` on MicroPython 1.9.4. Not yet measured on a real calculator.

## How to run

1. Copy `goldenrealm.py` to the calculator.
2. Open it from the Python app.
3. Wait for **LOADING...** to finish, then press **EXE** to start.
