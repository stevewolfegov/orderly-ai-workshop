from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from app import invoices, orders
from app.auth import get_current_customer, load_saved_cart, require_admin
from app.db import get_conn, init_db
from app.pricing import calculate_order_total


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(title="Orderly API", version="0.3.1", lifespan=lifespan)


class OrderItem(BaseModel):
    product_id: int
    quantity: int = 1


class OrderRequest(BaseModel):
    items: List[OrderItem]
    promo_code: Optional[str] = None


class CartRestoreRequest(BaseModel):
    cart: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/products")
def list_products(q: Optional[str] = None):
    conn = get_conn()
    if q:
        sql = f"SELECT * FROM products WHERE active = 1 AND name LIKE '%{q}%'"
    else:
        sql = "SELECT * FROM products WHERE active = 1"
    rows = conn.execute(sql).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_conn()
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(row)


@app.post("/quote")
def quote(req: OrderRequest, customer=Depends(get_current_customer)):
    items = [i.model_dump() for i in req.items]
    result = calculate_order_total(items, customer, req.promo_code)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["errors"])
    return result


@app.post("/orders", status_code=201)
def place_order(req: OrderRequest, customer=Depends(get_current_customer)):
    items = [i.model_dump() for i in req.items]
    result = orders.create_order(customer, items, req.promo_code)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["errors"])
    return result


@app.get("/orders")
def my_orders(customer=Depends(get_current_customer)):
    return orders.list_orders(customer["id"])


@app.get("/orders/{order_id}")
def get_order(order_id: int, customer=Depends(get_current_customer)):
    order = orders.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/orders/{order_id}/invoice")
def create_invoice(order_id: int, customer=Depends(get_current_customer)):
    inv = invoices.generate_invoice(order_id)
    if inv is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return inv


@app.get("/invoices/{filename:path}", response_class=PlainTextResponse)
def download_invoice(filename: str):
    content = invoices.read_invoice(filename)
    if content is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return content


@app.post("/cart/restore")
def restore_cart(req: CartRestoreRequest, customer=Depends(get_current_customer)):
    items = load_saved_cart(req.cart)
    return {"items": items}


@app.get("/admin/customers")
def admin_customers(_=Depends(require_admin)):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()
    return [dict(r) for r in rows]
