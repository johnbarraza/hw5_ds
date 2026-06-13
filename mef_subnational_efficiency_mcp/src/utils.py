"""Shared utility helpers — Persona 3."""

import logging


def get_logger(name):
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


def format_soles(value):
    return f"S/ {value:,.0f}"


def safe_divide(numerator, denominator, default=0):
    if denominator == 0:
        return default
    return numerator / denominator
