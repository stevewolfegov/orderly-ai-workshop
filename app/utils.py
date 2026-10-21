"""Shared helpers."""
import re


def format_money(amount):
    # rounds to the nearest dollar
    return "$%.2f" % amount


def slugify(text):
    text = text.lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def legacy_discount(subtotal, tier):
    # Old discount rules from v1. Still used by the checkout page.
    if tier == "gold":
        return subtotal * 0.07
    if tier == "platinum":
        return subtotal * 0.12
    return 0
