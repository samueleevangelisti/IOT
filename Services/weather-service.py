from os import path
import json
from datetime import datetime, timedelta
from pytz import timezone
from meteostat import Stations, Hourly
from time import sleep, gmtime
import atexit
from weatherdatabase import WeatherDatabase

f = open(path.abspath(path.join(path.dirname(__file__), '../Weather/weather-service-config.json')), 'r')
config = json.load(f)
f.close()

weather_database = WeatherDatabase()

def on_close():
  last_datetime = datetime.now()
  print('[LOG ] last datetime: {}'.format(last_datetime))
  weather_database.store(config['latitude'], config['longitude'], last_datetime)

atexit.register(on_close)

# orario UTC
utc_time = gmtime()
# orario locale
locale_datetime = datetime.now()
# converto l'orario UTC in datetime allineato al secondo con l'orario locale
utc_datetime = datetime(utc_time.tm_year, utc_time.tm_mon, utc_time.tm_mday, utc_time.tm_hour, utc_time.tm_min, locale_datetime.second, locale_datetime.microsecond)
print('[LOG ] utc datetime: {}'.format(utc_datetime))
print('[LOG ] locale datetime: {}'.format(locale_datetime))
# differenza del locale rispetto a UTC
utc_locale_timedelta = locale_datetime - utc_datetime
print('[LOG ] utc/locale timedelta: {}'.format(utc_locale_timedelta))
# stazione meteo
station = Stations().nearby(config['latitude'], config['longitude']).fetch(1)
# differenza della stazione rispetto a UTC
utc_station_timedelta = timezone(station['timezone'].values[0]).utcoffset(utc_datetime)
print('[LOG ] utc/station timedelta: {}'.format(utc_station_timedelta))
# differenza del locale rispetto alla stazione
locale_station_timedelta = utc_station_timedelta - utc_locale_timedelta
print('[LOG ] locale/station timedelta: {}'.format(locale_station_timedelta))
# data di fine rilevazioni in base al timezone della stazione
end_datetime = locale_datetime + locale_station_timedelta
print('[LOG ] end datetime: {}'.format(end_datetime))
# data di ultimo funzionamento
last_datetime = weather_database.retrieve(config['latitude'], config['longitude'])
if last_datetime == None:
  last_datetime = datetime(1970, 1, 1)
print('[LOG ] last datetime: {}'.format(last_datetime))
# tempo passata dall'ultimo rilevamento
end_last_timedelta = end_datetime - last_datetime
print('[LOG ] end/last timedelta: {}'.format(end_last_timedelta))
# la data di inizio rilevamenti viene impostata massimo a un giorno prima
if end_last_timedelta < timedelta(days=1):
  start_datetime = end_datetime - end_last_timedelta
else:
  start_datetime = end_datetime - timedelta(days=1)
print('[LOG ] start datetime: {}'.format(start_datetime))
# rilevazioni orarie in base alle configurazioni
hourly = Hourly(station, start_datetime, end_datetime).fetch().iloc[:, :1]
print(hourly)
# impostazione del timer al prossimo risveglio
alarm_datetime = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
print('[LOG ] alarm: {}'.format(alarm_datetime))
# il service aspetta la prossima rilevazione utile
sleep((alarm_datetime - datetime.now()).seconds)

# while True:
#   end = datetime.now()
#   start = end - timedelta(hours = 1)
#   hourly = Hourly(Stations().nearby(config['latitude'], config['longitude']).fetch(1), start, end).fetch().iloc[:, :1]
#   print(Stations().nearby(config['latitude'], config['longitude']).fetch(1))
#   print(hourly)
#   print(hourly.index)
#   sleep(3600)
