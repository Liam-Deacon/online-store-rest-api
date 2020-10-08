from http import HTTPStatus


def test_terms(client):
    response = client.get('/terms')
    assert response.status_code == HTTPStatus.OK
    assert 'Terms of Use' in response.get_data().decode()
