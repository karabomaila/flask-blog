import pytest
from flask import g, session
from blog.db import get_db


def test_index(client ,auth):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2024-02-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/update/1"' in response.data

@pytest.mark.parametrize('path', (
    ('/create'),
    ('/update/1'),
    ('/delete/1'),
))
def test_login_required(client, path):
    response = client.post(path)

    assert response.headers['Location'] == '/auth/login'

def test_author_required(client, auth, app):
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()
    
    auth.login()
    assert client.post('/update/1').status_code == 403
    assert client.post('/delete/1').status_code == 403

    assert b'href="/update/1"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    ('/update/2'),
    ('/delete/2'),
))
def test_exits(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 403

def test_create(app, client, auth):
    auth.login()
    assert client.get('/create').status_code == 200

    client.post('/create', data={'title': 'created', 'body': 'Testing blog'})

    with app.app_context():
        count = get_db().execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2
    
def test_update(app, client, auth):
    auth.login()
    assert client.get('/update/1').status_code == 200

    client.post('/update/1', data={'title': 'Updated', 'body': 'blog updated'})
    with app.app_context():
        post = get_db().execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'Updated'

@pytest.mark.parametrize('path', (
        ('/create'),
        ('/update/1'),
))
def test_create_update_validate(auth, client, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})

    assert b'Please add the blog title!' in response.data

def test_delete(client, auth, app):
    auth.login()

    response = client.post('/delete/1')
    assert response.headers['Location'] == '/'

    with app.app_context():
        post = get_db().execute('SELECT * FROM post WHERE id = 1').fetchone()

        assert post is None

