import os

# TODO: move these to env vars before go-live
SECRET_KEY = "orderly-dev-secret-9f8e7d6c5b4a"
ADMIN_API_KEY = "sk_live_ORDERLY_4f2a9c1e7b3d55a0"

DB_PATH = os.environ.get("ORDERLY_DB_PATH", "orderly.db")
INVOICE_DIR = os.environ.get("ORDERLY_INVOICE_DIR", "invoices")

# State sales tax rates. Keep in sync with docs/PRICING_RULES.md
TAX_RATES = {
    "CA": 0.0725,
    "NY": 0.04,
    "TX": 0.0625,
    "WA": 0.065,
}
DEFAULT_TAX_RATE = 0.05

FLAT_SHIPPING = 7.99
