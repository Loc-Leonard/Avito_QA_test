import requests

from .conftest import generate_seller_id

def test_tc01_create_item_success(base_url): # Успешное создание объявления
    payload = {
        "sellerID": generate_seller_id(),
        "name": "Test item from pytest",
        "price": 1500,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1,
        },
    }

    resp = requests.post(f"{base_url}/api/1/item", json=payload)
    data = resp.json()

    assert resp.status_code == 200
    assert "status" in data
    assert data["status"].startswith("Сохранили объявление - ")

def test_tc02_create_item_without_likes(base_url): # Создание объявления без statistics.likes
    payload = {
        "sellerID": generate_seller_id(),
        "name": "Test item from Postman",
        "price": 1500,
        "statistics": {
            "viewCount": 1,
            "contacts": 1
        },
    }

    resp = requests.post(f"{base_url}/api/1/item", json=payload)
    data = resp.json()

    assert resp.status_code == 400
    assert data["status"] == "400"
    assert data["result"]["message"] == "поле likes обязательно"

def test_tc03_create_item_without_name(base_url): # Создание объявления без поля name
    payload = {
        "sellerID": generate_seller_id(),
        "name": "",
        "price": 123,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        },
    }

    resp = requests.post(f"{base_url}/api/1/item", json=payload)
    data = resp.json()

    assert resp.status_code == 400
    assert data["status"] == "400"
    assert data["result"]["message"] == "поле name обязательно"

def test_tc04_create_item_with_negative_price(base_url): # Ссздание объявления с отрицательной ценой
    payload = {
        "sellerID": generate_seller_id(),
        "name": "Test item from Postman",
        "price": -1,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        },
    }

    resp = requests.post(f"{base_url}/api/1/item", json=payload)

    assert resp.status_code == 400, (
        "Ожидали 400 Bad Request при отрицательной цене, но получили {code} см. BUG-01 в BUGS.md".format(code=resp.status_code)
    )

def test_tc05_create_item_with_zero_price(base_url): # Создание объявления с нулевой ценой
    payload = {
        "sellerID": generate_seller_id(),
        "name": "phone",
        "price": 0,
        "statistics": {
            "likes": 1,
            "viewCount": 2,
            "contacts": 3
        },
    }

    resp = requests.post(f"{base_url}/api/1/item", json=payload)
    data = resp.json()

    assert resp.status_code == 400
    assert data ["result"]["message"] == "поле price обязательно"

def test_tc06_create_item_with_string_sellerid(base_url): # Создание объявления со строкой в sellerID
    payload = {
        "sellerID": "selledId in string",
        "name": "Test item from Postman",
        "price": 1234,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        },
    }

    resp = requests.post(f"{base_url}/api/1/item", json=payload)
    data = resp.json()

    assert resp.status_code == 400
    assert data ["status"] == "не передано тело объявления" # Данный баг описан в BUGS.md BUG-02. Сообщение неиформативно

