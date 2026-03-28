from __future__ import annotations

import streamlit as st

from modules import additive_subtractive, concepts, converter, hsv_explorer, perceptual_models, quiz_mode

st.set_page_config(page_title="Shane's Color Theory Lab", page_icon="🎨", layout="wide")

st.title("🎨 Shane's Color Theory Lab")
st.markdown(
    """
A classroom-friendly Streamlit app for learning color science with interactive demos.

Use the tabs below to explore:
- **Additive vs Subtractive mixing**
- **HSB/HSV decomposition**
- **Color format conversion**
- **3D RGB in Additive/Subtractive + 3D HSV in HSV Explorer**
- **Quiz mode for assignments**
- **Concepts (history + model notes)**
- **CIELAB / OKLab perceptual models**
"""
)


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Additive vs Subtractive",
        "HSB / HSV Explorer",
        "Converter",
        "Quiz Mode",
        "Concepts",
        "CIELAB / OKLab",
    ]
)

with tab1:
    additive_subtractive.render()

with tab2:
    hsv_explorer.render()

with tab3:
    converter.render()

with tab4:
    quiz_mode.render()

with tab5:
    concepts.render()

with tab6:
    perceptual_models.render()
