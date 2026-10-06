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
- Title screen carries the **tobias-jermain / CG100-Tools** badge
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
SPD=0;MS=1
```

| Setting | What it does |
|---|---|
| `SPD` | Extra delay added every frame. Bigger is slower, `0` is no extra delay. |
| `MS` | Moves the pipes and ground every `MS` frames instead of every frame. `2` or `3` is lighter on the calculator but looks steppier. |

Flappy Bird redraws more of the screen each frame than PAC-MAN does, so it is tuned to do as little as possible. `SPD=0` is the fastest. If it is too fast, raise `SPD` until it feels right. If it is still too slow, try `MS=2`. These values have not been tested on a real calculator, so adjust them to suit yours.

Other values you can change:

| Name | Meaning |
|---|---|
| `G` | Gravity (in 1/16 pixel units) |
| `FL` | Flap strength (negative is up) |
| `SP` | Distance between pipes in pixels |
| `W`, `H` | Canvas size (384×192 for `casioplot`) |

## Speed

The drawing code is built to touch as few pixels as it can, and to spend as little time as possible between pixels.

- **Pipes** repaint only the pixels that change. Each pipe edge is looked up in a small table, so only the few columns that change are visited, and rows that already have the right colour are skipped.
- **Bird** erases only the pixels it just left, instead of the whole box around it. It falls back to a full restore only when it is next to a pipe cap, the hills or a cloud.
- **Ground** works out each stripe's colour once instead of once per column.
- **Hot loops** keep `set_pixel` in a local variable and avoid helper calls and temporary lists, which MicroPython is slow at.

On MicroPython 1.9.4 on a PC this takes about 2.9 times less time per frame than the first version (292 µs against 863 µs), with 2.1 times fewer bytecodes and 1.35 times fewer pixel writes. Every frame is pixel-for-pixel identical to the first version, so the graphics are unchanged. The speed-up on the calculator has not been measured.

## How it works

- **Smooth drawing:** each frame only the pixels that changed are repainted. A moving pipe repaints its two edge columns and the strip it just left.
- **Background restore:** a single `col()` function redraws any column of sky, clouds, hills and pipes, and the bird, panel and text erasing all use it.
- **Fixed-point physics:** position and speed are stored in 1/16 pixels, so no floating point is used per frame.

## How to run

1. Copy `flappybird.py` to the calculator.
2. Open it from the Python app.
3. Press **EXE** or ⬆️ to start flapping.
