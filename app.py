from __future__ import annotations

import streamlit as st

from modules import additive_subtractive, converter, hsv_explorer

st.set_page_config(page_title="Color Theory Lab", page_icon="🎨", layout="wide")

st.title("🎨 Color Theory Lab")
st.markdown(
    """
A classroom-friendly Streamlit app for learning color science with interactive demos.

Use the tabs below to explore:
- **Additive vs Subtractive mixing**
- **HSB/HSV decomposition**
- **Color format conversion**
"""
)


tab1, tab2, tab3 = st.tabs(
    ["Additive vs Subtractive", "HSB / HSV Explorer", "Converter"]
)

with tab1:
    additive_subtractive.render()

with tab2:
    hsv_explorer.render()

with tab3:
    converter.render()
