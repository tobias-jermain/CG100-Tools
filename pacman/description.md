# 🟡 PAC-MAN

A Pac-Man style arcade game written in MicroPython for the Casio fx-CG100.

| | |
|---|---|
| **File** | [`pacman.py`](pacman.py) |
| **Type** | Game |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |

## Controls

| Key | Action |
|---|---|
| ⬅️ ⬆️ ⬇️ ➡️ | Move Pac-Man |
| **EXE** | Start / pause / continue |
| **AC** | Quit |

## Features

- Full 28×31 maze with dots, power pellets and the side tunnel
- Four ghosts, each with its own targeting behaviour
- Scatter and chase phases, plus frightened mode after a power pellet
- Eaten ghosts return to the ghost house and come back out
- Bonus fruit that changes with the level
- Score, high score and level display, with lives shown on screen
- Extra life at 10,000 points
- Endless levels, getting harder as you go

## Tuning the speed

Near the top of the file is the `SPD` setting:

```python
SPD=8000
```

`SPD` is an extra delay added to every frame. A bigger number gives a slower game and a smaller one gives a faster game. `0` means no extra delay.

The value is set to **8000** in this repo. Adjust it to suit how fast your calculator runs the game.

## How to run

1. Copy `pacman.py` to the calculator.
2. Open it from the Python app.
3. Press **EXE** to start.
