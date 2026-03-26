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

### 4) 3D Color Models
- Interactive **RGB cube** visualization
- Interactive **HSV 3D model** visualization
- Adjustable sampling density for performance/detail tradeoffs
- Improved usability for classroom navigation (wheel-scroll page behavior)

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

- Quiz mode (predict-and-reveal with scoring)
- Gamut clipping and device difference demos
- Optional CIELAB/perceptual distance activities

## Repository

GitHub: <https://github.com/shanem73-hash/color_theory>
