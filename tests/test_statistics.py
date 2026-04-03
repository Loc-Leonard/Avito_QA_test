import requests
from .helper import create_item


def test_tc07_get_statistics_existing_id(base_url):
    """TC-07 - Получение статистики объявления по существующему ID."""
    item_id, _ = create_item(
        base_url,
        likes=56,
        view_count=1234,
        contacts=45,
    )

    resp = requests.get(f"{base_url}/api/1/statistic/{item_id}")
    data = resp.json()

    assert resp.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    stat = data[0]
    assert stat["contacts"] == 45
    assert stat["likes"] == 56
    assert stat["viewCount"] == 1234


def test_tc08_get_statistics_invalid_id(base_url):
    """TC-08 - Получение статистики по некорректному ID."""
    bad_id = "1231435345465746"

    resp = requests.get(f"{base_url}/api/1/statistic/{bad_id}")
    data = resp.json()

    assert resp.status_code == 400
    assert data["status"] == "400"
    assert data["result"]["message"] == "передан некорректный идентификатор объявления"


def test_tc09_get_statistic_non_existent_id(base_url):
    """TC-09 - Получение статистики по несуществующему ID."""
    # Берём валидный по формату UUID, которого нет в системе.
    nonexist_id = "bd074e51-874e-48ff-876c-955376b26e60"

    resp = requests.get(f"{base_url}/api/1/statistic/{nonexist_id}")
    data = resp.json()

    assert resp.status_code == 404
    assert data["status"] == "404"
    assert data["result"]["message"] == f"statistic {nonexist_id} not found"