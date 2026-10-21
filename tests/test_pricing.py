"""Characterization tests for calculate_order_total.

Expected values come from docs/PRICING_RULES.md, not from the current code.
"""
import pytest

from app.pricing import calculate_order_total

ADA = {"id": 1, "tier": "standard", "state": "CA"}
GRACE = {"id": 2, "tier": "gold", "state": "NY"}
LINUS = {"id": 3, "tier": "platinum", "state": "TX"}
MARGARET = {"id": 4, "tier": "standard", "state": "OR"}

WIDGET, GADGET, GIZMO, CABLE, HUB, KEYBOARD, MONITOR, DONGLE = range(1, 9)


def price(customer, *lines, promo=None):
    items = [{"product_id": pid, "quantity": qty} for pid, qty in lines]
    return calculate_order_total(items, customer, promo)


def test_small_standard_order_pays_flat_shipping(seeded_db):
    result = price(ADA, (WIDGET, 1))
    assert result["subtotal"] == 19.99
    assert result["discount"] == 0
    assert result["shipping"] == 7.99
    assert result["tax"] == 1.45
    assert result["total"] == 29.43


def test_nine_units_get_no_bulk_discount(seeded_db):
    result = price(ADA, (WIDGET, 9))
    assert result["lines"][0]["line_total"] == 179.91


def test_bulk_discount_applies_at_ten_units(seeded_db):
    result = price(ADA, (WIDGET, 12))
    assert result["lines"][0]["line_total"] == 215.89


def test_bulk_discount_applies_per_line(seeded_db):
    result = price(ADA, (WIDGET, 10), (CABLE, 2))
    assert result["lines"][0]["line_total"] == 179.91
    assert result["lines"][1]["line_total"] == 19.98


def test_gold_customer_gets_five_percent(seeded_db):
    result = price(GRACE, (HUB, 1))
    assert result["discount"] == 6.45
    assert result["tax"] == 4.90
    assert result["total"] == 127.45


def test_platinum_customer_gets_ten_percent_and_free_shipping(seeded_db):
    result = price(LINUS, (WIDGET, 1))
    assert result["discount"] == 2.00
    assert result["shipping"] == 0


def test_order_size_discount_starts_at_exactly_500(seeded_db):
    result = price(ADA, (GIZMO, 2))
    assert result["subtotal"] == 500.00
    assert result["discount"] == 25.00
    assert result["tax"] == 34.44
    assert result["total"] == 509.44


def test_gold_customer_stacks_order_size_discount(seeded_db):
    result = price(GRACE, (GIZMO, 3))
    assert result["discount"] == 75.00


def test_platinum_customer_does_not_stack_order_size_discount(seeded_db):
    result = price(LINUS, (GIZMO, 3))
    assert result["discount"] == 75.00


def test_percent_promo_applies_after_automatic_discounts(seeded_db):
    result = price(ADA, (WIDGET, 10), promo="SAVE10")
    assert result["subtotal"] == 179.91
    assert result["discount"] == 17.99
    assert result["shipping"] == 0
    assert result["tax"] == 11.74
    assert result["total"] == 173.66


def test_free_shipping_uses_discounted_subtotal(seeded_db):
    result = price(ADA, (GADGET, 1), (CABLE, 3), promo="TENOFF")
    assert result["subtotal"] == 79.47
    assert result["discount"] == 10.00
    assert result["shipping"] == 7.99
    assert result["total"] == 82.50


def test_freeship_promo_waives_shipping(seeded_db):
    result = price(ADA, (WIDGET, 1), promo="FREESHIP")
    assert result["shipping"] == 0
    assert result["discount"] == 0


def test_promo_code_is_case_insensitive(seeded_db):
    assert price(ADA, (WIDGET, 10), promo="save10")["promo_code"] == "SAVE10"


@pytest.mark.parametrize(
    "promo, message",
    [
        ("NOPE", "Invalid promo code"),
        ("STAFF50", "Promo code is no longer active"),
        ("SUMMER2023", "Promo code has expired"),
        ("SAVE10", "Order does not meet the minimum for this promo code"),
    ],
)
def test_invalid_promo_codes_are_rejected(seeded_db, promo, message):
    result = price(ADA, (WIDGET, 1), promo=promo)
    assert result == {"ok": False, "errors": [message]}


def test_inactive_product_is_rejected(seeded_db):
    result = price(ADA, (DONGLE, 1))
    assert result == {"ok": False, "errors": ["Product 8 is not available"]}


def test_unknown_state_uses_default_tax_rate(seeded_db):
    result = price(MARGARET, (HUB, 1))
    assert result["tax"] == 6.45
    assert result["total"] == 135.45
