import requests

from fastapi.testclient import TestClient

from app.shop_app import app

client = TestClient(app)


def test_get_hello_world(wm_java, wm_url):
    response = requests.get(wm_url + "/hello")

    assert response.status_code == 200
    assert response.content == b"hello"


def test_get_overview_default(wm_java, wm_url):
    resp = client.get("/shop")

    assert resp.status_code == 200

    json_result = resp.json()

    assert "products" in json_result

    assert all("Mock" in product["name"] for product in json_result["products"])
