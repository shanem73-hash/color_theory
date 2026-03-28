from __future__ import annotations

import streamlit as st


def render() -> None:
    st.subheader("Concepts: Color Theory Timeline + Model Notes")
    st.caption("A quick historical and conceptual guide to connect the interactive demos to theory.")

    st.markdown("### Color theory timeline (short)")
    timeline = [
        ("1666 – Isaac Newton", "Prism experiments showed white light can be separated into a visible spectrum."),
        (
            "1810 – Goethe's Theory of Colours",
            "Emphasized human perception and psychological effects of color, complementing pure physics views.",
        ),
        (
            "Early 1900s – Munsell system",
            "Organized color by hue, value, and chroma; highly influential in education and art.",
        ),
        (
            "1931 – CIE XYZ",
            "Established a standardized mathematical framework for color measurement and conversion.",
        ),
        (
            "Digital era – RGB displays",
            "Screens emit light, so additive RGB became central for digital color creation.",
        ),
        (
            "Print era – CMYK workflows",
            "Printing relies on subtractive inks; device and paper profiles affect final output.",
        ),
    ]

    for era, note in timeline:
        st.markdown(f"- **{era}:** {note}")

    st.markdown("### Key model intuition")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
- **RGB (Additive):** Best for screens/light.
- **CMY/CMYK (Subtractive):** Best for inks/printing.
- **HSV/HSB:** Great for teaching and creative control (what color, how vivid, how bright).
"""
        )

    with c2:
        st.markdown(
            """
- **HSL:** Similar to HSV but uses lightness channel.
- **HEX:** Compact web representation of RGB.
- **CIELAB/OKLab (advanced):** Better for perceptual difference tasks.
"""
        )

    st.info(
        "Teaching tip: have students compare one color across RGB, HSV, HSL, and CMYK to learn that "
        "representation changes while the intent stays similar."
    )
