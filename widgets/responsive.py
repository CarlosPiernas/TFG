"""
Responsive scaling utilities for Anomalías vs Guardianes.

Base design resolution: 400 x 800 (portrait mobile).
All helpers return values in pixels scaled to the actual window size,
so layouts look identical on the base device and correct on any other.

Usage:
    from widgets.responsive import sw, sh, sf, sdp

    width=sw(90)        # 90px on 400-wide screen, scales proportionally
    height=sh(55)       # 55px on 800-tall screen, scales proportionally
    font_size=sf(14)    # font scaled by the smaller axis (avoids huge text on tablets)
    radius=[sdp(8)]     # dp-style value scaled to screen width
"""

from kivy.core.window import Window
from kivy.metrics import dp

# Base design dimensions
_BASE_W = 400.0
_BASE_H = 800.0


def sw(px: float) -> float:
    """Scale a width value relative to the base 400px design width."""
    return (Window.width / _BASE_W) * px


def sh(px: float) -> float:
    """Scale a height value relative to the base 800px design height."""
    return (Window.height / _BASE_H) * px


def sf(px: float) -> float:
    """
    Scale a font size using the smaller axis ratio.
    Prevents text from becoming disproportionately large on wide screens.
    """
    scale = min(Window.width / _BASE_W, Window.height / _BASE_H)
    return scale * px


def sdp(px: float) -> float:
    """
    Like dp() but also scaled to screen width.
    Use for border radii, spacing, padding where dp alone isn't enough.
    """
    return (Window.width / _BASE_W) * dp(px)
