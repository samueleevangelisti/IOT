import pickle
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

#from influx import Influx
import csv
import pandas as pd

bucket = 'IoT-sensor'
org = 'IoT'
token = 'sqnivYR104DFOVkJRUZd0FCzsKAhDobdVvw3tOtulrqyiTe-jnUbNiXJmIHq49atiF2zXk2mFQUC_kZJeA_AuQ=='
url='http://localhost:8086'


#influx = Influx()
client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
#influx.delete_forecasting_arima_all()

df = pd.read_csv('date.csv')

date=[]
for col in df.columns:
   date.append(col)

print(len(date))

id = input("Enter ESP32 id (ESP32_eva):   ")

import os.path

file_exists = os.path.exists(''+id+'_model_temperature.pkl')

print(file_exists)

pickled_model = pickle.load(open(''+id+'_model_temperature.pkl', 'rb'))
forecast_temperature=pickled_model.forecast(steps=10)

pickled_model = pickle.load(open(''+id+'_model_humidity.pkl', 'rb'))
forecast_humidity=pickled_model.forecast(steps=10)

pickled_model = pickle.load(open(''+id+'_model_gas.pkl', 'rb'))
forecast_gas=pickled_model.forecast(steps=10)

#TEMPERATURE
for i, item in enumerate(forecast_temperature):
   point_dict = dict({
      'time': date[i],
      'measurement': 'forecasting',
      'fields': dict({
            'temperature': forecast_temperature[i],
            'humidity': forecast_humidity[i],
            'gas': forecast_gas[i]
      })
   })
   #influx.write_forecasting_arima(point_dict)
