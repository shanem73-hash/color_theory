from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st


def _timeline_figure() -> go.Figure:
    years = [1666, 1810, 1905, 1931, 1990, 2020]
    labels = [
        "Newton\nSpectrum",
        "Goethe\nPerception",
        "Munsell\nOrganization",
        "CIE XYZ\nStandardization",
        "RGB/CMYK\nDigital+Print",
        "OKLab\nModern perceptual",
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years,
            y=[1] * len(years),
            mode="lines+markers+text",
            text=labels,
            textposition="top center",
            marker=dict(size=12, color="#ff8c00"),
            line=dict(color="#444", width=3),
            hovertemplate="%{x}<br>%{text}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Color theory history timeline",
        xaxis_title="Year",
        yaxis=dict(visible=False),
        height=260,
        margin=dict(l=20, r=20, t=45, b=20),
    )
    return fig


def _model_map_figure() -> go.Figure:
    nodes_x = [0, 1.5, 1.5, 3.1, 3.1, 4.7, 4.7]
    nodes_y = [1.2, 2.0, 0.4, 2.0, 0.4, 2.0, 0.4]
    names = ["Human Vision", "RGB", "CMYK", "HSV/HSL", "HEX", "CIELAB", "OKLab"]
    colors = ["#222", "#3b82f6", "#9b59b6", "#16a085", "#f39c12", "#c0392b", "#e67e22"]

    fig = go.Figure()
    edges = [
        (0, 1), (0, 2),
        (1, 3), (1, 4),
        (1, 5), (1, 6),
    ]
    for a, b in edges:
        fig.add_trace(
            go.Scatter(
                x=[nodes_x[a], nodes_x[b]],
                y=[nodes_y[a], nodes_y[b]],
                mode="lines",
                line=dict(color="#888", width=2),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=nodes_x,
            y=nodes_y,
            mode="markers+text",
            text=names,
            textposition="bottom center",
            marker=dict(size=26, color=colors, line=dict(color="white", width=2)),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    fig.update_layout(
        title="Concept map: how color models relate",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=320,
        margin=dict(l=20, r=20, t=45, b=20),
    )
    return fig


def render() -> None:
    st.subheader("Concepts: Color Theory Foundations")
    st.caption("Use this first: historical context + conceptual diagrams before interactive experiments.")

    if "lesson_step" not in st.session_state:
        st.session_state.lesson_step = 1

    st.markdown("### Guided lesson flow (10-minute classroom mode)")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("Step 1: Concepts"):
            st.session_state.lesson_step = 1
    with b2:
        if st.button("Step 2: Add/Sub + HSV"):
            st.session_state.lesson_step = 2
    with b3:
        if st.button("Step 3: Lab/OKLab"):
            st.session_state.lesson_step = 3
    with b4:
        if st.button("Step 4: Converter + Quiz"):
            st.session_state.lesson_step = 4

    step_text = {
        1: "Explain RGB vs CMYK and why multiple color models exist.",
        2: "Run additive/subtractive presets, then show HSV channel effects and 3D HSV model.",
        3: "Demonstrate perceptual distance using Lab/OKLab 2D/3D and ΔE.",
        4: "Use converter for cross-format practice, then assign Quiz mode.",
    }
    st.success(f"Current guided step: **{st.session_state.lesson_step}** — {step_text[st.session_state.lesson_step]}")

    st.plotly_chart(_timeline_figure(), use_container_width=True, config={"scrollZoom": False})

    st.markdown("### Historical notes")
    timeline = [
        ("1666 – Isaac Newton", "Prism experiments separated white light into visible spectrum."),
        ("1810 – Goethe", "Focused on perception and psychological experience of color."),
        ("1900s – Munsell", "Practical teaching framework: hue, value, chroma."),
        ("1931 – CIE XYZ", "Measurement standard enabling modern color conversion."),
        ("Digital + print era", "RGB for emissive displays, CMYK for reflective print."),
        ("Modern perceptual spaces", "CIELAB and OKLab improve distance/perception reasoning."),
    ]
    for era, note in timeline:
        st.markdown(f"- **{era}:** {note}")

    st.plotly_chart(_model_map_figure(), use_container_width=True, config={"scrollZoom": False})

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
### Practical model selection
- **RGB/HEX:** implementation for screens/web
- **CMYK:** print pipelines
- **HSV/HSL:** teaching + intuitive design controls
"""
        )
    with c2:
        st.markdown(
            """
### Perceptual work
- **CIELAB/OKLab:** compare visual differences
- Use ΔE-style distances for matching and tolerance
- Useful for accessibility and quality control
"""
        )

    st.info(
        "Recommended classroom flow: Concepts → Additive/Subtractive → HSV Explorer → CIELAB/OKLab → Converter → Quiz."
    )
