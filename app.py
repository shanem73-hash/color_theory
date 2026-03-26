from __future__ import annotations

import streamlit as st

from modules import additive_subtractive, color_models_3d, converter, hsv_explorer, quiz_mode

st.set_page_config(page_title="Shane's Color Theory Lab", page_icon="🎨", layout="wide")

st.title("🎨 Shane's Color Theory Lab")
st.markdown(
    """
A classroom-friendly Streamlit app for learning color science with interactive demos.

Use the tabs below to explore:
- **Additive vs Subtractive mixing**
- **HSB/HSV decomposition**
- **Color format conversion**
- **3D color models**
- **Quiz mode for assignments**
"""
)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Additive vs Subtractive", "HSB / HSV Explorer", "Converter", "3D Models", "Quiz Mode"]
)

with tab1:
    additive_subtractive.render()

with tab2:
    hsv_explorer.render()

with tab3:
    converter.render()

with tab4:
    color_models_3d.render()

with tab5:
    quiz_mode.render()
