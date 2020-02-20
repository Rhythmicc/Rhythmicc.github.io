#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
# -*- coding: utf-8 -*-

# <bitbar.title>Weather</bitbar.title>
# <bitbar.version>v3.5.0</bitbar.version>
# <bitbar.author>Daniel Seripap</bitbar.author>
# <bitbar.author.github>seripap</bitbar.author.github>
# <bitbar.desc>Detailed weather plugin powered by DarkSky with auto location lookup. Supports metric and imperial units. Needs API key from https://darksky.net/dev/.</bitbar.desc>
# <bitbar.image>https://cloud.githubusercontent.com/assets/683200/16276583/ff267f36-387c-11e6-9fd0-fc57b459e967.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>


# -----------------------------------------------------------------------------------
# For a more accurate location lookup, download and install CoreLocationCLI
# Available here: https://github.com/fulldecent/corelocationcli/releases
# This will allow a more percise location lookup as it uses native API for loc lookup
# -----------------------------------------------------------------------------------

import json
import requests
from requests import RequestException
import textwrap
from random import randint
import subprocess
from QuickStart_Rhy.Dict import Dict

# get yours at https://darksky.net/dev
api_key = '你的 API ID'

# get yours API key for encode location at https://opencagedata.com
geo_api_key = '你的 API ID'

# if you want to set manual location, define following two vars. If left empty, script will try to determine the location
# example:
location = {'loc':'39.9056,116.3913', 'region': 'Beijing', 'city': 'Beijing'} # Beijing


# set to si for metric, leave blank for imperial
units = 'si'

def auto_loc_lookup():
  try:
    location = requests.get('https://ipinfo.io/json').text
    return json.loads(location)
  except RequestException:
    return False

def reverse_latlong_lookup(loc):
  try:
    location_url = 'https://api.opencagedata.com/geocode/v1/json?q=' + loc + '&key=' + geo_api_key + '&language=en&pretty=1'
    location = json.loads(requests.get(location_url).text)
    if 'results' in location:
      return location['results'][0]['formatted']
    else:
      return 'Could not lookup location name'
  except:
    return 'Could not lookup location name'

def full_country_name(country):
  try:
    countries = json.loads(requests.get('http://country.io/names.json').text)
    try:
      if country in countries:
        return countries[country].encode('UTF-8')
      else:
        return False
    except KeyError:
      return False
  except RequestException:
    return False

def calculate_bearing(degree):
  cardinals = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
  return cardinals[int(round(((6 * degree)) / 360))]

def get_wx_icon(icon_code, ret_icon=True):
  if ret_icon:
    if icon_code == 'clear-day':
        icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAmVBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjHWqVAAAAMnRSTlMAAQIDBAUGCAoMFxgZHR4hIiU0NTc4QEFFRlhZZmeGh4qLra6xtL/AwdDR1tnb3Pf4+RkSsW4AAACvSURBVHgBJczZWqJgAADQw7+AouOMU2lGtrgYQhny/g/X9+XtuTgUhGDdZ0IC01JpO1YSCsnrJUabnWz+PiGohwM58m/4jEiW94uP4drWd8coIJuN56bpxoVQBrmiPUN3Av24i9cnVaUZ0uZ5bbXd5Gtzg7Afe3DqoGup8u+zuKW1jCAe/9ftMJz+PCwlxK/vv4TEYZgJTN7msv2jEC8vkgJJNW6V8hSkQO5XQqDwAzg9DY/cb+9eAAAAAElFTkSuQmCC'
    elif icon_code == 'clear-night':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAmVBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjHWqVAAAAMnRSTlMAAQIDBAUGBxMVFycoKSosMDE/QEpLTFhkZ2prdHZ6ipagoayusLS5u7zGyeXs8vn6+7VdeBQAAACGSURBVHjabU+HDoJQDLxKVRwo4saNgnv1/z/Oiy9PEkOTjrtuVEugqrUSiosDjwnHu3wdekZQP9m1eNjIMbT7d4d+Y32wmBrZEI0mZraCAtTFXUQxtRSCL5GSENy2DrOlawnQswGn+aGvCO1nzJxfe7bL0ebQ8rBJdli2IL/Txbm/5wTV8gEi7AeTMvh8mQAAAABJRU5ErkJggg=='
    elif icon_code == 'rain':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA5klEQVQoFQXBMSuFYRgA0PO870cGlMFgUEpEBiuKgUGMdhmU5AfIbvYHlNGghCIpLBaUWSmDQSbdgdW9j3MChDRkWbdH4+Z8OvGl6AAFu9Kvb+nPq5a0iQoNtqRtRZg3DPakRVSgZR8AVeDKMypMSdNohKqgC6vSLHDgS0UAoOLBPQVLLrR1SQAUXJikwY9BFI3URlEUTGgBG9IMoGoAC9I2BI6lS6fWwJhrL9IRggDrbr1JT26kD4dWQEAIwIpzZ3YARQDQaBQwAbpVoAI6OqDfuz53QhsoAAgM6DGCBAAAAqN6EQD/vPo8tMz6bZYAAAAASUVORK5CYII='
    elif icon_code == 'snow':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA40lEQVQoFQXBsSqFYRgA4Of9vv+4AHWUIhORwYqiMIjZKoMSNyC72Q0oo0EZTh1ZZFGSsigpE0omncKK1/MECGnQsj43xsx6c+Jd8QcU7ErfPqQfj3rSJio02JK2FWHOMNiTFlGBnn0AVIEzt6gwKU2hEaqCFlalGeDAu4oAQMWVSwqWdPxqSQAUdEzQ4EsbRSP9oigKxvWADWkaUDWAeWkbAsdS16k1MOrcnXSEIMC6C0/Sua704tAKCAgBeJau7QCKAKCFfvceAC0VAKBgxBAIAACggAVLCAAACAz49KqNAvwDhLU7zZRMOIUAAAAASUVORK5CYII='
    elif icon_code == 'sleet':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA6klEQVQoFQXBry+FYRgA0PO873cVqiCoxgQVG4FwN1E3wWaiZIImEzXJBGN2N6aYovjxBxjdJLuBZO7ncU6AkMZ0DXkwYd67Mx+KP6BgR/r2KQ286EsbqNBgU9pShAXjYFdaQgX69gFQBa49ocK0NINGqAo6WJHmgAMfKgIAFffuKFjW0+pIABT0TNHgyyiKRmpRFAWT+sC6NAuoGsCitAWBU+nKhVUw4dKzdIwgwJpbr9KjGymd6IIIBBKs2DDi3IxtrepPAjSqAHBoHAENYCB0tEL4NawFKCAwak+rNcCbHwAgMOYIBQDgH8ebRS21EV3JAAAAAElFTkSuQmCC'
    elif icon_code == 'wind':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAflBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCtoPsAAAAKXRSTlMAAQIDBAUOGx8kJjE7PkVHS05camtvdneHiY+su8DBw8rU1dzm8PH6/PnPEUAAAABvSURBVHgBlc3XDoJgDEDh0+HAvQc4FBHt+7+gI8T8XvJdnKRpk9KSKykB7G/uzjMSRj9ijTRrc2MftweYvxnAJKa9oNPcjw+zYSzOd+pTvtnmxzquI3bPy4BlUVZVWawyEJyEKvaJu4J+y++l0MYLmKUFUAQQSQkAAAAASUVORK5CYII='
    elif icon_code == 'fog':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA7UlEQVQoFQXBzyqEURwA0HPv/SazYGGh7NiwUzOlFHv5s1BWnmAW8wBW3gHlGSyUPIBkQcNkY+ElhEgyDb7v5xyAAiCBpAAJJGHJptqGZR+OHaGogYwD4dnIQN+J8KSLAgXrQg9tQMeDsIJChXN3SEhaWuDGACWDSa9oq2SNxhROLaKmQl+YAwBcG6KQwNCPLXvOdG3bdyWsokBG24Uw9iKEd/fWUAAymDWj6FiQQQEAAAAgkVDUDu36VIQsNCpvdrxKFQK3Rr5lAFljDAkwb1otAULlUSNrIONS+BNCCL9CDxUJMKGtkQAh+dLAP69nSf8xfn8mAAAAAElFTkSuQmCC'
    elif icon_code == 'cloudy':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA70lEQVQoFQXBLUuDURgA0HPvs1cFtVhFHAaTWMVgGgODySKCQQSTSZPFbrEMi8Hgb1gzCDOINruw5EdUGcJg23s9ByAECAFCAECAEGDaFAiAwKaebz/uPfoz0LOBIAsTR56MnDkVBo6dGHt2YCJgVXEOAOBC0QQ63hAqDSE0VDLeXQKfrlEBgAo3vmBXsYIMADIWFftZ26u+UAOAWvjwopWNVAhJApAkgRlDWop1QEiSAKwp2tBVbJs3C2DOgh1FF0juFGMjhzL2DNWKWwkSaGq7Uvz6VnRsWQIpIckmYFlL9qAPQq0kQJYxBgSKGv4BLfNBIGx3s8kAAAAASUVORK5CYII='
    elif icon_code == 'partly-cloudy-day':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAABCUlEQVQoFQXBLUjcYRwA4Od9714F56ZYLAbbmAjC4YIoWIzaLNo8kAmbzW5WYTCDa5v25YnBE0SYTTHIYTEsCSIs+MFO/z+fpwYggaKyb0RLUSFlQBI+mNDBG73oWPZeANTRFCYxZBCfhHEAsoJVDZvuPdjSMI0CFAAbwmcrwiZAlvDWjrYTYQGsuDfk2O+sEuZdW3LgBlu+K0LNs3NndPsjHOoHs376569HXwG+qQyDog6KO6dGfUHhxjq6JZD1YNuREaFJ3ZMBhJBkL/5jDJem3MGaMIMu0IVFYRqQYFf4iD4N9Huyh7qaDPBLaLkV2kLbOyQgySo0zblwbsqVHzqyCoAEACAD8Aph71BRnuBbowAAAABJRU5ErkJggg=='
    elif icon_code == 'partly-cloudy-night':
      icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA6UlEQVQoFQXBvyqFYRwA4Od93885AxLDySAMkpiUXAByA7LZbTJYnc4iF+HPxC1YLCYGYVJSslDUCYtTzvD9PE8CAJBl1GoAAKAAKEABAFlt0rY1XZ8SACRZE5tC17uwiwJkGTCkdggOhGUUCmiZsu9VWMW4N/cmkGHGnRB6Tl0IGzp+QYZhPx6t2NACbaHvBA1gT18CNCTsCJfIwJEHNBUJSYVjT0iQ3Zoz4g8JYQDPRhHAkjANGFAw6NsZKqD4cGXIrAXQFl6MIQMs+hJCOHcjdFTIQJLVmtb1zNvSdeAaWQ1AAQBUEgD/3uo/+JyzvikAAAAASUVORK5CYII='
    else:
      icon = ''
  else:
    if icon_code.startswith('clear'):
      icon = '晴朗'
    elif icon_code == 'rain':
      icon = '雨'
    elif icon_code == 'snow':
      icon = '雪'
    elif icon_code == 'sleet':
      icon = '雨夹雪'
    elif icon_code == 'wind':
      icon = '风'
    elif icon_code == 'fog':
      icon = '雾'
    elif icon_code == 'cloudy':
      icon = '多云'
    elif icon_code.startswith('partly-cloudy'):
      icon = '局部多云'
    else:
      icon = ''

  return icon

def get_wx():
  global location
  
  if api_key == "":
    return False

  location = location if location else auto_loc_lookup()

  if location is False:
    return False

  for locData in location:
    locData.encode('utf-8')

  try:
    if 'loc' in location:
      wx = json.loads(requests.get('https://api.darksky.net/forecast/' + api_key + '/' + location['loc'] + '?units=' + units + "&v=" + str(randint(0,100))).text)
    else:
      return False
  except RequestException:
    return False

  if units == 'si':
    unit = 'C'
    distance = 'm/s'
    distance_short = 'km'
  else:
    unit = 'F'
    distance = 'mph'
    distance_short = 'mi'

  try:

    weather_data = {}

    if 'currently' in wx:
      for item in wx['currently']:
        if item == 'temperature':
          weather_data['temperature'] = str(int(round(wx['currently']['temperature']))) + '°' + unit
        elif item == 'icon':
          weather_data['icon'] = get_wx_icon(str(wx['currently']['icon']), ret_icon=True)
        elif item == 'summary':
          weather_data['condition'] = get_wx_icon(str(wx['currently']['icon']), ret_icon=False) #str(wx['currently']['summary'].encode('utf-8'), encoding='utf-8')
        elif item == 'windSpeed':
          weather_data['wind'] = str(wx['currently']['windSpeed']) + ' ' + distance
        elif item == 'windBearing':
          weather_data['windBearing'] = calculate_bearing(wx['currently']['windBearing'])
        elif item == 'humidity':
          weather_data['humidity'] = str(int(round(wx['currently']['humidity'] * 100))) + '%'
        elif item == 'dewPoint':
          weather_data['dewPoint'] = str(wx['currently']['dewPoint'])
        elif item == 'visibility':
          weather_data['visibility'] = str(int(round(wx['currently']['visibility']))) + ' ' + distance_short
        elif item == 'pressure':
          weather_data['pressure'] = str(wx['currently']['pressure']) + ' mb'
        elif item == 'apparentTemperature':
          weather_data['feels_like'] = str(int(round(wx['currently']['apparentTemperature']))) + '°' + unit

    translator = Dict()
    if 'minutely' in wx and 'summary' in wx['minutely']:
      weather_data['next_hour'] = translator.dictionary(str(wx['minutely']['summary'], encoding='utf-8'))['trans_result']['data'][0]['dst']

    if 'daily' in wx and 'summary' in wx['daily']:
      weather_data['week'] = translator.dictionary(str((wx['daily']['summary'].encode('utf-8', 'ignore')), encoding='utf-8'))['trans_result']['data'][0]['dst']

    if 'city' in location and 'region' in location:
      if location['city'] == '' and location['region'] == '':
        if 'country' in location:
            country = full_country_name(location['country'])

            if country is False or location['country'] == '':
              weather_data['country'] = 'See Full Forecast'
            else:
              weather_data['country'] = country
      else:
        weather_data['city'] = str(location['city'].encode('utf-8'), encoding='utf-8')
        weather_data['region'] = str(location['region'].encode('utf-8'), encoding='utf-8')

    if 'loc' in location:
      weather_data['loc'] = str(location['loc'])

    if 'preformatted' in location:
      weather_data['preformatted'] = location['preformatted']

  except KeyError:
    return False

  return weather_data

def render_wx():

  if api_key == '':
    print('无API Key')
    print('---')
    print('获取API Key | href=https://darksky.net/dev')
    print('刷新 | refresh=true')
    return False

  weather_data = get_wx()
  loc_info = reverse_latlong_lookup(location['loc'])

  if weather_data is False:
    print('--')
    print('---')
    print('无法获取天气数据')
    print('刷新 | refresh=true')
    return False

  if 'icon' in weather_data and 'temperature' in weather_data:
    print(weather_data['temperature'] + ' | templateImage=' + weather_data['icon'])
  else:
    print('N/A')

  print('---')


  print(loc_info + ' | href=https://darksky.net/' + weather_data['loc'])

  if 'condition' in weather_data and 'feels_like' in weather_data:
    print(weather_data['condition'] + ', 体感温度: ' + weather_data['feels_like'])
  
  print('---')

  if 'next_hour' in weather_data:
    print(weather_data['next_hour'])
    print('---')

  print('---')

  if 'week' in weather_data:
    print("\n".join(textwrap.wrap(weather_data['week'], 50)))
    print('---')
  if 'wind' in weather_data and 'windBearing' in weather_data:
    ori = {
      'S': '南',
      'N': '北',
      'E': '东',
      'W': '西'
    }
    wind_ori = ''
    for i in weather_data['windBearing']:
      wind_ori += ori[i]
    print('风速: ' + weather_data['wind'] + '\n风向: ' + wind_ori)

  if 'humidity' in weather_data:
    print('湿度: ' + weather_data['humidity'])

  if 'dewPoint' in weather_data:
    print('露点: ' + weather_data['dewPoint'])

  if 'visibility' in weather_data:
    print('能见: ' + weather_data['visibility'])

  if 'pressure' in weather_data:
    print('气压: ' + weather_data['pressure'])

  print('---')
  print('刷新 | refresh=true')
  print('DarkSky | href=https://darksky.net/poweredby/?ref=bitbarWeather')

render_wx()
