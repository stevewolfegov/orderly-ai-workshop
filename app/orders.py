from app.db import get_conn
from app.pricing import calculate_order_total


def create_order(customer, items, promo_code=None):
    conn = get_conn()
    priced = calculate_order_total(items, customer, promo_code, conn=conn)
    if not priced["ok"]:
        conn.close()
        return priced

    cur = conn.execute(
        """INSERT INTO orders (customer_id, subtotal, discount, shipping, tax, total, promo_code)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            customer["id"],
            priced["subtotal"],
            priced["discount"],
            priced["shipping"],
            priced["tax"],
            priced["total"],
            priced["promo_code"],
        ),
    )
    order_id = cur.lastrowid
    for line in priced["lines"]:
        conn.execute(
            """INSERT INTO order_items (order_id, product_id, quantity, unit_price, line_total)
               VALUES (?, ?, ?, ?, ?)""",
            (order_id, line["product_id"], line["quantity"], line["unit_price"], line["line_total"]),
        )
    conn.commit()
    conn.close()
    priced["order_id"] = order_id
    return priced


def get_order(order_id):
    conn = get_conn()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if order is None:
        conn.close()
        return None
    items = conn.execute(
        """SELECT oi.*, p.sku, p.name FROM order_items oi
           JOIN products p ON p.id = oi.product_id
           WHERE oi.order_id = ?""",
        (order_id,),
    ).fetchall()
    conn.close()
    result = dict(order)
    result["items"] = [dict(i) for i in items]
    return result


def list_orders(customer_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM orders WHERE customer_id = ? ORDER BY id DESC", (customer_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

