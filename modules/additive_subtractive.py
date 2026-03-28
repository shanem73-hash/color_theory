from __future__ import annotations

import streamlit as st

from modules import color_models_3d
from modules.color_math import cmy_to_rgb, hex_to_rgb, rgb_to_hex


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

    pcol1, pcol2 = st.columns([3, 1])
    with pcol1:
        st.selectbox("Quick preset", presets, key="quick_preset", on_change=apply_preset)
    with pcol2:
        st.markdown(" ")
        if st.button("Reset tab", key="reset_addsub"):
            st.session_state.rgb_r = 120
            st.session_state.rgb_g = 120
            st.session_state.rgb_b = 120
            st.session_state.cmy_c = 40
            st.session_state.cmy_m = 40
            st.session_state.cmy_y = 40
            st.rerun()

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

    st.markdown("### 3D RGB Space (moved from 3D Models tab)")
    perf = st.session_state.get("perf_mode", "Balanced")
    default_density = "Low" if perf == "Fast" else "High" if perf == "Detail" else "Medium"
    rgb_density = st.select_slider(
        "RGB 3D point density",
        options=["Low", "Medium", "High"],
        value=default_density,
        key="rgb3d_density_additive",
    )
    rgb_step = 64 if rgb_density == "Low" else 32 if rgb_density == "High" else 48

    st.plotly_chart(
        color_models_3d.rgb_cube_figure(rgb_step, additive_rgb),
        use_container_width=True,
        config={"scrollZoom": False, "displayModeBar": True},
    )
    st.caption("Current additive RGB selection is marked in the RGB cube.")

    st.markdown("### New Demo: Overlay Two Color Filters")
    st.caption(
        "Simulate stacking transparent filters in front of a light source. "
        "Each filter transmits some portion of R/G/B, so stacking multiplies transmission."
    )

    f1, f2, f3 = st.columns(3)
    with f1:
        light_hex = st.color_picker("Input light color", value="#FFFFFF", key="filter_light")
    with f2:
        filter1_hex = st.color_picker("Filter 1", value="#FF0000", key="filter_1")
    with f3:
        filter2_hex = st.color_picker("Filter 2", value="#00FFFF", key="filter_2")

    light_rgb = hex_to_rgb(light_hex)
    filter1_rgb = hex_to_rgb(filter1_hex)
    filter2_rgb = hex_to_rgb(filter2_hex)

    final_rgb = (
        round((light_rgb[0] / 255) * (filter1_rgb[0] / 255) * (filter2_rgb[0] / 255) * 255),
        round((light_rgb[1] / 255) * (filter1_rgb[1] / 255) * (filter2_rgb[1] / 255) * 255),
        round((light_rgb[2] / 255) * (filter1_rgb[2] / 255) * (filter2_rgb[2] / 255) * 255),
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _swatch("Input light", light_rgb, "Light before filters")
    with c2:
        _swatch("Filter 1", filter1_rgb, "Transmission profile")
    with c3:
        _swatch("Filter 2", filter2_rgb, "Transmission profile")
    with c4:
        _swatch("Final transmitted color", final_rgb, "After stacking Filter 1 + Filter 2")

    st.code(
        "Final = Light × Filter1 × Filter2 (per channel, normalized)\n"
        f"R: {light_rgb[0]} × {filter1_rgb[0]} × {filter2_rgb[0]} / 255² = {final_rgb[0]}\n"
        f"G: {light_rgb[1]} × {filter1_rgb[1]} × {filter2_rgb[1]} / 255² = {final_rgb[1]}\n"
        f"B: {light_rgb[2]} × {filter1_rgb[2]} × {filter2_rgb[2]} / 255² = {final_rgb[2]}"
    )

    st.info(
        "Teaching tip: Ask students to guess the result for Red + Cyan filters on white light. "
        "Then show why overlapping filters usually gets darker, not brighter."
    )
