# Contributing to CG100 Tools

Thanks for helping out! These are the rules for adding to or changing this repo. Keep things small and simple.

## 🌿 Branches

`main` is the stable branch. Never commit to it directly. Make a branch, then open a pull request.

### Naming

Use `type/short-description`, in lowercase, with hyphens between words and no spaces.

| Type | Use for | Example |
|---|---|---|
| `feature/` | A new game or tool, or a new feature in one | `feature/tetris` |
| `fix/` | A bug fix | `fix/pacman-ghost-collision` |
| `docs/` | README, `description.md` or `CONTRIBUTING.md` changes | `docs/update-readme` |
| `chore/` | Tidying, renaming, repo upkeep | `chore/rename-folders` |

Keep names short (about 2–4 words) and say what the change does.

## 💬 Commit messages

- Write them in the imperative present tense ("Add snake game", not "Added" or "Adds").
- Keep the first line to about 50 characters, with no full stop.
- Add a body only when the *why* isn't obvious.

Examples:

```text
Add snake game
Fix ghost respawn bug in pacman
Update README programs table
```

## 📁 Adding a program

Each program gets its own folder, named in lowercase with no spaces:

```text
program-name/
├── program-name.py
└── description.md
```

Then add a row for it to the programs table in `README.md`.

### `description.md` should include

1. A title and a one-line summary
2. File, type (Game or Tool) and runtime
3. Controls (for games) or usage (for tools)
4. Features
5. Any settings the user can change (like `SPD` in PAC-MAN)
6. How to run it

Use [`pacman/description.md`](pacman/description.md) as a template.

## 🧮 Code rules

- Target **MicroPython 1.9.4** with `casioplot` on the **Casio fx-CG100**. Avoid newer Python features.
- Put a comment on the first line saying what the program is and how to control it.
- Memory is tight, so short names and compact code are fine. Comment anything that isn't obvious.
- Put adjustable settings (speed, colours and so on) as constants near the top of the file.
- Please test on a calculator or an emulator before opening a PR. Say in the PR which one you used.

## 🔀 Pull requests

- **Keep them light.** One program or one fix per PR.
- Use a short, clear title in the same style as a commit message.
- In the description, say what changed and how you tested it.
- Make sure the README and `description.md` match your change.
- Squash and merge into `main`, then delete the branch.
