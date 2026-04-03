import requests
from .helper import create_item

def test_tc17_delete_item_success(base_url): # Удаление объявления по ID
    item_id, _ = create_item(base_url)

    resp = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert resp.status_code == 200

def test_tc18_delete_item_twice(base_url): # Повторное удаление объявления
    item_id, _ = create_item(base_url)

    first = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert first.status_code == 200

    second = requests.delete(f"{base_url}/api/2/item/{item_id}")
    data = second.json()

    assert second.status_code == 404
    assert data["status"] == "404", (
        f'Ожидали status "404" в теле ответа'
        f'но получили "{data["status"]}" см. BUG-03 в BUGS.md'
    )

def test_tc19_delete_item_invalid_id(base_url): # Удаление по некорректному ID
    bad_id = "435234654372352357658768967898"

    resp = requests.delete(f"{base_url}/api/2/item/{bad_id}")
    data = resp.json()

    assert resp.status_code == 400
    assert data["status"] == "400"
    assert data["result"]["message"] == "переданный id айтема некорректный"