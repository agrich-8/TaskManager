import random
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

TEST_NAME = 'USER_TEST_NAME543v1111433'
TEST_EMAIL = 'usertestemail.ex111s4123@gmail.com'
TEST_PASSWORD = 'USER_TEST_PASSWORD'

token = ''
test_project_id = int()
test_task_id = int()



def test_create_user():

    response = client.post(
                        "/user",
                        json={"username": TEST_NAME, "email": TEST_EMAIL, "password": TEST_PASSWORD},
                        )
    assert response.status_code == 200
    json = response.json()
    for key, value in json.items():
        assert key in [
                        'username', 
                        'email', 
                        'id', 
                        'projects'
                        ]


def test_create_token():
    global token
    response = client.post(
                        "/auth/token",
                        data={"username": TEST_NAME, "password": TEST_PASSWORD}
                        )
    assert response.status_code == 200
    json =  response.json()
    for key, value in json.items():
        assert key in ['access_token', 'token_type']
    token = json['access_token']


def test_get_user():
    response = client.get(
                        "/user", 
                        headers={"Authorization": "Bearer "+token}
                        )
    assert response.status_code == 200
    json = response.json()
    for key, value in json.items():
        assert key in [
                        'username', 
                        'email', 
                        'id', 
                        'projects', 
                        'tasks'
                        ]


def test_create_project():
    global test_project_id
    response = client.post(
                        "/project",
                        headers={"Authorization": "Bearer "+token},
                        json={
                            "title": "string",
                            "color": "string"
                            }
                        )
    assert response.status_code == 200
    json = response.json()
    for key, value in json.items():
        assert key in [
                        'id', 
                        'title', 
                        'color', 
                        'is_base_project', 
                        'user_id', 
                        'tasks'
                        ]
    test_project_id = json['id']


def test_update_project():
    response = client.put(
                        "/project",
                        headers={"Authorization": "Bearer "+token},
                        json={
                            "id": test_project_id,
                            "title": "string_new",
                            "color": "string_new"
                            }
                        )
    assert response.status_code == 200
    json = response.json()
    for key, value in json.items():
        assert key in [
                        'id', 
                        'title', 
                        'color', 
                        'is_base_project', 
                        'user_id', 
                        'tasks'
                        ]


def test_create_task():
    global test_task_id
    response = client.post(
                        "/task",
                        headers={"Authorization": "Bearer "+token},
                        json={
                            "title": "string",
                            "description": "string",
                            "position": 0,
                            "priority": 0,
                            "section": "string",
                            "datetime_expiration": "2022-12-06T17:28:06.314Z",
                            "project_id": test_project_id
                            }
                        )
    assert response.status_code == 200
    json = response.json()
    for key, value in json.items():
        assert key in [
                        "title",
                        "description",
                        "position",
                        "priority",
                        "section",
                        "datetime_expiration",
                        "id",
                        "is_completed",
                        "datetime_completion",
                        "datetime_added",
                        "project_id"
                        ]
    test_task_id = json['id']


def test_update_task():
    response = client.put(
                        "/task",
                        headers={"Authorization": "Bearer "+token},
                        json={
                            "id": test_task_id,
                            "title": "string_new"
                            }
                        )
    assert response.status_code == 200
    json = response.json()
    for key, value in json.items():
        assert key in [
                        "title",
                        "description",
                        "position",
                        "priority",
                        "section",
                        "datetime_expiration",
                        "id",
                        "is_completed",
                        "datetime_completion",
                        "datetime_added",
                        "project_id"
                        ]



def test_update_user():
    response = client.put(
                        "/user",
                        headers={"Authorization": "Bearer " + token},
                        json={
                            "username": TEST_NAME + str(random.randint(1, 444)),
                            "email": str(random.randint(1, 444)) + TEST_EMAIL,
                            "password": TEST_PASSWORD + str(random.randint(1, 444))
                            }
                        )
    assert response.status_code == 200