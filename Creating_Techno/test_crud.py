from nikoss import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_insertion():
    song = {"id": 1, "name": "Too Far Gone", "artist": "Cane Hill", "bpm": 120}
    response = client.post("/songs/", json=song)
    assert response.status_code == 201


def test_getting():
    response = client.get("/songs/")
    assert response.status_code == 200


def test_changing():
    song = {"id": 1, "name": "Too Far Gin", "artist": "Timberlake", "bpm": 121}
    response = client.put("/songs/1", json=song)
    assert response.status_code == 200


def test_deleting():
    response = client.delete("/songs/1")
    assert response.status_code == 204


