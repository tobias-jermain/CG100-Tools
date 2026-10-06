# 🐤 Flappy Bird

A detailed Flappy Bird clone for the Casio fx-CG100. Tap to flap, squeeze through the pipes and beat your high score.

| | |
|---|---|
| **File** | [`flappybird.py`](flappybird.py) |
| **Type** | Game |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |
| **Size** | 160 lines (the calculator limit is 300) |

## Controls

| Key | Action |
|---|---|
| **EXE** or ⬆️ | Flap (also starts the game and retries) |
| ⬇️ | Pause / resume |
| **AC** | Quit |

Each press is one flap. Holding the key does nothing extra.

## Features

- Coloured sky, clouds, rolling bush hills and a scrolling striped ground
- Animated bird with a flapping wing, drawn with a proper sprite
- Pipes with caps and shading, redrawn only where they changed
- Score and best score in a bar along the top
- Gets harder as you score:
  - the gap between pipes shrinks from 62 to 46 pixels
  - the pipes speed up at 10 and 25 points
- Medals on the game-over screen: bronze (10), silver (20), gold (30), platinum (40)
- "NEW BEST!" when you beat your high score
- The bird falls to the ground when it crashes
- Press **EXE** to retry straight away

## Settings

Two settings sit at the top of the file:

```python
SPD=2000;MS=1
```

| Setting | What it does |
|---|---|
| `SPD` | Extra delay added every frame. Bigger is slower, `0` is no extra delay. |
| `MS` | Moves the pipes and ground every `MS` frames instead of every frame. `2` or `3` is lighter on the calculator but looks steppier. |

Flappy Bird redraws more of the screen each frame than PAC-MAN does. On a PC simulation it wrote about 2,000–3,000 pixels per frame, against about 500 for PAC-MAN. If it feels choppy, try `SPD=0` and then `MS=2`. If it is too fast, raise `SPD`. These values have not been tested on a real calculator, so adjust them to suit yours.

Other values you can change:

| Name | Meaning |
|---|---|
| `G` | Gravity (in 1/16 pixel units) |
| `FL` | Flap strength (negative is up) |
| `SP` | Distance between pipes in pixels |
| `W`, `H` | Canvas size (384×192 for `casioplot`) |

## How it works

- **Smooth drawing:** each frame only the columns that changed are repainted. A moving pipe repaints its two edge columns and the strip it just left.
- **Background restore:** a single `col()` function redraws any column of sky, clouds, hills and pipes, and the bird, panel and text erasing all use it.
- **Fixed-point physics:** position and speed are stored in 1/16 pixels, so no floating point is used per frame.

## How to run

1. Copy `flappybird.py` to the calculator.
2. Open it from the Python app.
3. Press **EXE** or ⬆️ to start flapping.
