import os
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

test_database_url = os.getenv("TEST_DATABASE_URL")
if not test_database_url:
    pytest.skip("TEST_DATABASE_URL is required for MySQL integration tests", allow_module_level=True)

parsed_test_url = make_url(test_database_url)
if parsed_test_url.drivername != "mysql+pymysql" or not (parsed_test_url.database or "").endswith("_test"):
    raise RuntimeError("TEST_DATABASE_URL must use mysql+pymysql and a database name ending with '_test'")

os.environ["DATABASE_URL"] = test_database_url

from app.database import Base, engine, import_all_entities
from app.main import app

import_all_entities()

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_full_pilot_flow():
    profile_res = client.post(
        "/api/profiles",
        json={
            "parent_name": "Parent A",
            "parent_phone": "13800000000",
            "child_name": "Child A",
            "child_phone": "13900000000",
            "chronic_diseases": "hypertension",
            "allergies": "none",
            "mobility_limitations": "light",
            "interests": "culture,food",
            "wechat_webhook_url": "",
        },
    )
    assert profile_res.status_code == 200
    profile_id = profile_res.json()["id"]

    profile_list_res = client.get("/api/profiles?limit=10")
    assert profile_list_res.status_code == 200
    assert any(item["id"] == profile_id for item in profile_list_res.json())

    trip_res = client.post(
        "/api/trips",
        json={
            "profile_id": profile_id,
            "destination": "Hongya Cave",
            "travel_date": str(date.today()),
        },
    )
    assert trip_res.status_code == 200
    trip = trip_res.json()
    trip_id = trip["id"]
    assert trip["pass_token"].startswith("ELDER-")
    assert "<svg" in trip["pass_qr_svg"]

    sos_res = client.post(
        "/api/sos/trigger",
        json={
            "profile_id": profile_id,
            "trip_id": trip_id,
            "latitude": 29.56,
            "longitude": 106.55,
            "network_status": "online",
        },
    )
    assert sos_res.status_code == 200
    assert "sent" in sos_res.json()["sms_status"]

    task_res = client.post(
        "/api/tasks",
        json={
            "profile_id": profile_id,
            "trip_id": trip_id,
            "title": "Take skyline photo",
            "description": "Take one skyline photo and share.",
        },
    )
    assert task_res.status_code == 200
    task_id = task_res.json()["id"]

    complete_res = client.post(
        f"/api/tasks/{task_id}/complete",
        json={"completed_note": "Done", "photo_url": "https://example.com/a.jpg"},
    )
    assert complete_res.status_code == 200
    assert complete_res.json()["status"] == "completed"

    feedback_res = client.post(
        f"/api/tasks/{task_id}/feedback",
        json={"feedback_text": "Nice!", "hearts_delta": 1},
    )
    assert feedback_res.status_code == 200
    assert feedback_res.json()["hearts"] >= 1

    guide_res = client.post("/api/guide/ask", json={"question": "Tell me about Hongya Cave"})
    assert guide_res.status_code == 200
    assert guide_res.json()["scope"] == "knowledge_limited"

    card_res = client.post(
        "/api/cards/generate",
        json={"trip_id": trip_id, "title": "Pilot Card", "image_url": ""},
    )
    assert card_res.status_code == 200
    assert card_res.json()["trip_id"] == trip_id
