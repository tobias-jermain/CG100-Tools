# 🧩 Template

A starting point for a new CG100 program. Copy this folder, rename it and fill in the blanks.

| | |
|---|---|
| **File** | [`template.py`](template.py) |
| **Type** | Game / Tool *(delete one)* |
| **Runtime** | MicroPython 1.9.4 with `casioplot` |

## How to use this template

1. Copy the `template/` folder and rename it in lowercase, e.g. `snake/`.
2. Rename `template.py` to match, e.g. `snake.py`.
3. Replace this file's content with your own (keep the headings below).
4. Add a row for your program to the table in the [README](../README.md).
5. Follow the branch and commit rules in [CONTRIBUTING.md](../CONTRIBUTING.md).

The demo code moves a blue square around with the arrow keys. It shows the basics: input, drawing, pausing and a speed setting.

## Controls

*(Games: list the keys. Tools: describe how to use it.)*

| Key | Action |
|---|---|
| ⬅️ ⬆️ ⬇️ ➡️ | Move |
| **EXE** | Start / pause |
| **AC** | Quit |

## Features

- *Feature one*
- *Feature two*

## Settings

*(Anything the user can change near the top of the file.)*

```python
SPD=2000
```

`SPD` is an extra delay added every frame. Bigger is slower, `0` is no extra delay.

## How to run

1. Copy the `.py` file to the calculator.
2. Open it from the Python app.
3. Press **EXE** to start.

## Notes

- Programs can be at most **300 lines** on the fx-CG100.
- The `casioplot` canvas is 384×192 pixels.
- `set_pixel` is the slow part, so redraw only what changed each frame.
