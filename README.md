# Shane's Color Theory Lab

**Shane's Color Theory Lab** is an interactive Streamlit application designed to help students learn core color theory concepts through hands-on visual exploration.

This project is built for classroom teaching, self-study, and live demos. Students can manipulate color channels, observe immediate visual changes, and connect abstract theory to real color behavior used in screens, design tools, and print workflows.

## Project goals

- Teach the difference between **additive** and **subtractive** color mixing
- Build intuition for **Hue, Saturation, and Brightness/Value (HSV/HSB)**
- Practice **color format conversion** across common digital/print representations
- Visualize color spaces with **interactive 3D models**

## Features (teaching order)

### 1) Concepts
- Visual **history timeline** diagram
- **Concept map** diagram showing relationships across RGB/CMYK/HSV/HEX/CIELAB/OKLab
- Foundation notes before hands-on sections

### 2) Additive vs Subtractive Mixing
- RGB light mixing demo (additive)
- CMY pigment-style mixing demo (subtractive)
- Quick presets for common classroom examples
- Side-by-side visual comparison with live swatches
- Embedded RGB 3D cube

### 3) HSB / HSV Explorer
- Interactive H, S, V controls
- Channel decomposition views
- Embedded HSV 3D model

### 4) CIELAB / OKLab
- Interactive perceptual color model demo
- Apply controlled deltas in Lab and OKLab spaces
- **2D Lab a*b* slice + iso-ΔE circle**
- **3D side-by-side RGB vs CIELAB/OKLab** with distance lines and transparent orange iso-spheres
- Demo card: RGB move in all channels with RGB distance + perceptual distance

### 5) Color Converter
Convert between:
- HEX, RGB, HSV, HSL, CMYK
- **CIELAB and OKLab output values**

Includes equation explainers for RGB↔HSV, RGB↔HSL, RGB↔CMYK, and RGB→CIELAB/OKLab pipeline notes.

### 6) Quiz Mode
- Mixed classroom questions including CIELAB/OKLab concepts
- Multiple-choice flow with immediate feedback
- Assignment lengths (5, 10, 15 questions)
- Live score tracking and completion summary

## Tech stack

- **Python**
- **Streamlit**
- **NumPy**
- **Plotly**

## Run locally

```bash
cd ~/.openclaw/workspace-coder/color_theory
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Teaching notes

- Recommended flow: **Concepts → Add/Sub → HSV → CIELAB/OKLab → Converter → Quiz**.
- Ask students to **predict** outcomes before moving sliders.
- Use additive/subtractive presets as quick formative checks.
- In HSV mode, vary one parameter at a time to isolate effects.
- Explain CMYK as an approximation (real print output depends on ICC/device profiles).
- In CIELAB/OKLab, compare RGB distance vs perceptual distance to discuss why RGB is not uniform.

## Roadmap

- Exportable quiz results for classroom grading
- Gamut clipping and device difference demos
- Exportable snapshots/worksheets for Lab/OKLab exercises
- Optional CIEDE2000 comparison activity
- Deeper historical module with references and primary sources

## Repository

GitHub: <https://github.com/shanem73-hash/color_theory>
