# Rubik's Cube Scrambler & 3D Visualizer

A desktop application designed for speedcubing.

What it offers:
- random-sequence scramble generator
- an integrated speedcubing timer
- a 3D real-time cube visualization engine (powered by Ursina Engine / Panda3D),
- an algorithm training module (F2L, OLL, PLL).

The graphical interface is built with `customtkinter`, while the 3D rendering pipeline runs in an isolated subprocess utilizing OpenGL.

---

## Prerequisites

- **Python**: `>= 3.10`.
- **Package Manager**: **`uv`** (recommended for deterministic resolution and near-instant environments) or standard `pip` + `venv`.
- **Display Server**: X11 or Wayland with hardware-accelerated OpenGL support.

---

## Installation & Running

### Option 1: Using `uv` (Recommended)

`uv` enforces reproducibility using `uv.lock`, automatically creates the virtual environment, and executes tasks without requiring manual environment activation.

1. **Install `uv`** (if not already installed):
   ```bash
   # Linux / macOS:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Alternatively via pip:
   pip install --user uv
   ```

2. **Synchronize dependencies**:
   ```bash
   # Install core dependencies locked in uv.lock:
   uv sync

   # (Optional) Include development dependencies (ruff, pytest):
   uv sync --extra dev
   ```

3. **Launch the application**:
   ```bash
   uv run python src/main.py
   ```

---

### Option 2: Traditional Virtualenv (`venv` + `pip`)

If running in an environment without `uv`:

1. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**:
   ```bash
   python src/main.py
   ```

---

## Quick guide

### Controls

#### Main Window (Timer & Scrambler):
- **`Space`**: Start / Stop / Resume timer
- **`r`**: Reset timer to `00:00:000`
- **`g`**: Generate a new scramble sequence
- **`Esc`**: Exit the application
#### 3D Cube View (Ursina Engine):
- - **Manual Face Turns**:
  - `L` – Left face
  - `R` – Right face
  - `U` – Up face
  - `D` – Down face
  - `F` – Front face
  - `B` – Back face

### UI buttons

#### Main Window:
- **"View 3D scramble animation" Button**: Spawns the 3D cube model window
- **"Learn algorithms" Button**: Opens the algorithm practice and learning view


#### 3D Cube View (Ursina Engine):
- **Camera Orbit / Pan**: Right Mouse Button / Scroll Wheel
- **Speed Slider**: Adjusts animation duration
- **Scramble / Stop / Resume / Reset Buttons**: Playback controls for move sequences

---

## Project Structure

```text
├── assets/                     # Graphic assets (textures, face colors, application icon)
├── src/
│   ├── main.py                 # Application entrypoint
│   └── app/
│       ├── constants/          # Configuration constants (window dimensions, move chances)
│       ├── logic/              # Business logic: timer, move generator, scraper, database
│       ├── main_menu/          # CustomTkinter UI frames (main window, algorithm view)
│       └── model/              # Ursina/Panda3D entities and scenes (cube, faces, pieces)
├── pyproject.toml              # Project metadata and PEP 621 dependencies specification
├── uv.lock                     # Deterministic multi-platform dependency lockfile
└── requirements.txt            # Fallback dependency manifest for traditional pip
```
