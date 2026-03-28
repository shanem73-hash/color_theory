from __future__ import annotations

import colorsys
import math
import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st


def _rgb_auto_figure(frame: int) -> go.Figure:
    vals = np.arange(0, 256, 64)
    rr, gg, bb = np.meshgrid(vals, vals, vals)
    r = rr.flatten()
    g = gg.flatten()
    b = bb.flatten()
    colors = [f"rgb({ri},{gi},{bi})" for ri, gi, bi in zip(r, g, b)]

    angle = (frame % 120) * 2 * math.pi / 120
    eye = dict(x=2.1 * math.cos(angle), y=2.1 * math.sin(angle), z=1.2)

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=r, y=g, z=b, mode="markers", marker=dict(size=3, color=colors, opacity=0.6), name="RGB space"
            )
        ]
    )
    fig.update_layout(
        title="Auto Demo 1: RGB cube rotates (additive light space)",
        scene=dict(
            xaxis_title="R", yaxis_title="G", zaxis_title="B",
            xaxis=dict(range=[0, 255]), yaxis=dict(range=[0, 255]), zaxis=dict(range=[0, 255]),
            aspectmode="cube", camera=dict(eye=eye)
        ),
        height=620,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig


def _hsv_auto_figure(frame: int) -> go.Figure:
    h_vals = np.arange(0, 360, 24)
    s_vals = np.linspace(0.25, 1.0, 5)
    v_vals = np.linspace(0.3, 1.0, 4)
    xs, ys, zs, cols = [], [], [], []
    for h in h_vals:
        t = np.deg2rad(h)
        for s in s_vals:
            for v in v_vals:
                x = s * np.cos(t)
                y = s * np.sin(t)
                z = v
                rr, gg, bb = [round(c * 255) for c in colorsys.hsv_to_rgb(h / 360, s, v)]
                xs.append(x); ys.append(y); zs.append(z); cols.append(f"rgb({rr},{gg},{bb})")

    h = (frame * 6) % 360
    t = np.deg2rad(h)
    sx, sy, sz = 0.9 * np.cos(t), 0.9 * np.sin(t), 0.9

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="markers", marker=dict(size=2.5, color=cols, opacity=0.6), name="HSV"))
    fig.add_trace(go.Scatter3d(x=[sx], y=[sy], z=[sz], mode="markers+text", marker=dict(size=8, color="black"), text=[f"H={h}°"], textposition="top center"))
    fig.update_layout(
        title="Auto Demo 2: Hue sweeps around HSV cylinder",
        scene=dict(xaxis_title="S·cos(H)", yaxis_title="S·sin(H)", zaxis_title="V", aspectmode="cube"),
        height=620,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig


def _lab_auto_figure(frame: int) -> go.Figure:
    # lightweight shell + moving point
    base = (60.0, 20.0, -10.0)
    radius = 25.0
    u_steps, v_steps = 26, 14
    u_vals = [i * (2 * math.pi / (u_steps - 1)) for i in range(u_steps)]
    v_vals = [i * (math.pi / (v_steps - 1)) for i in range(v_steps)]
    sx, sy, sz = [], [], []
    for v in v_vals:
        rowx, rowy, rowz = [], [], []
        for u in u_vals:
            rowx.append(base[1] + radius * math.cos(u) * math.sin(v))
            rowy.append(base[2] + radius * math.sin(u) * math.sin(v))
            rowz.append(base[0] + radius * math.cos(v))
        sx.append(rowx); sy.append(rowy); sz.append(rowz)

    a = base[1] + radius * math.cos(frame * 2 * math.pi / 120)
    b = base[2] + radius * math.sin(frame * 2 * math.pi / 120)
    l = base[0]

    fig = go.Figure()
    fig.add_trace(go.Surface(x=sx, y=sy, z=sz, opacity=0.22, showscale=False, colorscale=[[0, "#ff8c00"], [1, "#ff8c00"]]))
    fig.add_trace(go.Scatter3d(x=[base[1]], y=[base[2]], z=[base[0]], mode="markers+text", marker=dict(size=8, color="black"), text=["Base"], textposition="top center"))
    fig.add_trace(go.Scatter3d(x=[a], y=[b], z=[l], mode="markers+text", marker=dict(size=7, color="white", line=dict(color="black", width=2)), text=["Equal ΔE path"], textposition="bottom center"))
    fig.update_layout(
        title="Auto Demo 3: Equal perceptual distance (iso-ΔE sphere)",
        scene=dict(xaxis_title="a*", yaxis_title="b*", zaxis_title="L*", aspectmode="cube"),
        height=620,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig


def render() -> None:
    st.subheader("Auto Lesson Mode (3D demos + instruction)")
    st.caption("Play automated 3D teaching scenes with synced instruction captions.")

    if "auto_scene" not in st.session_state:
        st.session_state.auto_scene = "RGB"
    if "auto_frame" not in st.session_state:
        st.session_state.auto_frame = 0
    if "auto_running" not in st.session_state:
        st.session_state.auto_running = False

    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        st.session_state.auto_scene = st.selectbox("Scene", ["RGB", "HSV", "CIELAB"], index=["RGB", "HSV", "CIELAB"].index(st.session_state.auto_scene))
    with c2:
        if st.button("▶ Start"):
            st.session_state.auto_running = True
    with c3:
        if st.button("⏸ Pause"):
            st.session_state.auto_running = False
    with c4:
        if st.button("↺ Reset"):
            st.session_state.auto_frame = 0
            st.session_state.auto_running = False

    frame = st.session_state.auto_frame
    if st.session_state.auto_scene == "RGB":
        fig = _rgb_auto_figure(frame)
        note = "Instruction: Explain additive space and camera orbit around the RGB cube."
    elif st.session_state.auto_scene == "HSV":
        fig = _hsv_auto_figure(frame)
        note = "Instruction: Watch hue rotation while saturation/value stay near fixed levels."
    else:
        fig = _lab_auto_figure(frame)
        note = "Instruction: Point moving on sphere keeps equal perceptual distance from base color."

    st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": False, "displayModeBar": True})
    st.info(note)

    if st.session_state.auto_running:
        time.sleep(0.9)
        st.session_state.auto_frame = (st.session_state.auto_frame + 1) % 120
        st.rerun()
