from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

TEST_NAME = 'USER_TESTNAME'
TEST_EMAIL = 'USER_TESTEMAIL'
TEST_PASSWORD = 'USER_TESTPASSWORD'


def test_create_item():
    response = client.post(
        "/user",
        headers={"X-Token": "coneofsilence"},
        json={"username": TEST_NAME, "email": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    json = response.json()
    for key, value in json.items():
        assert key in ['username', 'email', 'id', 'projects']


def test_create_token():
    response = client.post(
                            "/main/token/",
                            data={"username": "string", "title": "string"}
                            )
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2Njg4OTk2MzB9.U5NRU4e4LP19VoJyn1VBIwnp8_LTiv-819r0x8ymuuA",
        "token_type": "bearer"
        }


def test_read_item():
    response = client.get("/user", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }

