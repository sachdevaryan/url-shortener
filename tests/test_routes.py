def test_shorten_url(client):
    response = client.post("/shorten", json={"url": "https://google.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert len(data["short_code"]) <= 8

def test_redirect(client):
    res = client.post("/shorten", json={"url": "https://github.com"})
    code = res.json()["short_code"]
    res = client.get(f"/{code}", follow_redirects=False)
    assert res.status_code == 301
    assert res.headers["location"] == "https://github.com"

def test_stats(client):
    res = client.post("/shorten", json={"url": "https://openai.com"})
    code = res.json()["short_code"]
    stats = client.get(f"/stats/{code}")
    assert stats.status_code == 200
    data = stats.json()
    assert data["click_count"] == 0
    assert data["short_code"] == code
    assert "created_at" in data

def test_click_count_increments(client):
    res = client.post("/shorten", json={"url": "https://example.com"})
    code = res.json()["short_code"]
    client.get(f"/{code}", follow_redirects=False)
    client.get(f"/{code}", follow_redirects=False)
    stats = client.get(f"/stats/{code}")
    assert stats.json()["click_count"] == 2

def test_404_on_invalid_code(client):
    res = client.get("/nonexistent", follow_redirects=False)
    assert res.status_code == 404

def test_invalid_url_rejected(client):
    res = client.post("/shorten", json={"url": "not-a-url"})
    assert res.status_code == 422
