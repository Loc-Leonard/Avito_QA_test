import time
import requests
from .helper import create_item
from .conftest import generate_seller_id

def test_tcnf01_no5xx_on_valid_requests(base_url): # проверка на отсутствие 5xx при валидных запросах

    seller_id = generate_seller_id()

    payload = {
        "sellerID": seller_id,
        "name": "NF item",
        "price": 1000,
        "statistics": {"likes":1, "viewCount": 1, "contacts": 1},
    }
    r1 = requests.post(f"{base_url}/api/1/item", json=payload)
    assert 200 <= r1.status_code < 500
    item_id = r1.json()["status"].split(" - ")[1]

    r2 = requests.get(f"{base_url}/api/1/item/{item_id}")
    assert 200 <= r2.status_code < 500

    r3 = requests.get(f"{base_url}/api/1/statistic/{item_id}")
    assert 200 <= r3.status_code < 500

    r4 = requests.get(f"{base_url}/api/1/{seller_id}/item")
    assert 200 <= r4.status_code < 500
    
    r5 = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert 200 <= r5.status_code < 500

def test_tcnf02_response_time(base_url): # Время отета от API
    item_id, _ = create_item(base_url)

    times = []
    for _ in range(10):
        start = time.time()
        resp = requests.get(f"{base_url}/api/1/item/{item_id}")
        elapsed_ms = (time.time() - start) * 1000
        times.append(elapsed_ms)
        assert resp.status_code == 200
    avg = sum(times) / len(times)
    assert avg <= 500, f"Average response time {avg:.1f} ms exceeds 500 ms"