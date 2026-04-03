import os
import random
import pytest

BASE_URL = os.getenv("API_BASE_URL", "https://qa-internship.avito.com")
@pytest.fixture(scope="session")
def base_url():
    return BASE_URL.rstrip("/")

def generate_seller_id():
    return random.randint(111111, 999999)