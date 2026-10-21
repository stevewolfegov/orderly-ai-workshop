"""Order pricing. The business rules live in docs/PRICING_RULES.md."""
from datetime import datetime

from app import config
from app.db import get_conn

BULK_MIN_QUANTITY = 10
BULK_DISCOUNT = 0.10
TIER_DISCOUNTS = {"gold": 0.05, "platinum": 0.10}
ORDER_SIZE_THRESHOLD = 500
ORDER_SIZE_DISCOUNT = 0.05
FREE_SHIPPING_THRESHOLD = 75


def tax_rate(state):
    return config.TAX_RATES.get(state, config.DEFAULT_TAX_RATE)


def calculate_order_total(items, customer, promo_code=None, conn=None):
    owns_conn = conn is None
    if owns_conn:
        conn = get_conn()
    try:
        return _price_order(conn, items, customer or {}, promo_code)
    finally:
        if owns_conn:
            conn.close()


def _price_order(conn, items, customer, promo_code):
    lines, subtotal, errors = _price_lines(conn, items)
    if errors:
        return _failure(*errors)

    tier = customer.get("tier")
    discount = _automatic_discount(subtotal, tier)

    free_shipping = False
    promo = None
    if promo_code:
        promo, error = _load_promo(conn, promo_code, subtotal)
        if error:
            return _failure(error)
        discount, free_shipping = _apply_promo(promo, subtotal, discount)

    discounted = subtotal - discount
    shipping = _shipping_cost(tier, free_shipping, discounted)
    tax = discounted * tax_rate(customer.get("state"))
    total = discounted + shipping + tax

    return {
        "ok": True,
        "lines": lines,
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "shipping": round(shipping, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "promo_code": promo["code"] if promo else None,
    }


def _failure(*errors):
    return {"ok": False, "errors": list(errors)}


def _price_lines(conn, items):
    lines = []
    errors = []
    subtotal = 0
    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)
        product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if product is None:
            errors.append("Product %s not found" % product_id)
            continue
        if not product["active"]:
            errors.append("Product %s is not available" % product_id)
            continue
        line_total = product["price"] * quantity
        if quantity >= BULK_MIN_QUANTITY:
            line_total -= line_total * BULK_DISCOUNT
        lines.append(
            {
                "product_id": product_id,
                "sku": product["sku"],
                "quantity": quantity,
                "unit_price": product["price"],
                "line_total": round(line_total, 2),
            }
        )
        subtotal += line_total
    return lines, subtotal, errors


def _automatic_discount(subtotal, tier):
    discount = subtotal * TIER_DISCOUNTS.get(tier, 0)
    # Platinum's tier discount replaces the order-size discount.
    if tier != "platinum" and subtotal >= ORDER_SIZE_THRESHOLD:
        discount += subtotal * ORDER_SIZE_DISCOUNT
    return discount


def _load_promo(conn, code, subtotal):
    promo = conn.execute(
        "SELECT * FROM promo_codes WHERE code = ?", (code.upper(),)
    ).fetchone()
    if promo is None:
        return None, "Invalid promo code"
    if not promo["active"]:
        return None, "Promo code is no longer active"
    if promo["expires"] and datetime.strptime(promo["expires"], "%Y-%m-%d") < datetime.now():
        return None, "Promo code has expired"
    if subtotal < promo["min_subtotal"]:
        return None, "Order does not meet the minimum for this promo code"
    return promo, None


def _apply_promo(promo, subtotal, discount):
    if promo["kind"] == "percent":
        return discount + (subtotal - discount) * (promo["value"] / 100.0), False
    if promo["kind"] == "fixed":
        return min(discount + promo["value"], subtotal), False
    if promo["kind"] == "freeship":
        return discount, True
    return discount, False


def _shipping_cost(tier, free_shipping, discounted):
    if tier == "platinum" or free_shipping or discounted >= FREE_SHIPPING_THRESHOLD:
        return 0
    return config.FLAT_SHIPPING
