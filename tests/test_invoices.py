def test_invoice_matches_amounts_charged(client):
    grace = {"X-API-Token": "tok_grace_456"}
    order = client.post("/orders", headers=grace, json={"items": [{"product_id": 5, "quantity": 1}]}).json()

    invoice = client.post(f"/orders/{order['order_id']}/invoice", headers=grace).json()

    assert invoice["tax"] == order["tax"]
    assert invoice["total"] == order["total"]
