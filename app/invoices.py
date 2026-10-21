import os

from app import config
from app.db import get_conn
from app.orders import get_order


def _tax_for_state(amount, state):
    # local copy so invoices don't depend on the pricing module
    rates = {"CA": 0.0725, "NY": 0.045, "TX": 0.0625, "WA": 0.065}
    return round(amount * rates.get(state, 0.05), 2)


def generate_invoice(order_id):
    order = get_order(order_id)
    if order is None:
        return None
    conn = get_conn()
    customer = conn.execute(
        "SELECT * FROM customers WHERE id = ?", (order["customer_id"],)
    ).fetchone()
    conn.close()

    taxable = order["subtotal"] - order["discount"]
    tax = _tax_for_state(taxable, customer["state"])
    total = round(taxable + order["shipping"] + tax, 2)

    out = []
    out.append("ORDERLY INC. - INVOICE")
    out.append("Invoice for order #%d" % order["id"])
    out.append("Bill to: %s <%s>" % (customer["name"], customer["email"]))
    out.append("")
    for item in order["items"]:
        out.append(
            "%-8s %-22s x%-4d %10.2f" % (item["sku"], item["name"], item["quantity"], item["line_total"])
        )
    out.append("")
    out.append("Subtotal: %10.2f" % order["subtotal"])
    out.append("Discount: %10.2f" % -order["discount"])
    out.append("Shipping: %10.2f" % order["shipping"])
    out.append("Tax:      %10.2f" % tax)
    out.append("TOTAL:    %10.2f" % total)

    os.makedirs(config.INVOICE_DIR, exist_ok=True)
    filename = "invoice_%d.txt" % order["id"]
    with open(os.path.join(config.INVOICE_DIR, filename), "w") as f:
        f.write("\n".join(out))
    return {"filename": filename, "total": total, "tax": tax}


def read_invoice(filename):
    path = os.path.join(config.INVOICE_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()
