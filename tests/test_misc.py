from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200


def test_get_all_posts(client):
    res = client.get("/sqlalchemy")
    assert res.status_code == 200
    assert res.json()== {"Connection":"Success"}