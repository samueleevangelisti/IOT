import pickle
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import statsmodels
from statsmodels.tsa.arima.model import ARIMA
import influx

import csv
import pandas as pd
import os.path

bucket = 'IoT-sensor'
org = 'IoT'
token = 'WOqKy-gIeRs9U-IlbEzZdLZcTZHpwPsx2NpibTGWbYFq_IuDZVEAcMZ1VtrYKnjFEjs2vsQJl6H2vvXvfClfPw=='
url='http://localhost:8086'


influx = influx.Influx()
client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
influx.delete_forecasting_arima_all()

df = pd.read_csv('date.csv')

date=[]
for col in df.columns:
   date.append(col)

print(len(date))

id = input("Enter ESP32 id (ESP32_eva):   ")

file_exists = os.path.exists(''+id+'_model_temperature.pkl')

if(file_exists==True):
   pickled_model = pickle.load(open(''+id+'_model_temperature.pkl', 'rb'))
   forecast_temperature=pickled_model.forecast(steps=10)
   #print('temp_conf= ',pd.DataFrame(forecast_temperature.conf_int(alpha=0.05)))
   
   forecast_temperature2=pickled_model.get_forecast(steps=10)
   print('temp_conf= ',pd.DataFrame(forecast_temperature2.conf_int(alpha=0.05)))

   forecast_temperature3=pickled_model.get_forecast()
   print('temp_conf= ',pd.DataFrame(forecast_temperature3.conf_int(alpha=0.05)))
   pickled_model = pickle.load(open(''+id+'_model_humidity.pkl', 'rb'))
   forecast_humidity=pickled_model.forecast(steps=10)

   pickled_model = pickle.load(open(''+id+'_model_gas.pkl', 'rb'))
   forecast_gas=pickled_model.forecast(steps=10)
   print(forecast_temperature)
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
      print(point_dict)
      influx.write_forecasting_arima(point_dict)
   

else:
   print('This ID is not registered')