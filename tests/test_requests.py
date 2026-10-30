import pytest


@pytest.mark.asyncio
async def test_create_and_get_request(client, monkeypatch):
    # Redis-ті mock-таймыз — тест нақты Redis-ке тәуелді болмауы керек
    async def fake_enqueue(_: str) -> None:
        return None

    monkeypatch.setattr("app.api.v1.requests.enqueue_request", fake_enqueue)

    resp = await client.post(
        "/api/v1/requests",
        json={"client_phone": "+77011234567", "text": "Бағаңыз қанша?"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "pending"

    resp = await client.get(f"/api/v1/requests/{body['id']}")
    assert resp.status_code == 200
    assert resp.json()["client_phone"] == "+77011234567"