# 🧱 Tetris

The classic falling-block puzzle for the Casio fx-CG100.

| | |
|---|---|
| **File** | [`tetris.py`](tetris.py) |
| **Type** | Game |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |
| **Size** | 176 lines (the calculator limit is 300) |

## Controls

| Key | Action |
|---|---|
| ⬅️ / ➡️ | Move (hold to repeat) |
| ⬆️ | Rotate |
| ⬇️ | Soft drop (+1 point per row) |
| **EXE** | Hard drop (+2 points per row), start and play again |
| **AC** | Quit |

## Features

- 10×20 board with shaded blocks in the seven classic colours
- 7-bag randomiser, so every piece comes once in each set of seven
- Ghost piece shows where the piece will land
- Wall kicks, so pieces rotate next to walls and other blocks
- Next-piece preview
- Classic scoring (40 / 100 / 300 / 1200 × level) with a level up every 10 lines and 15 gravity speeds
- Full rows flash before they clear
- Score, level, lines and best score, plus the **tobias-jermain / CG100-Tools** badge

## Settings

```python
SPD=0;DAS=6;ARR=2;GH=1
```

| Setting | What it does |
|---|---|
| `SPD` | Extra delay every frame. Bigger is slower, `0` is no extra delay. |
| `DAS` | Frames a left/right key must be held before it repeats. |
| `ARR` | Frames between repeats while held. |
| `GH` | `1` shows the ghost piece, `0` hides it (slightly faster). |

Gravity is counted in frames (`GV` table), so if pieces fall too fast on your calculator, raise `SPD`.

## Speed

Only cells that change are redrawn: the falling piece and its ghost are compared with the last frame, and after a line clear only the cells that moved are repainted. That is about **200 pixel writes per frame** on average, measured with a mock `casioplot` on MicroPython 1.9.4. Not yet measured on a real calculator.

## How to run

1. Copy `tetris.py` to the calculator.
2. Open it from the Python app.
3. Press **EXE** to start.
