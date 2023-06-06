import pytest
from requests_mock.mocker import Mocker

# pylint: disable=wrong-import-order
from test.helpers.conftest import (
    VATSIM_STATUS,
    VATSIM_DATA
)
from util.vatsim import data


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
        assert e_info.value == 'Corresponding URL for invalid_key not found in VATSIM server status'


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
