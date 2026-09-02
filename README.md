# Recomp Mod Setup

A Python automation utility designed to quickly bootstrap a new **Donkey Kong 64 Recompiled** mod project. This script handles configuration generation, boilerplate file copying, template placeholder substitution, and automatic Git submodule setup.

---

## Features

* **Interactive & CLI Support:** Pass configuration arguments directly via the command line or let the script prompt you interactively if values are missing.
* **Automated Manifest Generation:** Generates a fully configured `mod.toml` with your mod's ID, display name, description, authors, and default inputs.
* **Template Scaffolding:** Copies required core files (`Makefile`, linker scripts, licenses) and directories (`src`, `include`, `offline_build`) into your target workspace.
* **Placeholder Replacement:** Automatically updates template files (`README.md`, `build.bat`, `build.sh`) with your custom mod ID and title.
* **Git Submodule Integration:** Automatically pulls down the required `Dk64Syms` and `dk64` decompilation submodules (with an option to bypass via flags).

---

## Command-Line Options

| Flag | Long Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `-d` | `--directory` | Target directory path for your mod | Interactive prompt |
| `-t` | `--title` | Human-readable display name of your mod | Interactive prompt |
| `-i` | `--id` | Unique Mod ID (used for filenames and configs) | Interactive prompt |
| `-dsc` | `--description` | Description of what your mod does | Interactive prompt |
| `-a` | `--authors` | Authors of the mod (delimited by commas) | Interactive prompt |
| `-ng` | `--no_git` | Skip initializing/adding required Git submodules | `False` |

---

## Usage

### 1. Interactive Mode
Run the script without arguments to be guided through the setup process step-by-step:
```bash
python setup.py
```

### 2. Command-Line Mode
This script also supports supplying the arguments directly via CLI
```bash
python setup.py -d "my_dk64_mod" -t "My Custom Mod" -i "custom_mod" -dsc "Adds cool new features to DK64." -a "AuthorOne, AuthorTwo"
```

### 3. Skip Git Submodules
If you want to create the mod structure without pulling the Decomp and Syms submodules, you can pass the `--no_git` flag

```bash
python setup.py --no_git
```