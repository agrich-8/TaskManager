from fastapi.testclient import TestClient



client = TestClient(app)

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


