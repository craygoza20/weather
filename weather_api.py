import requests
from api_keys import xrapid_api_key
import pprint
import urllib.request
from PIL import Image

pp = pprint.PrettyPrinter(compact=True, sort_dicts=False)


def aqi_api_call(lat, lon):
    url = "https://air-quality-by-api-ninjas.p.rapidapi.com/v1/airquality"

    querystring = {"lat":lat,"lon":lon}

    headers = {
        "X-RapidAPI-Key": xrapid_api_key,
        "X-RapidAPI-Host": "air-quality-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = dict(response.json())

    return response['overall_aqi']


def forecast_api_call(query='Portland, OR') -> dict:
    """Makes a call to the forecast weather api for my location for 3 days of weather.
    Returns a dict containing location info, current day weather, forecast weather for next 2 days"""

    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring = {"q":str(query),"days":"3"}

    headers = {
        "X-RapidAPI-Key": xrapid_api_key,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    response = dict(response.json())

    # top-level dict contains location, current, forecast
    # what values do I want?
    # from location I want the name, region, and local time
    loc_name = response['location']['name']
    loc_region = response['location']['region']
    loc_time = response['location']['localtime']
    loc_lon = response['location']['lon']
    loc_lat = response['location']['lat']
    #print(loc_name,loc_region,loc_time)

    # from current weather I want temp_f, is_day, condition dict, humidity
    current_temp_f = response['current']['temp_f']
    current_is_day = response['current']['is_day']
    current_condition_dict = response['current']['condition']
    current_humidity = response['current']['humidity']
    #print(current_temp_f,current_is_day,current_condition_dict,current_humidity)

    # forecast is split into 3 days due to API subscription limit
    # day 0 is current day, so we can skip that and use 1 and 2
    # from forecastday I want date, maxtemp_f, mintemp_f, avgtemp_f, condition dict, avghumidity 
    # pp.pprint(response['forecast']['forecastday'][0]['date']) that's deep
    day_1_maxtemp_f = response['forecast']['forecastday'][1]['day']['maxtemp_f']
    day_1_mintemp_f = response['forecast']['forecastday'][1]['day']['mintemp_f']
    day_1_avgtemp_f = response['forecast']['forecastday'][1]['day']['avgtemp_f']
    day_1_condition_dict = response['forecast']['forecastday'][1]['day']['condition']
    day_1_avghumidity = response['forecast']['forecastday'][1]['day']['avghumidity']
    day_1_date = response['forecast']['forecastday'][1]['date']
    #print(day_1_maxtemp_f,day_1_mintemp_f,day_1_avgtemp_f,day_1_condition_dict,day_1_avghumidity)

    day_2_maxtemp_f = response['forecast']['forecastday'][2]['day']['maxtemp_f']
    day_2_mintemp_f = response['forecast']['forecastday'][2]['day']['mintemp_f']
    day_2_avgtemp_f = response['forecast']['forecastday'][2]['day']['avgtemp_f']
    day_2_condition_dict = response['forecast']['forecastday'][2]['day']['condition']
    day_2_avghumidity = response['forecast']['forecastday'][2]['day']['avghumidity']
    day_2_date = response['forecast']['forecastday'][2]['date']
    #print(day_2_maxtemp_f, day_2_mintemp_f, day_2_avgtemp_f,day_2_condition_dict,day_2_avghumidity)

    # finally, dicts I can see in my bird brain
    location_dict = {'loc_name':loc_name,
                     'loc_region':loc_region,
                     'loc_time':loc_time,
                     'lon':loc_lon,
                     'lat':loc_lat
                     }
    
    current_dict =  {'current_temp_f':current_temp_f,
                     'current_is_day':current_is_day,
                     'current_condition_dict':current_condition_dict,
                     'current_humidity':current_humidity}
    
    day_1_dict = {'day_1_maxtemp_f':day_1_maxtemp_f,
                  'day_1_mintemp_f':day_1_mintemp_f,
                  'day_1_avgtemp_f':day_1_avgtemp_f,
                  'day_1_condition_dict':day_1_condition_dict,
                  'day_1_avghumidity':day_1_avghumidity,
                  'day_1_date':day_1_date}
    
    day_2_dict = {'day_2_maxtemp_f':day_2_maxtemp_f,
                  'day_2_mintemp_f':day_2_mintemp_f,
                  'day_2_avgtemp_f':day_2_avgtemp_f,
                  'day_2_condition_dict':day_2_condition_dict,
                  'day_2_avghumidity':day_2_avghumidity,
                  'day_2_date':day_2_date}
    
    # one dict to rule them all
    formatted_response = {'location_dict':location_dict,
                          'current_dict':current_dict,
                          'day_1_dict':day_1_dict,
                          'day_2_dict':day_2_dict}

    return formatted_response

def get_condition_image(response_dict:dict) -> list:
    """Takes in formatted api response dict, gets the images from the inner condition dicts, outputs relative image paths"""
    
    # select inner conditions dict for each day
    current_condition_dict = response_dict['current_dict']['current_condition_dict']
    day_1_condition_dict = response_dict['day_1_dict']['day_1_condition_dict']
    day_2_condition_dict = response_dict['day_2_dict']['day_2_condition_dict']

    # grab image urls
    current_image = 'http:' + current_condition_dict['icon']
    day1_image = 'http:' + day_1_condition_dict['icon']
    day2_image = 'http:' + day_2_condition_dict['icon']

    # download the images
    urllib.request.urlretrieve(current_image,'currenticon.png')
    urllib.request.urlretrieve(day1_image,'day1icon.png')
    urllib.request.urlretrieve(day2_image,'day2icon.png')

    current_image_path = 'currenticon.png'
    day1_image_path = 'day1icon.png'
    day2_image_path = 'day2icon.png'

    return [current_image_path, day1_image_path, day2_image_path]




# silly me did not know I would become this evil
# WHY ARE THERE SO MANY NESTED DICTS 
# for key,value in forecast_response.items():
#     if key == 'forecast':
#         for key,day in value.items():
#             print(day[0].keys())
#             for inner_key,info in day[0].items():
#                 if inner_key == 'day':
#                     urllib.request.urlretrieve(('http:'+info['condition']['icon']),'weathericon.png')
#                     img = Image.open('weathericon.png')
#                     #img.show()

# image_paths = get_condition_image(forecast_response)
# pp.pprint(image_paths)
if __name__ == "__main__":
    forecast_response = forecast_api_call()
    #print(forecast_response)
    aqi = aqi_api_call(forecast_response['location_dict']['lat'], forecast_response['location_dict']['lon'])
    print(aqi)

    for image in get_condition_image(forecast_response):
        with Image.open(image) as im:
            print(im.getbands())  # Returns ('R', 'G', 'B'