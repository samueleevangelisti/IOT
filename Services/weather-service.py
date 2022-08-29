from os import path
import json
from datetime import datetime, timedelta
from pytz import timezone
from meteostat import Stations, Hourly
from time import sleep, gmtime
from influx import Influx

f = open(path.abspath(path.join(path.dirname(__file__), '../Weather/weather-service-config.json')), 'r')
config = json.load(f)
f.close()

influx = Influx()

while True:
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
    # datetime di inizio rilevamento
    start_datetime = end_datetime - timedelta(hours=1)
    print('[LOG ] start datetime: {}'.format(start_datetime))
    # rilevazioni orarie in base alle configurazioni
    hourly = Hourly(station, start_datetime, end_datetime).fetch()
    print('[LOG ] hourly')
    print(hourly)
    # salvataggio rilevazione attuale
    point_dict = dict({
        'fields': dict({
            'temperature': hourly['temp'][0]
        })
    })
    influx.write_weather(point_dict)
    # impostazione del timer al prossimo risveglio
    alarm_datetime = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1, minutes=5)
    print('[LOG ] alarm: {}'.format(alarm_datetime))
    sleep((alarm_datetime - datetime.now()).seconds)
