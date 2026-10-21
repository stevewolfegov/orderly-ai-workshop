"""Loads demo data. Run with: python -m app.seed"""

from app.db import get_conn, init_db

CUSTOMERS = [
    # name, email, state, tier, api_token
    ("Ada Lovelace", "ada@example.com", "CA", "standard", "tok_ada_123"),
    ("Grace Hopper", "grace@example.com", "NY", "gold", "tok_grace_456"),
    ("Linus Torvalds", "linus@example.com", "TX", "platinum", "tok_linus_789"),
    ("Margaret Hamilton", "margaret@example.com", "OR", "standard", "tok_margaret_000"),
]

PRODUCTS = [
    # sku, name, category, price, active
    ("WID-001", "Widget", "parts", 19.99, 1),
    ("GAD-002", "Gadget", "parts", 49.50, 1),
    ("GIZ-003", "Gizmo Pro", "devices", 250.00, 1),
    ("CAB-004", "USB-C Cable", "accessories", 9.99, 1),
    ("HUB-005", "Docking Hub", "accessories", 129.00, 1),
    ("KEY-006", "Mechanical Keyboard", "peripherals", 89.00, 1),
    ("MON-007", "4K Monitor", "peripherals", 399.00, 1),
    ("OLD-008", "Legacy Dongle", "accessories", 14.99, 0),
]

PROMO_CODES = [
    # code, kind, value, min_subtotal, expires, active
    ("SAVE10", "percent", 10, 100, "2099-12-31", 1),
    ("TENOFF", "fixed", 10, 50, None, 1),
    ("FREESHIP", "freeship", 0, 0, None, 1),
    ("SUMMER2023", "percent", 20, 0, "2023-09-01", 1),
    ("STAFF50", "percent", 50, 0, None, 0),
]


def seed():
    init_db()
    conn = get_conn()
    conn.execute("DELETE FROM order_items")
    conn.execute("DELETE FROM orders")
    conn.execute("DELETE FROM customers")
    conn.execute("DELETE FROM products")
    conn.execute("DELETE FROM promo_codes")
    conn.executemany(
        "INSERT INTO customers (name, email, state, tier, api_token) VALUES (?, ?, ?, ?, ?)",
        CUSTOMERS,
    )
    conn.executemany(
        "INSERT INTO products (sku, name, category, price, active) VALUES (?, ?, ?, ?, ?)",
        PRODUCTS,
    )
    conn.executemany(
        "INSERT INTO promo_codes (code, kind, value, min_subtotal, expires, active) VALUES (?, ?, ?, ?, ?, ?)",
        PROMO_CODES,
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed()
    print("Seeded demo data.")
