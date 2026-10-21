import base64
import pickle

from fastapi import Header, HTTPException

from app import config
from app.db import get_conn


def get_current_customer(x_api_token: str = Header(None)):
    if not x_api_token:
        raise HTTPException(status_code=401, detail="Missing X-API-Token header")
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM customers WHERE api_token = ?", (x_api_token,)
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return dict(row)


def require_admin(x_admin_key: str = Header(None)):
    if x_admin_key != config.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Admin only")
    return True


def load_saved_cart(blob):
    """Restores a cart that the frontend saved earlier (base64 encoded)."""
    if not blob:
        return []
    return pickle.loads(base64.b64decode(blob))
