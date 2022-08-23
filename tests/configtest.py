import pytest
from app.oauth2 import create_access_token
from app import models
from .database import client, session
@pytest.fixture
def test_user(client):
    user_data = {"email": "shivamsharma02@gmail.com",
                 "password": "king02"}
    res = client.post("/users/create", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password'] # here we adding password beacuse in response we not get passprd field.
    # new_user={'id': 1, 'email': 'shivamsharma02@gmail.com', 'created_at': '2022-08-22T22:30:32.771646+05:30', 'phone_number': None, 'password': 'king02'}
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "shivamsharma03@gmail.com",
                 "password": "king02"}
    res = client.post("/users/create", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):  #test_user with id one
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"  #this is same as we setting bearer token in postman
    }
    return client #authorized client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id'] #id=1
    }, {
        "title": "1st title",
        "content": "1st content",
        "owner_id": test_user2['id']  #id =2
    }]

    def create_post_model(post):
    #   post=  {                          first time this function called three time {len(posts_data)}
    #     "title": "first title",
    #     "content": "first content",
    #     "owner_id": test_user['id']
    # }
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)   #map(function, one list), map iterate all element of list.
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
