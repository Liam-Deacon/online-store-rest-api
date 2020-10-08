import pytest
import json


def test_list_get(client, test_auth_headers):
    response = client.get('/api/v1/gifts/list',
                          headers=test_auth_headers)
    assert response.status_code == 204
    try:
        data = json.loads(response.get_data().decode())
        assert data
        assert isinstance(data, list)
    except json.decoder.JSONDecodeError:
        pass


@pytest.mark.skip('TODO')
def test_list_gift_id_purchase_post(client, test_auth_headers):
    pass


@pytest.mark.skip('TODO')
def test_list_gift_id_delete(client, test_auth_headers):
    pass


@pytest.mark.skip('TODO')
def test_list_gift_id_get(client, test_auth_headers):
    pass


@pytest.mark.skip('TODO')
def test_list_add_post(client, test_auth_headers):
    pass


def test_list_report_get(client, test_auth_headers):
    response = client.get('/api/v1/gifts/list/report',
                          headers=test_auth_headers)
    assert response.status_code == 200
    data = json.loads(response.get_data().decode())
    assert data
    assert 'available' in data.keys()
    assert 'purchased' in data.keys()
    assert isinstance(data['available'], list)
    assert isinstance(data['purchased'], list)


@pytest.mark.parametrize(
    ('endpoint', 'method', 'data', 'has_auth', 'code'),
    [('/api/v1/gifts/list', 'GET', None, True, 204)]
)
def test_protected_endpoint(client, test_auth_headers,
                            endpoint, method, data, has_auth, code):
    request = getattr(client, method.lower())
    response = request(endpoint, headers=test_auth_headers if has_auth else {},
                       data=data, mimetype='application/json')
    assert response.status_code == code
