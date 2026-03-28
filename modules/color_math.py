from __future__ import annotations

import colorsys
from typing import Dict, Tuple


# D65 white point constants for CIELAB conversion
_XN, _YN, _ZN = 0.95047, 1.00000, 1.08883


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = hex_color.strip().lstrip("#")
    if len(h) != 6:
        raise ValueError("HEX must be 6 characters, e.g. #33AAFF")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def rgb_to_hsv_deg(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r, g, b = [c / 255 for c in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360, s * 100, v * 100


def hsv_deg_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    h_n = (h % 360) / 360
    s_n = clamp(s, 0, 100) / 100
    v_n = clamp(v, 0, 100) / 100
    r, g, b = colorsys.hsv_to_rgb(h_n, s_n, v_n)
    return round(r * 255), round(g * 255), round(b * 255)


def rgb_to_hsl_deg(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r, g, b = [c / 255 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100


def hsl_deg_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    h_n = (h % 360) / 360
    s_n = clamp(s, 0, 100) / 100
    l_n = clamp(l, 0, 100) / 100
    r, g, b = colorsys.hls_to_rgb(h_n, l_n, s_n)
    return round(r * 255), round(g * 255), round(b * 255)


def rgb_to_cmy(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r, g, b = [c / 255 for c in rgb]
    return (1 - r) * 100, (1 - g) * 100, (1 - b) * 100


def cmy_to_rgb(c: float, m: float, y: float) -> Tuple[int, int, int]:
    c_n = clamp(c, 0, 100) / 100
    m_n = clamp(m, 0, 100) / 100
    y_n = clamp(y, 0, 100) / 100
    r = (1 - c_n) * 255
    g = (1 - m_n) * 255
    b = (1 - y_n) * 255
    return round(r), round(g), round(b)


def rgb_to_cmyk(rgb: Tuple[int, int, int]) -> Tuple[float, float, float, float]:
    r, g, b = [c / 255 for c in rgb]
    k = 1 - max(r, g, b)
    if k >= 0.999999:
        return 0.0, 0.0, 0.0, 100.0
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return c * 100, m * 100, y * 100, k * 100


def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
    c_n = clamp(c, 0, 100) / 100
    m_n = clamp(m, 0, 100) / 100
    y_n = clamp(y, 0, 100) / 100
    k_n = clamp(k, 0, 100) / 100
    r = 255 * (1 - c_n) * (1 - k_n)
    g = 255 * (1 - m_n) * (1 - k_n)
    b = 255 * (1 - y_n) * (1 - k_n)
    return round(r), round(g), round(b)


def _srgb_to_linear(c: float) -> float:
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def rgb_to_lab(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(rgb[0] / 255), _srgb_to_linear(rgb[1] / 255), _srgb_to_linear(rgb[2] / 255))

    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b

    def f(t: float) -> float:
        d = 6 / 29
        if t > d**3:
            return t ** (1 / 3)
        return t / (3 * d * d) + 4 / 29

    fx, fy, fz = f(x / _XN), f(y / _YN), f(z / _ZN)
    l = 116 * fy - 16
    a = 500 * (fx - fy)
    b2 = 200 * (fy - fz)
    return l, a, b2


def rgb_to_oklab(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(rgb[0] / 255), _srgb_to_linear(rgb[1] / 255), _srgb_to_linear(rgb[2] / 255))

    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b2 = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, a, b2


def converter_state_from_rgb(rgb: Tuple[int, int, int]) -> Dict[str, object]:
    h_hsv, s_hsv, v_hsv = rgb_to_hsv_deg(rgb)
    h_hsl, s_hsl, l_hsl = rgb_to_hsl_deg(rgb)
    c, m, y, k = rgb_to_cmyk(rgb)
    lab = rgb_to_lab(rgb)
    okl = rgb_to_oklab(rgb)
    return {
        "hex": rgb_to_hex(rgb),
        "rgb": rgb,
        "hsv": (h_hsv, s_hsv, v_hsv),
        "hsl": (h_hsl, s_hsl, l_hsl),
        "cmyk": (c, m, y, k),
        "lab": lab,
        "oklab": okl,
    }
