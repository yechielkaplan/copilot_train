import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

@pytest.fixture
def client():
    # Preserve original in-memory activities between tests
    original = copy.deepcopy(activities)
    client = TestClient(app)
    try:
        yield client
    finally:
        activities.clear()
        activities.update(original)
