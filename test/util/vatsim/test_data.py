import pytest
from requests_mock.mocker import Mocker

from test.conftest import (
    VATSIM_STATUS,
    VATSIM_DATA
)
from util.vatsim import data


def mock_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://status.vatsim.net/status.json':
        return MockResponse(VATSIM_STATUS, 200)

    return MockResponse(None, 404)


@pytest.mark.parametrize(
    'call,expected',
    [
        ('v3', 'https://data.vatsim.net/v3/vatsim-data.json'),
        ('servers', 'https://data.vatsim.net/v3/vatsim-servers.json'),
        ('user', 'https://stats.vatsim.net/search_id.php'),
        ('metar', 'http://metar.vatsim.net/metar.php')
    ]
)
def test_get_data_url(call, expected, requests_mock: Mocker):
    requests_mock.get('https://status.vatsim.net/status.json', json=VATSIM_STATUS)
    assert data.get_data_url(call) == expected


def test_get_data_url_default(requests_mock: Mocker):
    requests_mock.get('https://status.vatsim.net/status.json', json=VATSIM_STATUS)
    assert data.get_data_url() == 'https://data.vatsim.net/v3/vatsim-data.json'


def test_get_data_url_error(requests_mock: Mocker):
    requests_mock.get('https://status.vatsim.net/status.json', json=VATSIM_STATUS)
    with pytest.raises(IndexError) as e_info:
        data.get_data_url('invalid_key')


def test_get_vatsim_data(requests_mock: Mocker):
    requests_mock.get('https://status.vatsim.net/status.json', json=VATSIM_STATUS)
    requests_mock.get('https://data.vatsim.net/v3/vatsim-data.json', json=VATSIM_DATA)
    assert data.get_vatsim_data()['general']['update'] == '20230511015914'


def test_vatsim_controllers(requests_mock: Mocker):
    requests_mock.get('https://status.vatsim.net/status.json', json=VATSIM_STATUS)
    requests_mock.get('https://data.vatsim.net/v3/vatsim-data.json', json=VATSIM_DATA)
    assert len(data.vatsim_controllers()) == 3


def test_vatsim_ratings(requests_mock: Mocker):
    requests_mock.get('https://status.vatsim.net/status.json', json=VATSIM_STATUS)
    requests_mock.get('https://data.vatsim.net/v3/vatsim-data.json', json=VATSIM_DATA)
    assert len(data.vatsim_ratings()) == 14


def test_vatsim_facilities(requests_mock: Mocker):
    requests_mock.get('https://status.vatsim.net/status.json', json=VATSIM_STATUS)
    requests_mock.get('https://data.vatsim.net/v3/vatsim-data.json', json=VATSIM_DATA)
    assert len(data.vatsim_facilities()) == 7
