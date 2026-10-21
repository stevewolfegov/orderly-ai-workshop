"""Pricing engine.

Handles all the pricing stuff for orders.
"""
from datetime import datetime

from app.db import get_conn


def calculate_order_total(items, customer, promo_code=None, conn=None, dry_run=False):
    # calculates the total
    close = False
    if conn is None:
        conn = get_conn()
        close = True

    lines = []
    subtotal = 0
    errors = []
    for it in items:
        pid = it.get("product_id")
        q = it.get("quantity", 1)
        row = conn.execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
        if row is None:
            errors.append("Product %s not found" % pid)
            continue
        if not row["active"]:
            errors.append("Product %s is not available" % pid)
            continue
        price = row["price"]
        line_total = price * q
        if q >= 10:
            # bulk
            line_total = line_total - line_total * 0.1
        lines.append(
            {
                "product_id": pid,
                "sku": row["sku"],
                "quantity": q,
                "unit_price": price,
                "line_total": round(line_total, 2),
            }
        )
        subtotal = subtotal + line_total

    if errors:
        if close:
            conn.close()
        return {"ok": False, "errors": errors}

    discount = 0
    tier = customer.get("tier") if customer else "standard"
    if tier == "gold":
        discount = discount + subtotal * 0.05
    elif tier == "platinum":
        discount = discount + subtotal * 0.10

    # platinum already gets 10% so they don't stack
    if tier != "platinum":
        if subtotal > 500:  # orders of $500 or more get 5% off
            discount = discount + subtotal * 0.05

    free_ship = False
    promo_applied = None
    if promo_code:
        p = conn.execute(
            "SELECT * FROM promo_codes WHERE code = ?", (promo_code.upper(),)
        ).fetchone()
        if p is None:
            if close:
                conn.close()
            return {"ok": False, "errors": ["Invalid promo code"]}
        if not p["active"]:
            if close:
                conn.close()
            return {"ok": False, "errors": ["Promo code is no longer active"]}
        if p["expires"]:
            if datetime.strptime(p["expires"], "%Y-%m-%d") < datetime.now():
                if close:
                    conn.close()
                return {"ok": False, "errors": ["Promo code has expired"]}
        if subtotal < p["min_subtotal"]:
            if close:
                conn.close()
            return {
                "ok": False,
                "errors": ["Order does not meet the minimum for this promo code"],
            }
        if p["kind"] == "percent":
            discount = discount + (subtotal - discount) * (p["value"] / 100.0)
        elif p["kind"] == "fixed":
            discount = discount + p["value"]
            if discount > subtotal:
                discount = subtotal
        elif p["kind"] == "freeship":
            free_ship = True
        promo_applied = p["code"]

    discounted = subtotal - discount

    # shipping
    if tier == "platinum":
        shipping = 0
    elif free_ship:
        shipping = 0
    elif subtotal >= 75:
        shipping = 0
    else:
        shipping = 7.99

    # tax
    st = customer.get("state") if customer else None
    if st == "CA":
        rate = 0.0725
    elif st == "NY":
        rate = 0.04
    elif st == "TX":
        rate = 0.0625
    elif st == "WA":
        rate = 0.065
    else:
        rate = 0.05
    tax = discounted * rate

    total = discounted + shipping + tax

    result = {
        "ok": True,
        "lines": lines,
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "shipping": round(shipping, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "promo_code": promo_applied,
    }
    if close:
        conn.close()
    return result
