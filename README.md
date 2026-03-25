# Color Theory Lab

An interactive Streamlit app for teaching students color theory.

## v1 Features

- **Additive vs Subtractive** color mixing demo (RGB vs CMY)
- **HSB/HSV decomposition explorer**
- **Color converter**: HEX, RGB, HSV, HSL, CMYK
- Classroom-friendly UI with clear visual swatches

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Teaching notes

- Use preset demos in Additive/Subtractive to create quick "predict first" activities.
- In HSV Explorer, lock two channels and vary one to build intuition.
- CMYK conversion in this app is educational/approximate; production print requires ICC profiles.

## Planned v2

- 3D RGB cube and HSV cylinder visualizations
- Target-color challenge/quiz mode
- Gamut clipping and device difference demos
