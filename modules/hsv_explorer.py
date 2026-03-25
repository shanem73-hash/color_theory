from __future__ import annotations

import streamlit as st

from modules.color_math import hsv_deg_to_rgb, rgb_to_hex


def _swatch(title: str, rgb: tuple[int, int, int], note: str) -> None:
    st.markdown(
        f"""
        <div style='border:1px solid #ddd; border-radius:12px; padding:12px; margin-bottom:10px;'>
          <div style='font-size:1.0rem; margin-bottom:8px;'><b>{title}</b></div>
          <div style='height:110px; border-radius:10px; background: rgb({rgb[0]}, {rgb[1]}, {rgb[2]}); border:1px solid #ccc;'></div>
          <div style='margin-top:8px; font-family:monospace;'>RGB: {rgb} | HEX: {rgb_to_hex(rgb)}</div>
          <div style='font-size:0.9rem; color:#555; margin-top:4px;'>{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    st.subheader("HSB / HSV Decomposition Explorer")
    st.caption("Learn what Hue, Saturation, and Brightness each do to a color.")

    c1, c2 = st.columns([1, 1])
    with c1:
        h = st.slider("Hue (0-360°)", 0, 360, 210)
        s = st.slider("Saturation (%)", 0, 100, 60)
        v = st.slider("Brightness / Value (%)", 0, 100, 75)
    with c2:
        lock_mode = st.radio(
            "Exploration mode",
            ["Free", "Lock S,V (change Hue)", "Lock H,V (change Saturation)", "Lock H,S (change Brightness)"],
        )

    base_rgb = hsv_deg_to_rgb(h, s, v)
    _swatch("Current HSV Color", base_rgb, f"H={h}°, S={s}%, V={v}%")

    st.markdown("### Channel isolation preview")
    p1, p2, p3 = st.columns(3)

    with p1:
        hue_only = hsv_deg_to_rgb(h, 100, 100)
        _swatch("Hue only", hue_only, "S=100, V=100 (pure hue)")
    with p2:
        sat_view = hsv_deg_to_rgb(h, s, 100)
        _swatch("Saturation effect", sat_view, "V fixed at 100")
    with p3:
        val_view = hsv_deg_to_rgb(h, 100, v)
        _swatch("Brightness effect", val_view, "S fixed at 100")

    if lock_mode != "Free":
        st.success(
            "Use this mode in class to isolate one variable at a time and build intuition quickly."
        )
