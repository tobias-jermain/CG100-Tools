# 🎬 Video Player

Plays short, low-resolution colour clips on the Casio fx-CG100. A PC script turns a GIF or a folder of images into a clip that lives inside the `.py` file.

| | |
|---|---|
| **File** | [`video.py`](video.py) (player) and [`mkvideo.py`](mkvideo.py) (PC converter) |
| **Type** | Tool |
| **Runtime** | MicroPython 1.9.4 with `casioplot` (player), Python 3 with Pillow (converter) |
| **Size** | 111 lines with the demo clip (the calculator limit is 300) |

## Usage

| Key | Action |
|---|---|
| **EXE** | Start, then play / pause |
| ➡️ | Next frame (while paused) |
| ⬅️ | Restart from the first frame |
| ⬆️ / ⬇️ | Faster / slower |
| **AC** | Quit |

It ships with a 60-frame demo (a ball bouncing over grass, 4 colours).

### Making your own clip

On a PC with Python 3 and [Pillow](https://pypi.org/project/pillow/) (`pip install pillow`):

```sh
python3 mkvideo.py clip.gif                 # black and white, 48x24 cells of 8px
python3 mkvideo.py clip.gif -c 8 -s 6 -w 64 # 8 colours, 64 cells of 6px across
python3 mkvideo.py frames/ --step 2         # folder of PNG/JPG frames, every 2nd one
python3 mkvideo.py --demo -c 4              # rebuild the bundled demo
```

It rewrites the data block of `video.py` and refuses to write a file over 300 lines. Then copy `video.py` to the calculator. To convert an MP4, turn it into a GIF or a folder of frames first (for example with `ffmpeg -i in.mp4 -vf fps=10 frames/%04d.png`).

| Option | Meaning |
|---|---|
| `-w` | Cells across (default 48) |
| `-s` | Cell size in pixels (default 8). The picture is at most 384×192 |
| `-c` | Colours in the palette, 2 to 64 (default 2) |
| `--step` | Keep every Nth frame |
| `--max` | Stop after this many frames |
| `--line` | Characters per data line (default 120). Longer lines fit more video in 300 lines |

## Features

- Up to 64 colours from one palette chosen for the whole clip
- Only the cells that change are redrawn each frame, and runs of cells are drawn together
- Pause, single-step, restart and speed control
- Loops the clip, or stops at the end

## Settings

```python
SPD=0;LP=1;ST=400
```

| Setting | What it does |
|---|---|
| `SPD` | Extra delay added every frame at the start. Bigger is slower |
| `LP` | `1` loops the clip, `0` stops on the last frame (EXE plays it again) |
| `ST` | How much ⬆️ / ⬇️ change the delay |

## How it works

- **Frames:** the picture is a grid of cells. Each frame stores only the cells that changed since the last one, as runs of *(cells to skip, run length, colour)*.
- **Encoding:** every number is one character, `ord(c)-35` with the backslash skipped, so the data needs no `int()` or escapes. A value of 63 means "add 63 and read the next character". `!` ends a frame and `}` ends the clip.
- **Drawing:** the screen starts filled with colour 0, which the converter picks as the most used colour, so the first frame is small too.

## Limits

This is a flipbook, not a media player. It cannot decode MP4 or other video formats, so the clip is converted on a PC and embedded in the program, and `set_pixel` is slow.

- **Length:** a few hundred frames at most. The player takes about 85 lines, leaving roughly 215 lines × 120 characters, or about 25 KB of data, and the data also has to fit in the calculator's Python memory. Simple clips with few colours and little movement fit the most frames.
- **Resolution:** blocky by design. Each changed cell costs `S×S` pixel writes, so fewer, bigger cells play faster.
- **Speed:** depends on how much of the picture changes per frame, so busy clips play slowest. It has been tested pixel-for-pixel against the converter on a PC with a mock `casioplot`, but not yet on a real calculator.
- **No sound.**

## How to run

1. Copy `video.py` to the calculator.
2. Open it from the Python app.
3. Press **EXE** to start playing.
