from django.shortcuts import render
from .models import Station, Address
from datetime import datetime
import requests


def date_converter(data):
    date = data.split(".")[0].replace("T", " ")
    new_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return new_date

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_adress_data(item):
    data = Address.objects.filter(id=item["uid"]).last()
    if not data:
        timestamp = item["last_updated"]
        date = datetime.fromtimestamp(timestamp)
        instance = Address.objects.create(
            id=item["uid"],
            slots=item["slots"],
            address=item["address"].title(),
            payment=item["payment"],
            has_ebikes=item["has_ebikes"],
            payment_terminal=item["payment-terminal"],
            last_updated=date
        )
        instance.save()
        return instance
    return data

def get_stations_data(request, params={}):
    url = 'http://api.citybik.es/v2/networks/bikesantiago'
    response = generate_request(url, params)
    if response:
        stations = response.get('network').get('stations')
        stations_instance = []
        item_id = [x.id for x in Station.objects.all()]
        for item in stations:
            extra = item.get('extra')
            extra_field = get_adress_data(extra)
            if item["id"] not in item_id:
                timestamp = date_converter(item["timestamp"])
                instance = Station.objects.create(
                    id=item["id"],
                    name=item["name"],
                    free_bikes=item["free_bikes"],
                    empty_slots=item["empty_slots"],
                    timestamp=timestamp,
                    latitude=item["latitude"],
                    longitude=item["longitude"],
                    extra=extra_field
                )
                instance.save()
                stations_instance.append(instance)
            else:
                instance = Station.objects.filter(id=item["id"]).last()
                stations_instance.append(instance)
        context = dict(
            stations=stations_instance
        )
        return render(request, 'BikeSantiago/index.html', context=context)

    return ''