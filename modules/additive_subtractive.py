from __future__ import annotations

import streamlit as st

from modules.color_math import cmy_to_rgb, rgb_to_hex


def _swatch(label: str, rgb: tuple[int, int, int], subtitle: str) -> None:
    st.markdown(
        f"""
        <div style='border:1px solid #ddd; border-radius:12px; padding:12px; margin-bottom:10px;'>
          <div style='font-size:1.0rem; margin-bottom:8px;'><b>{label}</b></div>
          <div style='height:130px; border-radius:10px; background: rgb({rgb[0]}, {rgb[1]}, {rgb[2]}); border:1px solid #ccc;'></div>
          <div style='margin-top:8px; font-family:monospace;'>RGB: {rgb}</div>
          <div style='font-family:monospace;'>HEX: {rgb_to_hex(rgb)}</div>
          <div style='font-size:0.9rem; color:#555; margin-top:4px;'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    st.subheader("Additive vs Subtractive Color Mixing")
    st.caption("Compare light mixing (RGB) and pigment-style mixing (CMY) side by side.")

    presets = [
        "Custom",
        "Additive: Red + Green = Yellow",
        "Additive: Green + Blue = Cyan",
        "Additive: Red + Blue = Magenta",
        "Additive: All channels max = White",
        "Subtractive: Cyan + Yellow = Green",
        "Subtractive: Cyan + Magenta = Blue",
        "Subtractive: Magenta + Yellow = Red",
        "Subtractive: Heavy CMY mix ≈ dark",
    ]

    if "rgb_r" not in st.session_state:
        st.session_state.rgb_r = 120
        st.session_state.rgb_g = 120
        st.session_state.rgb_b = 120
        st.session_state.cmy_c = 40
        st.session_state.cmy_m = 40
        st.session_state.cmy_y = 40

    def apply_preset() -> None:
        p = st.session_state.quick_preset
        if p == "Custom":
            return

        if p == "Additive: Red + Green = Yellow":
            st.session_state.rgb_r, st.session_state.rgb_g, st.session_state.rgb_b = 255, 255, 0
        elif p == "Additive: Green + Blue = Cyan":
            st.session_state.rgb_r, st.session_state.rgb_g, st.session_state.rgb_b = 0, 255, 255
        elif p == "Additive: Red + Blue = Magenta":
            st.session_state.rgb_r, st.session_state.rgb_g, st.session_state.rgb_b = 255, 0, 255
        elif p == "Additive: All channels max = White":
            st.session_state.rgb_r, st.session_state.rgb_g, st.session_state.rgb_b = 255, 255, 255
        elif p == "Subtractive: Cyan + Yellow = Green":
            st.session_state.cmy_c, st.session_state.cmy_m, st.session_state.cmy_y = 100, 0, 100
        elif p == "Subtractive: Cyan + Magenta = Blue":
            st.session_state.cmy_c, st.session_state.cmy_m, st.session_state.cmy_y = 100, 100, 0
        elif p == "Subtractive: Magenta + Yellow = Red":
            st.session_state.cmy_c, st.session_state.cmy_m, st.session_state.cmy_y = 0, 100, 100
        elif p == "Subtractive: Heavy CMY mix ≈ dark":
            st.session_state.cmy_c, st.session_state.cmy_m, st.session_state.cmy_y = 85, 85, 85

    st.selectbox("Quick preset", presets, key="quick_preset", on_change=apply_preset)

    left, right = st.columns(2)

    with left:
        st.markdown("### Additive (Light, RGB)")
        r = st.slider("R", 0, 255, key="rgb_r")
        g = st.slider("G", 0, 255, key="rgb_g")
        b = st.slider("B", 0, 255, key="rgb_b")
        additive_rgb = (r, g, b)
        _swatch("Light Result", additive_rgb, "Starts from black; channels add light.")

    with right:
        st.markdown("### Subtractive (Pigment, CMY)")
        c = st.slider("C (%)", 0, 100, key="cmy_c")
        m = st.slider("M (%)", 0, 100, key="cmy_m")
        y = st.slider("Y (%)", 0, 100, key="cmy_y")
        subtractive_rgb = cmy_to_rgb(c, m, y)
        _swatch("Pigment Result", subtractive_rgb, "Starts from white paper; pigments subtract light.")

    st.info(
        "Teaching tip: Ask students to predict the color before moving sliders. "
        "Then compare prediction vs result."
    )
