from jose import jwt
from app import schemas
from .configtest import client,session,test_user
from  app.config import settings
import pytest
# misc
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/create", json={"email": "hello12345677@gmail.com", "password": "password123","phone_number":"8210206878"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello12345677@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])               
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 202


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'king02', 401),
    ('shivamsharma02@gmail.com', 'wrongpassword', 401),
    ('wrongemail@gmail.com', 'wrongpassword', 401),
    (None, 'king02', 422),
    ('shivamsharma02@gmail.com', None, 422),
    ("","",422),
    (None,None,422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials' #for 422 this is show failed beacuse field_Required