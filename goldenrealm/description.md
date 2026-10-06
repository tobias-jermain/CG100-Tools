# 🌾 Golden Realm

A cozy Norse farming speedrun for the Casio fx-CG100. Run across a peaceful fjord valley, gather the golden sheaves from the wheat fields, then board the longship and sail for Vinland as fast as you can.

| | |
|---|---|
| **File** | [`goldenrealm.py`](goldenrealm.py) |
| **Type** | Game |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |
| **Size** | 295 lines (the calculator limit is 300) |

## Controls

| Key | Action |
|---|---|
| ⬅️ ⬆️ ⬇️ ➡️ | Walk |
| **EXE** | Dash (also starts and restarts a run) |
| **AC** | Quit |

## The run

1. You start outside the longhouse on the home farm.
2. Gather all **12 golden sheaves** hidden in the wheat fields.
3. Run to the dock on the fjord and board the **longship** to stop the clock.

The map and the sheaves are **the same every run**, so you can learn the valley and plan a route. The timer counts game ticks, so the short pause when you walk onto a new screen doesn't cost you time.

- **Dash:** EXE gives a quick burst of speed, then needs a moment to recharge (the green light in the top bar). Timing your dashes well is the key to fast runs.
- **Splits:** each sheaf shows the time you picked it up.
- **Personal best:** shown in the top bar. At the end you see your time, the difference from your best, and a medal:

| Medal | Time |
|---|---|
| 🥇 Gold | under 1:15 |
| 🥈 Silver | under 1:35 |
| 🥉 Bronze | under 2:00 |

## The valley

- 120×55 tile world (5×5 screens): pine woods in the northern hills, mixed woods, an autumn grove, a river with bridges, flower meadows, farmsteads and a sandy beach on the fjord
- Six kinds of tree and plant: oak, pine, birch, apple, autumn maple and berry bushes
- Turf-roofed longhouses, haystacks, fences, runestones and a longship with a striped sail, shields and a dragon prow
- Sheep wander the fields. They're only there for company, so they never get in your way
- Mini-map of the valley in the top bar
- Title screen carries the **tobias-jermain / CG100-Tools** badge

## Settings

```python
SPD=0;PS=2;NG=12;FPS=30;MG=(75,95,120)
```

| Setting | What it does |
|---|---|
| `SPD` | Extra delay every tick. Bigger is slower, `0` is no extra delay. |
| `PS` | Walking speed in pixels per tick. |
| `NG` | How many sheaves to gather. |
| `FPS` | Ticks per second on the timer. |
| `MG` | Gold, silver and bronze medal times in seconds. |

Changing `PS`, `NG` or `FPS` changes the run, so only compare times made with the same settings.

The best time is saved to `goldenrealm.txt` on the calculator when file saving is available. If it isn't, the best time lasts until you quit.

## Speed and memory

- Walking costs about **400 pixel writes per tick** (Flappy Bird does about 1,200 per frame). Sprites are erased by repainting only the tile pixels under them.
- A new screen redraws only the tiles that differ. Tiles on grass (trees, flowers, fences, hay) only repaint their detail pixels, so a screen change costs about 20,000–45,000 pixel writes instead of 67,000.
- Tiles are stored as short strings of colour indexes, which keeps memory low: the whole game uses about half the memory of the first version.

Measured with a mock `casioplot` on MicroPython 1.9.4. Not yet measured on a real calculator.

## How to run

1. Copy `goldenrealm.py` to the calculator.
2. Open it from the Python app.
3. Wait for **LOADING...** to finish, then press **EXE** to start the run.
