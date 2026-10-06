# 🟥 Rubix

A 3D Rubik's cube solver for 2×2 and 3×3 cubes, plus a speedcubing timer, for the Casio fx-CG100.

| | |
|---|---|
| **Files** | [`rubix.py`](rubix.py) (3D solver) and [`rubixtimer.py`](rubixtimer.py) (timer) |
| **Type** | Tool |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |
| **Size** | 296 and 166 lines (the calculator limit is 300) |

The solver and the timer are two separate programs, so each one fits under the 300-line limit.

## 🧊 Rubix (3D solver)

### Home menu

Rubix opens on a home screen: a 3D cube slowly turns on the left while you pick from three cards on the right: **3X3 CUBE**, **2X2 CUBE** and **HOW TO**. Use ⬆️ / ⬇️ to move and **EXE** to open. The picked card turns dark, with a stripe in that face's colour.

### Controls

In the cube view a menu runs along the bottom of the screen: `U R F D L B MIX SOLVE RESET HOME`. `RESET` puts the cube back to solved and `HOME` goes back to the home menu.

| Key | Action |
|---|---|
| ⬅️ / ➡️ | Pick a menu item |
| ⬆️ or **EXE** | Turn the picked face clockwise, or do the picked item |
| ⬇️ | Turn the picked face anticlockwise |
| **EXE** (while a solve plays) | Skip to the end |
| **AC** | Quit |

### Features

- Shaded 3D cube that animates every turn: the layer swings round and you can see the black inside of the cube
- 2×2 and 3×3 cubes, picked from the home menu
- A flat net of all six faces next to the 3D view, so you can see the back, left and bottom too
- Turn any face yourself, or press `MIX` for a random scramble
- `SOLVE` works out a solution for whatever state the cube is in, then plays it back move by move in 3D. It shows the current step, a move counter and the next few moves
- Beginner's layer-by-layer method, so you can follow along on a real cube:
  - **3×3:** cross, first-layer corners, second-layer edges, edge flip, corner twist (Sune, H, Pi, U, T and L cases), corner swap (A-perms), edge swap (U-perms). About 100 moves.
  - **2×2:** first layer, corner twist, corner swap. About 40 moves.
- The solver searches with small integer tables only, so it runs within the calculator's limits (no floats, no `//`)

Standard colours: white top, green front, red right, yellow bottom, orange left, blue back.

### Settings

```python
ST=3;SA=0;SL=(11,20);HI=300
```

| Setting | What it does |
|---|---|
| `ST` | Animation step. `3` (default) draws 2 frames per quarter turn, `2` draws 3 (smoother), `1` draws 6 (smoothest) and `6` jumps straight to the end of each turn. |
| `SA` | `1` animates the scramble too. `0` (default) scrambles instantly. |
| `SL` | Scramble length for the 2×2 and the 3×3. |
| `HI` | Pause between turns of the cube on the home screen. Bigger is calmer. |

### Notes

- Working out a 3×3 solution takes a few seconds on the calculator. `SOLVING: ...` shows which step it's on.
- `set_pixel` is the slow part, so the cube is drawn in a way that sets as few pixels as possible:
  - Each frame is first built in memory as runs of colour along each screen row, with nearer surfaces drawn over farther ones.
  - That frame is compared with the one already on screen, and only the pixels that changed are set. While a layer turns, only it and the part it uncovers get redrawn.
  - The rest of the cube is built once per turn and reused for every frame of that turn.
  - The flat net, the step text and the bottom menu only redraw the parts that changed. The screen is never cleared during a turn.
  - Compared with the first version, each frame of a turn sets about 4× fewer pixels (about 8,000 instead of 31,700). With 2 frames per turn instead of 3, a whole turn sets about 6× fewer. The home screen's turning cube sets about 9× fewer per frame.

## ⏱️ Rubix Timer

### Controls

| Key | Action |
|---|---|
| **EXE** | Start inspection |
| Hold **EXE**, then let go | Start the timer (the time turns red, then green when you can let go) |
| Any key | Stop the timer |
| ⬆️ | Change the last solve: OK → +2 → DNF → OK |
| ⬇️ | Delete the last solve |
| ⬅️ / ➡️ | Switch between 2×2 and 3×3 (each has its own session) |
| **AC** | Quit |

### Features

- Random-move scramble for each solve (11 moves of R/U/F for 2×2, 20 moves for 3×3)
- WCA-style 15-second inspection: going over 15 s gives +2, going over 17 s gives DNF
- Hold-to-start, like a stackmat timer, so you don't start by accident
- Big 7-segment time display that ticks while you solve
- Stats: number of solves, best single, **ao5**, **ao12** (best and worst dropped, as in WCA rules) and mean
- The last 8 times, with +2 and DNF shown
- Times are saved to `rubixtimer.txt` on the calculator when file saving is available

### Settings

```python
INS=15;HD=300;TPS=2000;SV=1
```

| Setting | What it does |
|---|---|
| `INS` | Inspection time in seconds. `0` turns inspection off. |
| `HD` | How long (ms) EXE must be held before the timer can start. |
| `TPS` | Timer ticks per second. Only used if the calculator has no clock (see below). |
| `SV` | `1` saves times to `rubixtimer.txt`, `0` doesn't. |

### Timing

The timer uses the calculator clock (`time.ticks_ms`) when there is one, so times are accurate to the centisecond.

If there's no clock, the top bar shows **(TPS)**. The timer then counts loop ticks instead and shows `-.--` while it runs. To set it up, time a solve of about a minute against a stopwatch, then change `TPS` to `TPS × (timer time ÷ stopwatch time)`. In this mode the inspection countdown is only approximate.

## How to run

1. Copy `rubix.py` and/or `rubixtimer.py` to the calculator.
2. Open one from the Python app.
3. **Rubix:** pick a cube on the home menu, then `MIX` and `SOLVE`. **Timer:** press EXE to inspect, then hold and let go of EXE to start.
