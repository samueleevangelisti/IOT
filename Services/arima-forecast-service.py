import pickle
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import statsmodels
from statsmodels.tsa.arima.model import ARIMA
import influx
from statsmodels.tsa.arima.model import ARIMAResults
import csv
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import numpy
bucket = 'IoT-sensor'
org = 'IoT'
#token = 'WOqKy-gIeRs9U-IlbEzZdLZcTZHpwPsx2NpibTGWbYFq_IuDZVEAcMZ1VtrYKnjFEjs2vsQJl6H2vvXvfClfPw=='
token = '996mqBkUkAAnmEBU-l3WKyzl4AXfPVhdeGWPhIJBR79k6LNpeP1rRGqiWuw8dqzXbHZUL7H9wcHMLKu4auclyg=='
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

id = input("Enter ESP32 id (ESP32_eva):   ")

file_exists = os.path.exists(''+id+'_model_temperature.pkl')

if(file_exists==True):
   pickled_model = pickle.load(open(''+id+'_model_temperature.pkl', 'rb'))
   forecast_temperature=pickled_model.forecast(steps=10)

   pickled_model = pickle.load(open(''+id+'_model_humidity.pkl', 'rb'))
   forecast_humidity=pickled_model.forecast(steps=10)

   pickled_model = pickle.load(open(''+id+'_model_gas.pkl', 'rb'))
   forecast_gas=pickled_model.forecast(steps=10)
   #Temperature Graph Maker
   plt.clf()
   plt.figure(figsize=(10,10))
   data = forecast_temperature
   date_time= numpy.array(date[-10:])
   print(type(data))
   print(type(date_time))
   DF = pd.DataFrame()
   DF['yhat'] = data
   DF = DF.set_index(date_time)
   plt.plot(date_time,data)
   plt.gcf().autofmt_xdate()
   fig1 = plt
   fig1.savefig('arima_future_temperature.pdf')

   #Humidity Graph Maker
   plt.clf()
   plt.figure(figsize=(10,10))
   data = forecast_humidity
   date_time= numpy.array(date[-10:])
   print(type(data))
   print(type(date_time))
   DF = pd.DataFrame()
   DF['yhat'] = data
   DF = DF.set_index(date_time)
   plt.plot(date_time,data)
   plt.gcf().autofmt_xdate()
   fig1 = plt
   fig1.savefig('arima_future_humidity.pdf')

   #Gas Graph Maker
   plt.clf()
   plt.figure(figsize=(10,10))
   data = forecast_gas
   date_time= numpy.array(date[-10:])
   print(type(data))
   print(type(date_time))
   DF = pd.DataFrame()
   DF['yhat'] = data
   DF = DF.set_index(date_time)
   plt.plot(date_time,data)
   plt.gcf().autofmt_xdate()
   fig1 = plt
   fig1.savefig('arima_future_gas.pdf')


   #Influx write forecast data
   for i, item in enumerate(forecast_temperature):
      point_dict = dict({
         'time': date[i],
         'fields': dict({
               'temperature': forecast_temperature[i],
               'humidity': forecast_humidity[i],
               'gas': forecast_gas[i]
         })
      })
      print(point_dict)
      influx.write_forecasting_arima(point_dict)
   
else:
   print('This ID is not registered')