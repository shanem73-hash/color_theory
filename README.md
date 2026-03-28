# Shane's Color Theory Lab

**Shane's Color Theory Lab** is an interactive Streamlit application designed to help students learn core color theory concepts through hands-on visual exploration.

This project is built for classroom teaching, self-study, and live demos. Students can manipulate color channels, observe immediate visual changes, and connect abstract theory to real color behavior used in screens, design tools, and print workflows.

## Project goals

- Teach the difference between **additive** and **subtractive** color mixing
- Build intuition for **Hue, Saturation, and Brightness/Value (HSV/HSB)**
- Practice **color format conversion** across common digital/print representations
- Visualize color spaces with **interactive 3D models**

## Features

### 1) Additive vs Subtractive Mixing
- RGB light mixing demo (additive)
- CMY pigment-style mixing demo (subtractive)
- Quick presets for common classroom examples
- Side-by-side visual comparison with live swatches

### 2) HSB / HSV Explorer
- Interactive H, S, V controls
- Channel decomposition views
- Supports guided instruction on what each channel changes

### 3) Color Converter
Convert between:
- HEX
- RGB
- HSV
- HSL
- CMYK (educational approximation)

Great for helping students understand that one color can be represented in multiple formats.
Includes an **equation explainer** with RGB↔HSV, RGB↔HSL, and RGB↔CMYK reference formulas plus a worked example.

### 4) 3D Color Models
- Interactive **RGB cube** visualization
- Interactive **HSV 3D model** visualization
- Adjustable sampling density for performance/detail tradeoffs
- Improved usability for classroom navigation (wheel-scroll page behavior)

### 5) Quiz Mode (v3)
- Predict-the-result classroom questions
- Multiple-choice flow with immediate feedback
- Assignment lengths (5, 10, 15 questions)
- Live score tracking and completion summary

### 6) Concepts Tab (v4)
- Short color theory history timeline
- Core model intuition notes (RGB/CMYK/HSV/HSL)
- Teaching-oriented explanation blocks

### 7) CIELAB / OKLab Tab (v5)
- Interactive perceptual color model demo
- Apply controlled deltas in Lab and OKLab spaces
- Compare resulting colors side-by-side with the original
- Intro to perceptual distance ideas (ΔE intuition)
- **2D Lab a*b* slice visualization** (fixed lightness)
- **3D CIELAB/OKLab space visualization** with selectable model and density
- Demo card: **RGB move in R/G/B channels** with computed ΔE
- **Iso-ΔE circle (2D)** and **iso-ΔE sphere (3D, transparent orange)** visual overlays
- Side-by-side **RGB 3D vs CIELAB/OKLab 3D** distance comparison

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

- Ask students to **predict** outcomes before moving sliders.
- Use additive/subtractive presets as short formative checks.
- In HSV mode, vary one parameter at a time to isolate effects.
- Explain CMYK as an approximation in this app (real print output depends on device/ICC profiles).

## Roadmap

- Exportable quiz results for classroom grading
- Gamut clipping and device difference demos
- Exportable snapshots/worksheets for Lab/OKLab exercises
- Optional CIEDE2000 comparison activity
- Deeper historical module with references and primary sources

## Repository

GitHub: <https://github.com/shanem73-hash/color_theory>
