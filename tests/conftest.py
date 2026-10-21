import pytest
from fastapi.testclient import TestClient

from app import config, db, seed


@pytest.fixture
def seeded_db(tmp_path, monkeypatch):
    """A fresh SQLite database loaded with the demo data from app/seed.py."""
    monkeypatch.setattr(config, "DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setattr(config, "INVOICE_DIR", str(tmp_path / "invoices"))
    db.init_db()
    seed.seed()
    return config.DB_PATH


@pytest.fixture
def client(seeded_db):
    from app.main import app

    return TestClient(app)
