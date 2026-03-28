from __future__ import annotations

import math

import streamlit as st

from modules.color_math import rgb_to_hex


# ----- sRGB / XYZ / Lab helpers -----
def _srgb_to_linear(c: float) -> float:
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    if c <= 0.0031308:
        return 12.92 * c
    return 1.055 * (c ** (1 / 2.4)) - 0.055


def _rgb255_to_linear(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = rgb
    return _srgb_to_linear(r / 255), _srgb_to_linear(g / 255), _srgb_to_linear(b / 255)


def _linear_to_rgb255(rgb: tuple[float, float, float]) -> tuple[int, int, int]:
    r, g, b = rgb
    r8 = max(0, min(255, round(_linear_to_srgb(max(0.0, min(1.0, r))) * 255)))
    g8 = max(0, min(255, round(_linear_to_srgb(max(0.0, min(1.0, g))) * 255)))
    b8 = max(0, min(255, round(_linear_to_srgb(max(0.0, min(1.0, b))) * 255)))
    return r8, g8, b8


def _linear_rgb_to_xyz(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = rgb
    # D65
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    return x, y, z


def _xyz_to_linear_rgb(xyz: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = xyz
    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    b = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z
    return r, g, b


def rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    xr, yr, zr = _linear_rgb_to_xyz(_rgb255_to_linear(rgb))
    # D65 white
    xn, yn, zn = 0.95047, 1.00000, 1.08883

    def f(t: float) -> float:
        d = 6 / 29
        if t > d**3:
            return t ** (1 / 3)
        return t / (3 * d * d) + 4 / 29

    fx, fy, fz = f(xr / xn), f(yr / yn), f(zr / zn)
    l = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return l, a, b


def lab_to_rgb(lab: tuple[float, float, float]) -> tuple[int, int, int]:
    l, a, b = lab
    xn, yn, zn = 0.95047, 1.00000, 1.08883

    fy = (l + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200

    def finv(t: float) -> float:
        d = 6 / 29
        if t > d:
            return t**3
        return 3 * d * d * (t - 4 / 29)

    x = xn * finv(fx)
    y = yn * finv(fy)
    z = zn * finv(fz)
    rgb_lin = _xyz_to_linear_rgb((x, y, z))
    return _linear_to_rgb255(rgb_lin)


# ----- OKLab helpers -----
def rgb_to_oklab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = _rgb255_to_linear(rgb)

    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, a, b


def oklab_to_rgb(oklab: tuple[float, float, float]) -> tuple[int, int, int]:
    L, a, b = oklab

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_**3
    m = m_**3
    s = s_**3

    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b2 = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    return _linear_to_rgb255((r, g, b2))


def _swatch(label: str, rgb: tuple[int, int, int]) -> None:
    st.markdown(
        f"""
        <div style='border:1px solid #ddd; border-radius:12px; padding:10px; margin-bottom:8px;'>
          <div><b>{label}</b></div>
          <div style='height:90px; border:1px solid #ccc; border-radius:10px; background: rgb({rgb[0]}, {rgb[1]}, {rgb[2]}); margin:8px 0;'></div>
          <div style='font-family:monospace;'>RGB {rgb} | {rgb_to_hex(rgb)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    st.subheader("CIELAB + OKLab (Modern Perceptual Models)")
    st.caption("These models are designed so numeric distance better matches human perceived color difference.")

    base = st.color_picker("Pick a base color", value="#4FA3FF")
    base_rgb = tuple(int(base[i : i + 2], 16) for i in (1, 3, 5))

    lab = rgb_to_lab(base_rgb)
    okl = rgb_to_oklab(base_rgb)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### CIELAB tweak")
        dL = st.slider("ΔL*", -30.0, 30.0, 0.0, 1.0)
        dA = st.slider("Δa*", -40.0, 40.0, 0.0, 1.0)
        dB = st.slider("Δb*", -40.0, 40.0, 0.0, 1.0)
        lab2 = (lab[0] + dL, lab[1] + dA, lab[2] + dB)
        lab_rgb = lab_to_rgb(lab2)

    with c2:
        st.markdown("### OKLab tweak")
        dL_ok = st.slider("ΔL (OKLab)", -0.2, 0.2, 0.0, 0.01)
        dA_ok = st.slider("Δa (OKLab)", -0.25, 0.25, 0.0, 0.01)
        dB_ok = st.slider("Δb (OKLab)", -0.25, 0.25, 0.0, 0.01)
        okl2 = (okl[0] + dL_ok, okl[1] + dA_ok, okl[2] + dB_ok)
        okl_rgb = oklab_to_rgb(okl2)

    s1, s2, s3 = st.columns(3)
    with s1:
        _swatch("Base color", base_rgb)
    with s2:
        _swatch("After CIELAB change", lab_rgb)
    with s3:
        _swatch("After OKLab change", okl_rgb)

    de_lab = math.sqrt(dL**2 + dA**2 + dB**2)
    de_ok = math.sqrt((dL_ok * 100) ** 2 + (dA_ok * 100) ** 2 + (dB_ok * 100) ** 2)

    st.markdown("### Distance intuition")
    st.write(f"Approx ΔE*ab (Lab Euclidean): **{de_lab:.2f}**")
    st.write(f"Scaled OKLab distance (for classroom intuition): **{de_ok:.2f}**")

    with st.expander("Why CIELAB / OKLab matter"):
        st.markdown(
            """
- RGB is device-centric and not perceptually uniform.
- CIELAB (1976) was designed so Euclidean distance is closer to perceived difference.
- OKLab is a newer perceptual model that often behaves better for gradients and UI work.
- In practice: use RGB/HEX for implementation, use Lab/OKLab for comparing or adjusting perceived color difference.
"""
        )
