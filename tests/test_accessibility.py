from __future__ import annotations

import re
from pathlib import Path


STYLESHEET = (
    Path(__file__).resolve().parents[1] / "timemanager" / "static" / "styles.css"
)


def _relative_luminance(hex_color: str) -> float:
    channels = [
        int(hex_color[index : index + 2], 16) / 255
        for index in (1, 3, 5)
    ]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast_ratio(first: str, second: str) -> float:
    lighter, darker = sorted(
        (_relative_luminance(first), _relative_luminance(second)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def _color_tokens() -> dict[str, str]:
    stylesheet = STYLESHEET.read_text(encoding="utf-8")
    return dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6});", stylesheet))


def test_functional_color_tokens_meet_documented_contrast_thresholds():
    tokens = _color_tokens()
    adjacent_surfaces = (
        tokens["paper"],
        tokens["surface"],
        tokens["surface-muted"],
        tokens["mint"],
        tokens["mint-soft"],
        "#ffffff",
    )

    for surface in adjacent_surfaces:
        assert _contrast_ratio(tokens["focus-indicator"], surface) >= 3
        assert _contrast_ratio(tokens["control-border"], surface) >= 3

    for input_surface in (tokens["paper"], tokens["surface"], "#ffffff"):
        assert _contrast_ratio(tokens["placeholder-text"], input_surface) >= 4.5


def test_functional_color_tokens_are_used_for_controls_and_focus():
    stylesheet = STYLESHEET.read_text(encoding="utf-8")

    assert "outline: 3px solid var(--focus-indicator);" in stylesheet
    assert "border: 1px solid var(--control-border);" in stylesheet
    assert "border: 2px solid var(--control-border);" in stylesheet
    assert "color: var(--placeholder-text);" in stylesheet
    assert "@media (forced-colors: active)" in stylesheet
