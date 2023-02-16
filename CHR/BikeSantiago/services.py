import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_stations_data(params={}):
    url = 'http://api.citybik.es/v2/networks/bikesantiago'
    response = generate_request(url, params)
    if response:
       stations = response.get('network').get('stations')
       return stations

    return ''