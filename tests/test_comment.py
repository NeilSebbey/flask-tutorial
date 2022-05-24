from flaskr.db import get_db
from flaskr.blog import get_all_comments


def test_login_required(client):
    response = client.post('/1/createComment')
    assert response.headers["Location"] == "/auth/login"


def test_exists_required(client, auth):
    auth.login()
    assert client.post('/2/createComment').status_code == 404


def test_create_comment_without_text(client, auth, app):
    auth.login()
    assert client.get('/1/createComment').status_code == 200
    client.post('/1/createComment', data={'comment': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM comment').fetchone()[0]
        assert count == 2


def test_create_comment(client, auth, app):
    auth.login()
    assert client.get('/1/createComment').status_code == 200
    client.post('/1/createComment', data={'comment': 'Test comment.'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM comment').fetchone()[0]
        assert count == 3


def test_get_all_comments(client, app):
    with app.app_context():
        result = get_all_comments(1)
        assert result is not None
        assert len(result)==2
        assert result[0][1] == 'test comment 2'
        assert result[1][1] == 'test comment 1'


