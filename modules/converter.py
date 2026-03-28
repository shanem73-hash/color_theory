from __future__ import annotations

import streamlit as st

from modules.color_math import (
    cmyk_to_rgb,
    converter_state_from_rgb,
    hex_to_rgb,
    hsl_deg_to_rgb,
    hsv_deg_to_rgb,
    rgb_to_hex,
)


def _color_result(rgb: tuple[int, int, int]) -> None:
    st.markdown(
        f"""
        <div style='height:120px; border-radius:12px; border:1px solid #ccc; background: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});'></div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    st.subheader("Color Format Converter")
    st.caption("Edit one format, then click Convert to update all representations.")

    mode = st.radio("Input format", ["HEX", "RGB", "HSV", "HSL", "CMYK"], horizontal=True)

    rgb = (52, 152, 219)

    if mode == "HEX":
        hex_value = st.text_input("HEX", value="#3498DB")
        if st.button("Convert", key="convert_hex"):
            try:
                rgb = hex_to_rgb(hex_value)
            except ValueError as e:
                st.error(str(e))
                return
        else:
            rgb = hex_to_rgb("#3498DB")

    elif mode == "RGB":
        col1, col2, col3 = st.columns(3)
        with col1:
            r = st.number_input("R", min_value=0, max_value=255, value=52)
        with col2:
            g = st.number_input("G", min_value=0, max_value=255, value=152)
        with col3:
            b = st.number_input("B", min_value=0, max_value=255, value=219)
        if st.button("Convert", key="convert_rgb"):
            rgb = (int(r), int(g), int(b))
        else:
            rgb = (52, 152, 219)

    elif mode == "HSV":
        col1, col2, col3 = st.columns(3)
        with col1:
            h = st.number_input("H", min_value=0.0, max_value=360.0, value=204.0)
        with col2:
            s = st.number_input("S (%)", min_value=0.0, max_value=100.0, value=76.0)
        with col3:
            v = st.number_input("V (%)", min_value=0.0, max_value=100.0, value=86.0)
        if st.button("Convert", key="convert_hsv"):
            rgb = hsv_deg_to_rgb(h, s, v)
        else:
            rgb = hsv_deg_to_rgb(204, 76, 86)

    elif mode == "HSL":
        col1, col2, col3 = st.columns(3)
        with col1:
            h = st.number_input("H", min_value=0.0, max_value=360.0, value=204.0, key="hsl_h")
        with col2:
            s = st.number_input("S (%)", min_value=0.0, max_value=100.0, value=69.0, key="hsl_s")
        with col3:
            l = st.number_input("L (%)", min_value=0.0, max_value=100.0, value=53.0, key="hsl_l")
        if st.button("Convert", key="convert_hsl"):
            rgb = hsl_deg_to_rgb(h, s, l)
        else:
            rgb = hsl_deg_to_rgb(204, 69, 53)

    else:  # CMYK
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            c = st.number_input("C (%)", min_value=0.0, max_value=100.0, value=76.0)
        with col2:
            m = st.number_input("M (%)", min_value=0.0, max_value=100.0, value=31.0)
        with col3:
            y = st.number_input("Y (%)", min_value=0.0, max_value=100.0, value=0.0)
        with col4:
            k = st.number_input("K (%)", min_value=0.0, max_value=100.0, value=14.0)
        if st.button("Convert", key="convert_cmyk"):
            rgb = cmyk_to_rgb(c, m, y, k)
        else:
            rgb = cmyk_to_rgb(76, 31, 0, 14)

    data = converter_state_from_rgb(rgb)

    st.markdown("### Converted values")
    _color_result(rgb)

    c1, c2 = st.columns(2)
    with c1:
        st.code(f"HEX: {data['hex']}")
        st.code(f"RGB: {data['rgb']}")
        hsv = data["hsv"]
        st.code(f"HSV: ({hsv[0]:.1f}°, {hsv[1]:.1f}%, {hsv[2]:.1f}%)")
    with c2:
        hsl = data["hsl"]
        cmyk = data["cmyk"]
        st.code(f"HSL: ({hsl[0]:.1f}°, {hsl[1]:.1f}%, {hsl[2]:.1f}%)")
        st.code(f"CMYK: ({cmyk[0]:.1f}%, {cmyk[1]:.1f}%, {cmyk[2]:.1f}%, {cmyk[3]:.1f}%)")

    st.caption(
        "Note: CMYK conversion here is educational and approximate. Real print workflows depend on ICC/device profiles."
    )
    st.caption(f"Current HEX: {rgb_to_hex(rgb)}")

    with st.expander("Explain conversion equations (classroom reference)"):
        st.markdown(
            """
### RGB → HSV (normalized RGB in [0,1])
Let `max = max(r,g,b)`, `min = min(r,g,b)`, `Δ = max-min`.
- **V** = `max`
- **S** = `0 if max=0 else Δ/max`
- **H** depends on which channel is max:
  - if max=r: `60 * ((g-b)/Δ mod 6)`
  - if max=g: `60 * (((b-r)/Δ) + 2)`
  - if max=b: `60 * (((r-g)/Δ) + 4)`

### RGB → HSL
- **L** = `(max + min)/2`
- **S** = `0 if Δ=0 else Δ / (1 - |2L - 1|)`
- Hue uses the same piecewise form as HSV.

### RGB ↔ CMYK (educational approximation)
With normalized RGB:
- `K = 1 - max(r,g,b)`
- `C = (1-r-K)/(1-K)`, `M = (1-g-K)/(1-K)`, `Y = (1-b-K)/(1-K)`
If `K=1`, then `C=M=Y=0`.

Inverse:
- `R = 255*(1-C)*(1-K)`
- `G = 255*(1-M)*(1-K)`
- `B = 255*(1-Y)*(1-K)`
"""
        )

        hsv = data["hsv"]
        hsl = data["hsl"]
        cmyk = data["cmyk"]
        st.markdown("### Worked example (current color)")
        st.code(
            f"RGB {data['rgb']} -> HEX {data['hex']}\n"
            f"HSV ({hsv[0]:.1f}°, {hsv[1]:.1f}%, {hsv[2]:.1f}%)\n"
            f"HSL ({hsl[0]:.1f}°, {hsl[1]:.1f}%, {hsl[2]:.1f}%)\n"
            f"CMYK ({cmyk[0]:.1f}%, {cmyk[1]:.1f}%, {cmyk[2]:.1f}%, {cmyk[3]:.1f}%)"
        )
