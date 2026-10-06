# ⚡ Circuit Solver

Build a DC circuit on the screen and see every current, voltage and power worked out exactly, as fractions, while you edit.

| | |
|---|---|
| **File** | [`circuitsolver.py`](circuitsolver.py) |
| **Type** | Tool |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |
| **Size** | 296 lines (the calculator limit is 300) |

## Usage

The circuit sits on a 6×4 grid. A part goes on the gap between two neighbouring grid points. Move the cursor onto a gap, add a part, and type its value. The circuit is solved again after every key press.

| Key | Action |
|---|---|
| ⬅️ ⬆️ ⬇️ ➡️ | Move between grid points and gaps (hold to repeat) |
| **OK** | Change the part: empty → wire → resistor → lamp → cell → switch → empty |
| **0–9**, **.** | Type a value (Ω for a resistor or lamp, V for a cell). Typing on an empty gap adds a resistor |
| **+** / **−** | Raise or lower the value by 1 |
| **EXE** | Flip a cell round, or open/close a switch. While typing, EXE finishes the value |
| **DEL** | Delete the last digit you typed, or delete the part |
| **×10^x** | Next example circuit (the last one is a blank board) |
| **AC** | Quit |

The panel on the right shows whatever is under the cursor:

- **Part:** its value, and the voltage across it, current through it and power, as an exact fraction plus a 3-decimal value. If the fraction is long, only the decimal is shown, with `~`.
- **Wire:** the current in it, like an ammeter.
- **Grid point:** its voltage, like a voltmeter. 0 V is the negative terminal of the first cell.

## Features

- Exact answers: nodal analysis with whole-number fractions, so 6 V over 4 Ω + (12 Ω ∥ 6 Ω) gives **3/4 A**, not 0.7500001
- Resistors, lamps, cells, switches and wires, drawn with the usual circuit symbols
- Animated current dots, moving in the direction of conventional current, faster where more current flows
- Lamps glow brighter with more power, and go dark when shorted or switched off
- Handles series, parallel, potential dividers and circuits with more than one cell (a cell being charged shows current flowing into its + terminal)
- Warns about a **SHORT CIRCUIT!** (a loop with cells and wires but no resistance) and says **ADD A CELL** when there is nothing to drive current
- Three example circuits to start from: lamps in parallel, a loaded potential divider and two cells sharing a resistor
- **tobias-jermain / CG100-Tools** badge on the start screen

## Settings

```python
SPD=0;LP=6;HOLD=8
```

| Setting | What it does |
|---|---|
| `SPD` | Extra delay every frame. Bigger makes the current dots move more slowly. |
| `LP` | Lamp power in watts for full brightness. Lamps are dimmer below this. |
| `HOLD` | Frames an arrow key must be held before it repeats. |

## How it works

1. Wires and closed switches join grid points into a single node.
2. Each resistor and lamp adds its conductance to the node equations, and each cell adds an equation that fixes the voltage across it.
3. The equations are solved by Gaussian elimination with fractions. Each step uses the row with the fewest non-zero entries as its pivot, to keep the numbers small.
4. Wire currents come from Kirchhoff's current law, worked out along a spanning tree of the wires.

The solver has been checked on 3,000 random circuits. In each one that could be solved, every part obeyed Ohm's law and every cell its EMF, and Kirchhoff's current law held at every grid point. Every **SHORT CIRCUIT!** warning matched a real loop with cells and wires but no resistance.

## How to run

1. Copy `circuitsolver.py` to the calculator.
2. Open it from the Python app.
3. Press **EXE** to start. The first example circuit loads straight away.

## Notes

- Tested on MicroPython 1.9.4 (Unix port) with a mock `casioplot`. Not yet tested on a real calculator.
- It runs with about 120 KB of heap.
- Usual school circuits solve in well under a millisecond on a PC. A grid full of resistors takes about 20 ms. If the numbers ever get too big for the calculator, the panel shows **TOO COMPLEX** instead of crashing.
- Cells and wires are ideal (no internal resistance). To model internal resistance, put a small resistor in series with the cell.
