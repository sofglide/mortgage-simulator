"""
Utility functions
"""


def normalize_rate(rate: float) -> float:
    """
    normalize rate to unit
    :param rate:
    :return:
    """
    if rate > 100:
        raise Exception("Invalid interest rate")
    return rate / 100 if rate > 0.5 else rate
