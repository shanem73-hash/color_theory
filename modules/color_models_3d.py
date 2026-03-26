from __future__ import annotations

import colorsys

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from modules.color_math import hsv_deg_to_rgb, rgb_to_hex


def _rgb_cube_figure(step: int, selected_rgb: tuple[int, int, int]) -> go.Figure:
    vals = np.arange(0, 256, step)
    rr, gg, bb = np.meshgrid(vals, vals, vals)
    r = rr.flatten()
    g = gg.flatten()
    b = bb.flatten()

    colors = [f"rgb({ri},{gi},{bi})" for ri, gi, bi in zip(r, g, b)]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=r,
            y=g,
            z=b,
            mode="markers",
            marker=dict(size=3, color=colors, opacity=0.65),
            name="RGB samples",
            hovertemplate="R:%{x}<br>G:%{y}<br>B:%{z}<extra></extra>",
        )
    )

    sr, sg, sb = selected_rgb
    fig.add_trace(
        go.Scatter3d(
            x=[sr],
            y=[sg],
            z=[sb],
            mode="markers+text",
            marker=dict(size=8, color="black", symbol="diamond"),
            text=["Selected"],
            textposition="top center",
            name="Selected color",
            hovertemplate=f"Selected<br>R:{sr}<br>G:{sg}<br>B:{sb}<extra></extra>",
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
        margin=dict(l=0, r=0, b=20, t=40),
        height=900,
        legend=dict(orientation="h"),
    )
    return fig


def _hsv_cylinder_figure(h_step: int, s_steps: int, v_steps: int, selected_hsv: tuple[int, int, int]) -> go.Figure:
    h_vals = np.arange(0, 360, h_step)
    s_vals = np.linspace(0.15, 1.0, s_steps)
    v_vals = np.linspace(0.2, 1.0, v_steps)

    xs, ys, zs, cols = [], [], [], []

    for h in h_vals:
        theta = np.deg2rad(h)
        for s in s_vals:
            for v in v_vals:
                x = s * np.cos(theta)
                y = s * np.sin(theta)
                z = v
                r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
                xs.append(x)
                ys.append(y)
                zs.append(z)
                cols.append(f"rgb({round(r*255)},{round(g*255)},{round(b*255)})")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="markers",
            marker=dict(size=2.6, color=cols, opacity=0.62),
            name="HSV samples",
            hovertemplate="x:%{x:.2f}<br>y:%{y:.2f}<br>V:%{z:.2f}<extra></extra>",
        )
    )

    h, s, v = selected_hsv
    theta = np.deg2rad(h)
    s_n = s / 100
    v_n = v / 100
    sx = s_n * np.cos(theta)
    sy = s_n * np.sin(theta)
    sz = v_n

    fig.add_trace(
        go.Scatter3d(
            x=[sx],
            y=[sy],
            z=[sz],
            mode="markers+text",
            marker=dict(size=8, color="black", symbol="diamond"),
            text=["Selected"],
            textposition="top center",
            name="Selected HSV",
            hovertemplate=f"H:{h}°<br>S:{s}%<br>V:{v}%<extra></extra>",
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="S·cos(H)",
            yaxis_title="S·sin(H)",
            zaxis_title="V",
            xaxis=dict(range=[-1, 1]),
            yaxis=dict(range=[-1, 1]),
            zaxis=dict(range=[0, 1]),
            aspectmode="cube",
        ),
        margin=dict(l=0, r=0, b=20, t=40),
        height=900,
        legend=dict(orientation="h"),
    )
    return fig


def render() -> None:
    st.subheader("3D Color Models")
    st.caption("Explore color as geometry: RGB cube and HSV cylindrical model.")

    c1, c2, c3 = st.columns(3)
    with c1:
        sel_r = st.slider("Selected R", 0, 255, 80)
    with c2:
        sel_g = st.slider("Selected G", 0, 255, 160)
    with c3:
        sel_b = st.slider("Selected B", 0, 255, 220)

    st.markdown(
        f"**Selected color:** `{(sel_r, sel_g, sel_b)}` | `{rgb_to_hex((sel_r, sel_g, sel_b))}`"
    )

    h, s, v = colorsys.rgb_to_hsv(sel_r / 255, sel_g / 255, sel_b / 255)
    h_deg, s_pct, v_pct = int(round(h * 360)) % 360, int(round(s * 100)), int(round(v * 100))

    density_col, _ = st.columns([1, 2])
    with density_col:
        density = st.select_slider("Point density", options=["Low", "Medium", "High"], value="Medium")

    if density == "Low":
        rgb_step = 64
        h_step, s_steps, v_steps = 24, 6, 4
    elif density == "High":
        rgb_step = 32
        h_step, s_steps, v_steps = 12, 10, 7
    else:
        rgb_step = 48
        h_step, s_steps, v_steps = 18, 8, 5

    t1, t2 = st.tabs(["RGB Cube", "HSV 3D Model"])

    with t1:
        st.plotly_chart(_rgb_cube_figure(rgb_step, (sel_r, sel_g, sel_b)), use_container_width=True)
        st.caption("Each point is a sampled RGB color in 3D space. Black point marks selected color.")

    with t2:
        st.plotly_chart(
            _hsv_cylinder_figure(h_step, s_steps, v_steps, (h_deg, s_pct, v_pct)),
            use_container_width=True,
        )
        rgb_from_hsv = hsv_deg_to_rgb(h_deg, s_pct, v_pct)
        st.caption(
            f"Selected RGB maps to HSV ≈ ({h_deg}°, {s_pct}%, {v_pct}%) and back to RGB {rgb_from_hsv}."
        )
