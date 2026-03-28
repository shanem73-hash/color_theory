from __future__ import annotations

import streamlit as st

from modules import additive_subtractive, concepts, converter, hsv_explorer, perceptual_models, quiz_mode

st.set_page_config(page_title="Shane's Color Theory Lab", page_icon="🎨", layout="wide")

if "app_mode" not in st.session_state:
    st.session_state.app_mode = "Student"
if "perf_mode" not in st.session_state:
    st.session_state.perf_mode = "Balanced"

with st.sidebar:
    st.markdown("### Classroom Controls")
    st.session_state.app_mode = st.radio("Mode", ["Student", "Teacher"], index=0 if st.session_state.app_mode == "Student" else 1)
    st.session_state.perf_mode = st.select_slider("Performance", options=["Fast", "Balanced", "Detail"], value=st.session_state.perf_mode)

st.title("🎨 Shane's Color Theory Lab")
st.markdown(
    """
A classroom-friendly Streamlit app for learning color science with interactive demos.

Use the tabs below in teaching order:
1. **Concepts (history + model map)**
2. **Additive vs Subtractive**
3. **HSB / HSV Explorer**
4. **CIELAB / OKLab**
5. **Converter**
6. **Quiz Mode**
"""
)


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Concepts",
        "Additive vs Subtractive",
        "HSB / HSV Explorer",
        "CIELAB / OKLab",
        "Converter",
        "Quiz Mode",
    ]
)

with tab1:
    concepts.render()

with tab2:
    additive_subtractive.render()

with tab3:
    hsv_explorer.render()

with tab4:
    perceptual_models.render()

with tab5:
    converter.render()

with tab6:
    quiz_mode.render()
