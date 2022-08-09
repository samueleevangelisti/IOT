from datetime import tzinfo
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from math import sqrt
from prophet import Prophet
from matplotlib.pyplot import figure
from time import time, sleep
import math
from sklearn.metrics import mean_squared_error
import statistics

bucket = 'IoT-sensor'
org = 'IoT'
token = 'sqnivYR104DFOVkJRUZd0FCzsKAhDobdVvw3tOtulrqyiTe-jnUbNiXJmIHq49atiF2zXk2mFQUC_kZJeA_AuQ=='
# Store the URL of your InfluxDB instance
url='http://localhost:8086'
client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
query_api = client.query_api()

query = 'from(bucket: "IoT-sensor")\
  |> range(start: 2022-07-04T18:00:00Z, stop: 2022-07-04T20:30:00Z)\
  |> filter(fn: (r) => r["_measurement"] == "sensor")\
  |> filter(fn: (r) => r["_field"] == "temperature")\
  |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'



def training(query):
    result = client.query_api().query(org=org, query=query)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_time().strftime("%Y-%m-%d %H:%M:%S"), record.get_value()))

    df = pd.DataFrame (results, columns = ['ds', 'y'])
    print (df)

    m = Prophet(interval_width=0.95)
    m.fit(df)

    p=10
    future = m.make_future_dataframe(periods=p, freq='1 min')
    forecast = m.predict(future)

    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])


    #fig1 = m.plot(forecast,uncertainty=True)
    #fig1.savefig('books_read.pdf')
    #fig1.show()


    predicted = forecast['yhat'].iloc[:-p].values
    expected = df['y'].values


        
    print('-'*40)
    
    mse = math.mean_squared_error(expected, predicted)
    print(' MSE: %.3f'% mse)
    
    rmse = math.sqrt(mean_squared_error(expected, predicted))
    print(' RMSE: %.3f'% rmse)
        
    mean = statistics.mean(predicted)
    print(' Mean: %.3f' % mean)
        
    stdev = statistics.stdev(predicted)
    print('Standard deviation:%.3f' % stdev)
        
    print('-'*40)

    print(forecast['yhat'].iloc[-p:])


while True:
  query_temperature = 'from(bucket: "IoT-sensor")\
    |> range(start: 2022-07-04T18:00:00Z, stop: 2022-07-04T19:50:00Z)\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == "temperature")\
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'

  query_humidity = 'from(bucket: "IoT-sensor")\
    |> range(start: 2022-07-04T18:00:00Z, stop: 2022-07-04T19:50:00Z)\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == "humidity")\
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'

  query_gas = 'from(bucket: "IoT-sensor")\
    |> range(start: 2022-07-04T18:00:00Z, stop: 2022-07-04T19:50:00Z)\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == "gas")\
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'

  model_temperature = training(query_temperature)


  model_humidity = training(query_humidity)


  model_gas = training(query_gas)

  sleep(60 - time() % 60)