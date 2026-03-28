from __future__ import annotations

import math

import plotly.graph_objects as go
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


def _lab_plane_figure(
    l_fixed: float,
    base_lab: tuple[float, float, float],
    moved_lab: tuple[float, float, float] | None = None,
    delta_e: float | None = None,
) -> go.Figure:
    a_vals = list(range(-80, 81, 8))
    b_vals = list(range(-80, 81, 8))
    x, y, cols = [], [], []

    for a in a_vals:
        for b in b_vals:
            rgb = lab_to_rgb((l_fixed, float(a), float(b)))
            x.append(a)
            y.append(b)
            cols.append(f"rgb({rgb[0]},{rgb[1]},{rgb[2]})")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(size=10, color=cols),
            hovertemplate="a*: %{x}<br>b*: %{y}<extra></extra>",
            name="Lab a*b* slice",
        )
    )

    base_a, base_b = base_lab[1], base_lab[2]
    fig.add_trace(
        go.Scatter(
            x=[base_a],
            y=[base_b],
            mode="markers+text",
            marker=dict(size=12, color="black", symbol="diamond"),
            text=["Base"],
            textposition="top center",
            name="Base color",
        )
    )

    if moved_lab is not None:
        fig.add_trace(
            go.Scatter(
                x=[moved_lab[1]],
                y=[moved_lab[2]],
                mode="markers+text",
                marker=dict(size=11, color="white", line=dict(color="black", width=2)),
                text=["RGB move"],
                textposition="bottom center",
                name="RGB move",
            )
        )

    if delta_e is not None and delta_e > 0:
        theta = [i * (2 * math.pi / 180) for i in range(181)]
        cx = [base_a + delta_e * math.cos(t) for t in theta]
        cy = [base_b + delta_e * math.sin(t) for t in theta]
        fig.add_trace(
            go.Scatter(
                x=cx,
                y=cy,
                mode="lines",
                line=dict(color="black", width=2, dash="dash"),
                name=f"Iso-ΔE circle (r={delta_e:.1f})",
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        title=f"CIELAB a*b* plane at L*={l_fixed:.1f}",
        xaxis_title="a* (green ↔ red)",
        yaxis_title="b* (blue ↔ yellow)",
        yaxis_scaleanchor="x",
        height=620,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def _rgb_space_3d_figure(
    base_rgb: tuple[int, int, int],
    moved_rgb: tuple[int, int, int] | None,
    step: int,
) -> go.Figure:
    vals = list(range(0, 256, step))
    xs, ys, zs, cols = [], [], [], []

    for r in vals:
        for g in vals:
            for b in vals:
                xs.append(r)
                ys.append(g)
                zs.append(b)
                cols.append(f"rgb({r},{g},{b})")

    base_r, base_g, base_b = base_rgb
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="markers",
            marker=dict(size=3, color=cols, opacity=0.7),
            name="RGB samples",
            hovertemplate="R:%{x}<br>G:%{y}<br>B:%{z}<extra></extra>",
        )
    )

    radius = None
    if moved_rgb is not None:
        mr, mg, mb = moved_rgb
        radius = math.sqrt((mr - base_r) ** 2 + (mg - base_g) ** 2 + (mb - base_b) ** 2)

        # Distance line (RGB Euclidean)
        fig.add_trace(
            go.Scatter3d(
                x=[base_r, mr],
                y=[base_g, mg],
                z=[base_b, mb],
                mode="lines",
                line=dict(color="black", width=6),
                name=f"RGB distance ({radius:.1f})",
                hoverinfo="skip",
            )
        )

        # Iso-distance sphere in RGB space
        if radius > 0:
            u_steps, v_steps = 28, 14
            u_vals = [i * (2 * math.pi / (u_steps - 1)) for i in range(u_steps)]
            v_vals = [i * (math.pi / (v_steps - 1)) for i in range(v_steps)]
            sx, sy, sz = [], [], []
            for v in v_vals:
                rowx, rowy, rowz = [], [], []
                for u in u_vals:
                    rowx.append(base_r + radius * math.cos(u) * math.sin(v))
                    rowy.append(base_g + radius * math.sin(u) * math.sin(v))
                    rowz.append(base_b + radius * math.cos(v))
                sx.append(rowx)
                sy.append(rowy)
                sz.append(rowz)
            fig.add_trace(
                go.Surface(
                    x=sx,
                    y=sy,
                    z=sz,
                    opacity=0.22,
                    showscale=False,
                    colorscale=[[0, "#ff8c00"], [1, "#ff8c00"]],
                    name=f"RGB iso-distance sphere ({radius:.1f})",
                    hoverinfo="skip",
                )
            )

    fig.add_trace(
        go.Scatter3d(
            x=[base_r],
            y=[base_g],
            z=[base_b],
            mode="markers+text",
            marker=dict(size=8, color="black", symbol="diamond"),
            text=["Base"],
            textposition="top center",
            name="Base color",
        )
    )

    if moved_rgb is not None:
        mr, mg, mb = moved_rgb
        fig.add_trace(
            go.Scatter3d(
                x=[mr],
                y=[mg],
                z=[mb],
                mode="markers+text",
                marker=dict(size=7, color="white", line=dict(color="black", width=2)),
                text=["RGB move"],
                textposition="bottom center",
                name="RGB move",
            )
        )

    fig.update_layout(
        scene=dict(
            xaxis_title="R",
            yaxis_title="G",
            zaxis_title="B",
            xaxis=dict(range=[0, 255]),
            yaxis=dict(range=[0, 255]),
            zaxis=dict(range=[0, 255]),
            aspectmode="cube",
        ),
        title="RGB 3D view",
        height=760,
        margin=dict(l=0, r=0, t=40, b=10),
    )
    return fig


def _perceptual_space_3d_figure(
    base_rgb: tuple[int, int, int],
    mode: str,
    step: int,
    moved_rgb: tuple[int, int, int] | None = None,
    delta_e: float | None = None,
) -> go.Figure:
    vals = list(range(0, 256, step))
    xs, ys, zs, cols = [], [], [], []

    for r in vals:
        for g in vals:
            for b in vals:
                rgb = (r, g, b)
                if mode == "CIELAB":
                    L, a, b2 = rgb_to_lab(rgb)
                else:
                    L0, a0, b0 = rgb_to_oklab(rgb)
                    L, a, b2 = L0 * 100, a0 * 100, b0 * 100
                xs.append(a)
                ys.append(b2)
                zs.append(L)
                cols.append(f"rgb({r},{g},{b})")

    if mode == "CIELAB":
        baseL, baseA, baseB = rgb_to_lab(base_rgb)
    else:
        L0, a0, b0 = rgb_to_oklab(base_rgb)
        baseL, baseA, baseB = L0 * 100, a0 * 100, b0 * 100

    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="markers",
            marker=dict(size=3, color=cols, opacity=0.7),
            name=f"{mode} samples",
            hovertemplate="a: %{x:.1f}<br>b: %{y:.1f}<br>L: %{z:.1f}<extra></extra>",
        )
    )

    if delta_e is not None and delta_e > 0:
        u_steps, v_steps = 28, 14
        u_vals = [i * (2 * math.pi / (u_steps - 1)) for i in range(u_steps)]
        v_vals = [i * (math.pi / (v_steps - 1)) for i in range(v_steps)]
        sx, sy, sz = [], [], []
        for v in v_vals:
            rowx, rowy, rowz = [], [], []
            for u in u_vals:
                rowx.append(baseA + delta_e * math.cos(u) * math.sin(v))
                rowy.append(baseB + delta_e * math.sin(u) * math.sin(v))
                rowz.append(baseL + delta_e * math.cos(v))
            sx.append(rowx)
            sy.append(rowy)
            sz.append(rowz)
        fig.add_trace(
            go.Surface(
                x=sx,
                y=sy,
                z=sz,
                opacity=0.22,
                showscale=False,
                colorscale=[[0, "#ff8c00"], [1, "#ff8c00"]],
                name=f"Iso-ΔE sphere ({delta_e:.1f})",
                hoverinfo="skip",
            )
        )

    fig.add_trace(
        go.Scatter3d(
            x=[baseA],
            y=[baseB],
            z=[baseL],
            mode="markers+text",
            marker=dict(size=8, color="black", symbol="diamond"),
            text=["Base"],
            textposition="top center",
            name="Base color",
        )
    )

    moved_point = None
    if moved_rgb is not None:
        if mode == "CIELAB":
            mL, mA, mB = rgb_to_lab(moved_rgb)
        else:
            mL0, mA0, mB0 = rgb_to_oklab(moved_rgb)
            mL, mA, mB = mL0 * 100, mA0 * 100, mB0 * 100
        moved_point = (mA, mB, mL)

        fig.add_trace(
            go.Scatter3d(
                x=[baseA, mA],
                y=[baseB, mB],
                z=[baseL, mL],
                mode="lines",
                line=dict(color="black", width=6),
                name="Perceptual distance",
                hoverinfo="skip",
            )
        )

        fig.add_trace(
            go.Scatter3d(
                x=[mA],
                y=[mB],
                z=[mL],
                mode="markers+text",
                marker=dict(size=7, color="white", line=dict(color="black", width=2)),
                text=["RGB move"],
                textposition="bottom center",
                name="RGB move",
            )
        )

    span = 85.0
    if delta_e is not None and delta_e > 0:
        span = max(span, delta_e * 1.35)
    if moved_point is not None:
        span = max(
            span,
            abs(moved_point[0] - baseA) * 1.35,
            abs(moved_point[1] - baseB) * 1.35,
            abs(moved_point[2] - baseL) * 1.35,
        )

    fig.update_layout(
        scene=dict(
            xaxis_title="a axis",
            yaxis_title="b axis",
            zaxis_title="L axis",
            xaxis=dict(range=[baseA - span, baseA + span]),
            yaxis=dict(range=[baseB - span, baseB + span]),
            zaxis=dict(range=[baseL - span, baseL + span]),
            aspectmode="cube",
        ),
        title=f"{mode} 3D view",
        height=760,
        margin=dict(l=0, r=0, t=40, b=10),
    )
    return fig


def _delta_e76(lab1: tuple[float, float, float], lab2: tuple[float, float, float]) -> float:
    return math.sqrt((lab1[0] - lab2[0]) ** 2 + (lab1[1] - lab2[1]) ** 2 + (lab1[2] - lab2[2]) ** 2)


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

    st.markdown("### What each axis means")
    e1, e2 = st.columns(2)
    with e1:
        st.markdown(
            """
**CIELAB axes**
- **L***: lightness (0=black, 100=white)
- **a***: green (−) ↔ red (+)
- **b***: blue (−) ↔ yellow (+)

CIELAB is older but widely used (e.g., ΔE metrics in print/quality workflows).
"""
        )
    with e2:
        st.markdown(
            """
**OKLab axes**
- **L**: perceptual lightness (roughly 0..1)
- **a**: green ↔ red component
- **b**: blue ↔ yellow component

OKLab is newer and often smoother for gradients/UI manipulation.
"""
        )

    st.markdown("### Distance intuition")
    st.write(f"Approx ΔE*ab (Lab Euclidean): **{de_lab:.2f}**")
    st.write(f"Scaled OKLab distance (for classroom intuition): **{de_ok:.2f}**")

    st.markdown("### Demo: RGB move in all channels vs perceptual distance")
    st.caption("Move R/G/B together, compute ΔE, then visualize iso-ΔE circle (2D) and sphere (3D).")

    m1, m2, m3 = st.columns(3)
    with m1:
        d_r = st.slider("ΔR", -80, 80, 30, 1)
    with m2:
        d_g = st.slider("ΔG", -80, 80, 0, 1)
    with m3:
        d_b = st.slider("ΔB", -80, 80, 0, 1)

    rgb_demo = (
        max(0, min(255, base_rgb[0] + d_r)),
        max(0, min(255, base_rgb[1] + d_g)),
        max(0, min(255, base_rgb[2] + d_b)),
    )
    rgb_euclidean = math.sqrt(
        (rgb_demo[0] - base_rgb[0]) ** 2 + (rgb_demo[1] - base_rgb[1]) ** 2 + (rgb_demo[2] - base_rgb[2]) ** 2
    )
    base_lab = rgb_to_lab(base_rgb)
    rgb_demo_lab = rgb_to_lab(rgb_demo)
    rgb_demo_de = _delta_e76(base_lab, rgb_demo_lab)

    if "target_de_lab_demo" not in st.session_state:
        st.session_state.target_de_lab_demo = 12.0

    t1, t2 = st.columns([2, 1])
    with t1:
        target_de = st.slider(
            "Target perceptual ΔE (Lab)",
            3.0,
            40.0,
            float(st.session_state.target_de_lab_demo),
            0.5,
            key="target_de_lab_demo",
        )
    with t2:
        st.markdown(" ")
        if st.button("Use current RGB move ΔE"):
            st.session_state.target_de_lab_demo = round(rgb_demo_de * 2) / 2
            st.rerun()

    # one matched perceptual move example: shift along +a* only
    lab_match = (base_lab[0], base_lab[1] + target_de, base_lab[2])
    lab_demo_rgb = lab_to_rgb(lab_match)
    lab_demo_de = _delta_e76(base_lab, rgb_to_lab(lab_demo_rgb))

    s1, s2, s3 = st.columns(3)
    with s1:
        _swatch("Base", base_rgb)
    with s2:
        _swatch(f"RGB move ({d_r:+d},{d_g:+d},{d_b:+d})", rgb_demo)
        st.caption(f"RGB Euclidean distance ≈ **{rgb_euclidean:.2f}**")
        st.caption(f"Observed Lab ΔE*ab ≈ **{rgb_demo_de:.2f}**")
    with s3:
        _swatch("One perceptual move example", lab_demo_rgb)
        st.caption(f"Observed Lab ΔE*ab ≈ **{lab_demo_de:.2f}** (target {target_de:.1f})")

    st.markdown("### 2D explanation: Lab a*b* plane + iso-ΔE circle")
    st.caption(
        "This slice fixes lightness (L*). Dashed circle is all points at the same ΔE radius in this 2D slice. "
        "(True 3D ΔE is a sphere.)"
    )
    l_fixed = st.slider("2D plane lightness L*", 10.0, 95.0, float(lab[0]), 1.0)
    st.plotly_chart(
        _lab_plane_figure(l_fixed, base_lab, moved_lab=rgb_demo_lab, delta_e=target_de),
        use_container_width=True,
        config={"scrollZoom": False},
    )

    st.markdown("### 3D explanation: RGB vs perceptual spaces (side-by-side)")
    st.caption(
        "Left: RGB geometry using Euclidean RGB distance. Right: selected perceptual geometry using ΔE-like distance."
    )
    d1, d2 = st.columns([1, 1])
    with d1:
        space_mode = st.radio("Perceptual 3D model", ["CIELAB", "OKLab"], horizontal=True)
    with d2:
        density = st.select_slider("3D point density", options=["Low", "Medium", "High"], value="Medium")

    if density == "Low":
        step = 64
    elif density == "High":
        step = 32
    else:
        step = 48

    pleft, pright = st.columns(2)
    with pleft:
        st.plotly_chart(
            _rgb_space_3d_figure(base_rgb, rgb_demo, step),
            use_container_width=True,
            config={"scrollZoom": False},
        )
    with pright:
        st.plotly_chart(
            _perceptual_space_3d_figure(base_rgb, space_mode, step, moved_rgb=rgb_demo, delta_e=target_de),
            use_container_width=True,
            config={"scrollZoom": False},
        )

    st.info(
        "Yes, different axis scales between CIELAB and OKLab are normal because they are different coordinate systems. "
        "To make the iso-distance shell look like a true sphere, this view forces equal axis span around the base point."
    )

    with st.expander("Why CIELAB / OKLab matter"):
        st.markdown(
            """
- RGB is device-centric and not perceptually uniform.
- CIELAB (1976) was designed so Euclidean distance is closer to perceived difference.
- OKLab is a newer perceptual model that often behaves better for gradients and UI work.
- In practice: use RGB/HEX for implementation, use Lab/OKLab for comparing or adjusting perceived color difference.

**How to teach with these plots:**
1. Pick a base color.
2. In the 2D plot, keep L* fixed and move across a*/b* directions.
3. In the 3D plot, show how lightness sits on a separate axis from chromatic directions.
4. Compare equal numeric moves in RGB vs perceptual spaces.
"""
        )
