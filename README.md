# Orderly API

> **Workshop participants:** Start at [Start here](exercises/00-start-here.md).
> Treat everything below this box as the project's own README. It's part of the
> codebase you're about to explore, and you shouldn't trust all of it.

Orderly is the order and invoicing service behind our storefront. It prices
orders, applies promo codes, stores orders, and generates invoices.

## Tech stack

- Python and FastAPI
- SQLite

## Getting started

1. Install Python 3.10 or later.
2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Load the demo data. This creates `orderly.db` in the current directory:

   ```sh
   python -m app.seed
   ```

   To use a different database file, set `ORDERLY_DB_PATH` before you seed and
   run the app.

4. Start the server from the repository root:

   ```sh
   uvicorn app.main:app --reload
   ```

5. Open http://localhost:8000/docs and try an endpoint. Authenticate with an
   `X-API-Token` header that uses one of the demo tokens in `app/seed.py`, for
   example `tok_ada_123`.

## Running tests

```sh
pytest
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| GET | `/products` | List or search products (`?q=`) |
| GET | `/products/{id}` | Get one product |
| POST | `/quote` | Price an order without placing it |
| POST | `/orders` | Place an order |
| GET | `/orders` | List your orders |
| GET | `/orders/{id}` | Get an order |
| POST | `/orders/{id}/invoice` | Generate an invoice |
| GET | `/invoices/{filename}` | Download an invoice |
| POST | `/cart/restore` | Restore a saved cart |
| GET | `/admin/customers` | List customers (admin only) |

Pricing rules live in [Orderly pricing rules](docs/PRICING_RULES.md).
