import requests
from api_keys import realtime_apikey, forecast_apikey
import pprint
import urllib.request
from PIL import Image

pp = pprint.PrettyPrinter(compact=True)


def realtime_api_call() -> dict:
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q":"97201"}

    headers = {
        "X-RapidAPI-Key": realtime_apikey,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    response = dict(response.json())

    return response


def forecast_api_call():
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring = {"q":"97201","days":"1"}

    headers = {
        "X-RapidAPI-Key": forecast_apikey,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    response = dict(response.json())

    return response

realtime_response = realtime_api_call()
forecast_response = forecast_api_call()

# WHY ARE THERE SO MANY NESTED DICTS 
for key,value in forecast_response.items():
    if key == 'forecast':
        for key,day in value.items():
            print(day[0].keys())
            for inner_key,info in day[0].items():
                if inner_key == 'day':
                    urllib.request.urlretrieve(('http:'+info['condition']['icon']),'weathericon.png')
                    img = Image.open('weathericon.png')
                    img.show()
