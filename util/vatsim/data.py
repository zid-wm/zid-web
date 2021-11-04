import requests


def get_data_url(call='v3'):
    status = requests.get("https://status.vatsim.net/status.json").json()

    if call not in status and call not in status['data']:
        raise IndexError(f'Corresponding URL for {call} not found in VATSIM server status')

    try:
        return status[call][0]
    except KeyError:
        return status['data'][call][0]


def get_vatsim_data():
    return requests.get(get_data_url()).json()


def vatsim_controllers():
    return get_vatsim_data()['controllers']


def vatsim_ratings():
    return get_vatsim_data()['ratings']


def vatsim_facilities():
    return get_vatsim_data()['facilities']
