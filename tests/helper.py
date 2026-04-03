import requests
from .conftest import generate_seller_id  # или from .conftest import ...


def create_item(base_url, seller_id=None, name="Test item", price=1234,
                likes=1, view_count=1, contacts=1):
    if seller_id is None:
        seller_id = generate_seller_id()
    payload = {
        "sellerID": seller_id,
        "name": name,
        "price": price,
        "statistics": {
            "likes": likes,
            "viewCount": view_count,
            "contacts": contacts,
        },
    }
    resp = requests.post(f"{base_url}/api/1/item", json=payload)
    resp.raise_for_status()
    status = resp.json()["status"]
    item_id = status.split(" - ")[1]
    return item_id, seller_id