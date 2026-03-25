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

    preset = st.selectbox(
        "Quick preset",
        [
            "Custom",
            "Additive: Red + Green = Yellow",
            "Additive: Green + Blue = Cyan",
            "Additive: Red + Blue = Magenta",
            "Additive: All channels max = White",
            "Subtractive: Cyan + Yellow = Green",
            "Subtractive: Cyan + Magenta = Blue",
            "Subtractive: Magenta + Yellow = Red",
            "Subtractive: Heavy CMY mix ≈ dark",
        ],
    )

    rgb_defaults = (120, 120, 120)
    cmy_defaults = (40, 40, 40)

    if preset == "Additive: Red + Green = Yellow":
        rgb_defaults = (255, 255, 0)
    elif preset == "Additive: Green + Blue = Cyan":
        rgb_defaults = (0, 255, 255)
    elif preset == "Additive: Red + Blue = Magenta":
        rgb_defaults = (255, 0, 255)
    elif preset == "Additive: All channels max = White":
        rgb_defaults = (255, 255, 255)
    elif preset == "Subtractive: Cyan + Yellow = Green":
        cmy_defaults = (100, 0, 100)
    elif preset == "Subtractive: Cyan + Magenta = Blue":
        cmy_defaults = (100, 100, 0)
    elif preset == "Subtractive: Magenta + Yellow = Red":
        cmy_defaults = (0, 100, 100)
    elif preset == "Subtractive: Heavy CMY mix ≈ dark":
        cmy_defaults = (85, 85, 85)

    left, right = st.columns(2)

    with left:
        st.markdown("### Additive (Light, RGB)")
        r = st.slider("R", 0, 255, rgb_defaults[0], key="rgb_r")
        g = st.slider("G", 0, 255, rgb_defaults[1], key="rgb_g")
        b = st.slider("B", 0, 255, rgb_defaults[2], key="rgb_b")
        additive_rgb = (r, g, b)
        _swatch("Light Result", additive_rgb, "Starts from black; channels add light.")

    with right:
        st.markdown("### Subtractive (Pigment, CMY)")
        c = st.slider("C (%)", 0, 100, int(cmy_defaults[0]), key="cmy_c")
        m = st.slider("M (%)", 0, 100, int(cmy_defaults[1]), key="cmy_m")
        y = st.slider("Y (%)", 0, 100, int(cmy_defaults[2]), key="cmy_y")
        subtractive_rgb = cmy_to_rgb(c, m, y)
        _swatch("Pigment Result", subtractive_rgb, "Starts from white paper; pigments subtract light.")

    st.info(
        "Teaching tip: Ask students to predict the color before moving sliders. "
        "Then compare prediction vs result."
    )
