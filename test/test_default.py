

def test_default_route(client):
    response = client.get('/')
    assert response.status_code == 200

    body = response.get_data()
    assert body
    assert b'routes' in body
    assert b'</table>' in body
