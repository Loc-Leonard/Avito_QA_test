import requests
from .helper import create_item
from .conftest import generate_seller_id

def test_tc10_items_by_existing_seller(base_url):
    seller_id = generate_seller_id()

    created_ids = []
    for name in ["Test item from py", "phone", "cat"]:
        item_id, _ = create_item(base_url, seller_id=seller_id, name=name)
        created_ids.append(item_id)

    resp = requests.get(f"{base_url}/api/1/{seller_id}/item")
    data = resp.json()

    assert resp.status_code == 200
    assert isinstance(data, list)
    returned_id = {item["id"] for item in data}

    for item_id in created_ids:
        assert item_id in returned_id

    for item in data:
        assert {"id", "name", "price", "sellerId", "statistics"} <= set(item.keys())
        assert {"contacts", "likes", "viewCount"} <= set(item["statistics"].keys())

def test_tc11_get_items_with_invalid_seller_id(base_url): # некорректный идентификатор продавца
    resp = requests.get(f"{base_url}/api/1/sellerID_string/item")
    data = resp.json()

    assert resp.status_code == 400
    assert data["status"] == "400"
    assert data["result"]["message"] == "передан некорректный идентификатор продавца"

def test_tc12_get_items_for_seeler_without_items(base_url): # получение объявлений по sellerid без объявлений
    seller_id = generate_seller_id()

    resp = requests.get(f"{base_url}/api/1/{seller_id}/item")
    data = resp.json()

    assert resp.status_code == 200
    assert data == []

def test_tc13_get_item_by_existing_id(base_url): # получение объявления по существующему идентификатору
    item_id, seller_id = create_item(base_url, name="cat", price=12345)

    resp = requests.get(f"{base_url}/api/1/item/{item_id}")
    data = resp.json()

    assert resp.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    item = data[0]
    assert item["id"] == item_id
    assert item["sellerId"] == seller_id
    assert {"createdAt", "id", "name", "price", "sellerId", "statistics"} <= set(item.keys())
    assert {"contacts", "likes", "viewCount"} <= set(item["statistics"].keys())

def test_tc14_get_item_by_nonexistent_id(base_url): # получение объявления по несуществующему ID
    nonexistent = "bd6ac18a-af0a-442a-a3d4-158d7d5984a8"
    
    resp = requests.get(f"{base_url}/api/1/item/{nonexistent}")
    data = resp.json()

    assert resp.status_code == 404
    assert data["status"] == "404"
    assert data["result"]["message"] == f"item {nonexistent} not found"

def test_tc15_get_item_by_invalid_uuid(base_url): # получение объявления по некорректному идентификатору
    bad_id = "43145246453765876"

    resp = requests.get(f"{base_url}/api/1//item/{bad_id}")
    data = resp.json()

    assert resp.status_code == 400
    assert data["status"] == "400"
    assert data ["result"]["message"] == f"ID айтема не UUID: {bad_id}" 

def test_tc16_get_request_idempotency(base_url): # проверка идемпотентности 
    item_id, seller_id = create_item(base_url, name="cat", price=12345)

    # GET /api/1/item/:id
    r1 = requests.get(f"{base_url}/api/1/item/{item_id}")
    r2 = requests.get(f"{base_url}/api/1/item/{item_id}")
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json() == r2.json()

    # GET /api/1/statistic/:id
    s1 = requests.get(f"{base_url}/api/1/statistic/{item_id}")
    s2 = requests.get(f"{base_url}/api/1/statistic/{item_id}")
    assert s1.status_code == 200
    assert s2.status_code == 200
    assert s1.json() == s2.json()

    # GET /api/1/:sellerID/item
    l1 = requests.get(f"{base_url}/api/1/{seller_id}/item")
    l2 = requests.get(f"{base_url}/api/1/{seller_id}/item")
    assert l1.status_code == 200
    assert l2.status_code == 200
    assert l1.json() == l2.json()

