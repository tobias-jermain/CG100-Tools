# 🏰 Golden Realm 3D

A first-person 3D walk through a medieval open world for the Casio fx-CG100. Explore golden wheat fields, villages, forests and the king's castle, and find all the gold.

| | |
|---|---|
| **File** | [`goldenrealm3d.py`](goldenrealm3d.py) |
| **Type** | Game |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |
| **Size** | 271 lines (the calculator limit is 300) |

## Controls

| Key | Action |
|---|---|
| ⬆️ / ⬇️ | Walk forward / back |
| ⬅️ / ➡️ | Turn left / right |
| **EXE** | Start / pause / play again |
| **AC** | Quit |

## Features

- Real raycast 3D view (288×160) with a sky gradient and furrowed golden fields
- 64×64 block open world: mountains around the edge, forests, fences, five villages and a walled castle with towers and a royal keep
- 20 gold coins scattered in the fields, drawn as 3D sprites that hide behind walls
- Live minimap with your position and every coin still to find
- Compass, gold counter and a best score (fewest steps)
- Title and win screens carry the **tobias-jermain / CG100-Tools** badge

## Settings

```python
SPD=0;MV=40;TR=12;IL=1;VD=9;WS=144;NG=20
```

| Setting | What it does |
|---|---|
| `SPD` | Extra delay every frame. Bigger is slower, `0` is no extra delay. |
| `MV` | Walking step (256 = one block). |
| `TR` | Turning step (256 = a full turn). Bigger turns faster in fewer frames. |
| `IL` | `1` redraws every other column while turning (twice as fast, stripy for a moment, then sharp when you let go). `0` gives clean but slower turns. |
| `VD` | View distance in blocks. Lower is faster. |
| `WS` | Wall height in pixels one block away. Lower is faster. |
| `NG` | How many gold coins to find. |

## Speed

The view is only redrawn when you move or turn, and only the pixels that change are painted:

- Each 4-pixel column remembers what it shows (wall top, bottom and colour). When walking, only the few rows where a wall grew or shrank are repainted.
- All maths is integer and table-based (sine, ray step lengths and wall heights are worked out once while loading), so there are no floats or divisions per frame.
- Coin sprites remember the area they covered and that area is restored next frame.

Measured with a mock `casioplot` on MicroPython 1.9.4: about **2,100 pixel writes per step** when walking (Flappy Bird does about 1,200 per frame) and about **13,000 per frame while turning** with `IL=1` (about 23,000 with `IL=0`). Turning is the heavy part, so if it feels slow, lower `VD` or `WS`, or raise `TR`. Not yet measured on a real calculator.

## How to run

1. Copy `goldenrealm3d.py` to the calculator.
2. Open it from the Python app.
3. Wait for **LOADING...** to finish, then press **EXE** to start.
