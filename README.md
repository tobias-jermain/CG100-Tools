<div align="center">

# 🧮 CG100 Tools

### Games and tools for the **Casio fx-CG100**

![Platform](https://img.shields.io/badge/platform-Casio%20fx--CG100-blue?style=for-the-badge)
![Language](https://img.shields.io/badge/MicroPython-1.9.4-yellow?style=for-the-badge&logo=python&logoColor=white)
![Library](https://img.shields.io/badge/library-casioplot-green?style=for-the-badge)

*Small programs, written to fit and run on the fx-CG100 without modifying the binaries/OS..*

</div>

---

## 📦 Programs

| Program | Type | Description |
|---|---|---|
| [🟡 **PAC-MAN**](pacman/description.md) | 🎮 Game | Pac-Man style arcade game with four ghosts, power pellets, fruit and endless levels |

Each program has its own folder containing the code and a `description.md` that explains what it does and how to use it.

## 🚀 Getting started

1. **Download** the `.py` file from the program's folder.
2. **Copy** it to your calculator.
3. **Open** it in the Python app and run it.

## 🗂️ Repository layout

```text
CG100-Tools/
├── README.md
├── CONTRIBUTING.md
└── pacman/
    ├── pacman.py
    └── description.md
```

New programs follow the same pattern: one folder per program, with the code and a `description.md`.

## ⚙️ Requirements

- Casio **fx-CG100**
- MicroPython **1.9.4** with the `casioplot` module

## 📝 Notes

- Programs are written compactly, with short names and little whitespace, to keep memory use low.
- Games often have a speed setting near the top of the file, such as `SPD` in PAC-MAN. Change it if a game runs too fast or too slow.

## 🤝 Contributing

Want to add a game or tool? Read [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, commit style and how to structure a program.
