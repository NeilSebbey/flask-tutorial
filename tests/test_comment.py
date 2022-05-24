import pytest
from flaskr.db import get_db




@pytest.mark.parametrize('path', (
        '/1/createComment',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
        '/2/createComment',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_createComment(client, auth, app):
    auth.login()
    assert client.get('/1/createComment').status_code == 200
    client.post('/1/createComment', data={'comment': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM comment').fetchone()[0]
        assert count == 0


