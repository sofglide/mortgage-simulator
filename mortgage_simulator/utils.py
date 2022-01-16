"""
Utility functions
"""
from typing import Optional

from colorclass import Color

COLORS = {
    "Property value": "autoyellow",
    "Down payment": "automagenta",
    "Monthly payment": "autogreen",
    "Term": "autocyan",
}


def normalize_rate(rate: float) -> float:
    """
    normalize rate to unit
    :param rate:
    :return:
    """
    if rate > 100:
        raise Exception("Invalid interest rate")
    return rate / 100 if rate > 0.5 else rate


def add_color(field: str, text: Optional[str] = None) -> str:
    """
    Add color to fields
    :param field:
    :param text:
    :return:
    """
    text = text or field
    if field in COLORS:
        return Color(f"{{{COLORS[field]}}}{text}{{/{COLORS[field]}}}")
    return text
