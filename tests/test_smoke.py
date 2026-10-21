def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_lists_active_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    skus = {p["sku"] for p in response.json()}
    assert "WID-001" in skus
    assert "OLD-008" not in skus
