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
from influx import Influx
import pandas as pd
import matplotlib.pyplot as plt

influx = Influx()

id = input("Enter ESP32 id: ")
# bucket = 'IoT-sensor'
# org = 'IoT'
# token = 'WOqKy-gIeRs9U-IlbEzZdLZcTZHpwPsx2NpibTGWbYFq_IuDZVEAcMZ1VtrYKnjFEjs2vsQJl6H2vvXvfClfPw=='

# # token = '996mqBkUkAAnmEBU-l3WKyzl4AXfPVhdeGWPhIJBR79k6LNpeP1rRGqiWuw8dqzXbHZUL7H9wcHMLKu4auclyg=='
# # Store the URL of your InfluxDB instance
# url='http://localhost:8086'
# client = influxdb_client.InfluxDBClient(
#    url=url,
#    token=token,
#    org=org
# )
# query_api = client.query_api()

global date


influx.delete_forecasting_prophet_all()
def training(query,name_file):
    # result = client.query_api().query(org=org, query=query)
    result = influx.query(query=query)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_time().strftime("%Y-%m-%d %H:%M:%S"), record.get_value()))

    df = pd.DataFrame (results, columns = ['ds', 'y'])
    #print (df)

    m = Prophet(interval_width=0.95)
    m.fit(df)

    p=10
    future = m.make_future_dataframe(periods=p, freq='1 min')
    forecast = m.predict(future)

    #Graph maker
    data = df['y'][:len(df)]
    pred = forecast['yhat'][:len(df)]
    date_time= forecast['ds'][:len(df)]
    plt.clf()

    plt.figure(figsize=(13,8))
    DF = pd.DataFrame()
    DF['yhat'] = data
    DF['y'] = pred
    DF = DF.set_index(date_time)
    plt.plot(date_time,data)
    plt.gcf().autofmt_xdate()

    data = df['y'][:len(df)]
    pred = forecast['yhat'][:len(df)]
    date_time= forecast['ds'][:len(df)]

    DF = pd.DataFrame()
    DF['yhat'] = data
    DF['y'] = pred
    DF = DF.set_index(date_time)
    plt.plot(date_time,pred)
    plt.gcf().autofmt_xdate()

    data = forecast['yhat'][-9:]
    date_time= forecast['ds'][-9:]

    DF = pd.DataFrame()
    DF['yhat'] = data
    DF = DF.set_index(date_time)
    plt.plot(date_time,data)
    plt.gcf().autofmt_xdate()
    
    fig1 = plt    
    fig1.savefig(name_file)
    #end graph maker


    predicted = forecast['yhat'].iloc[:-p].values
    expected = df['y'].values
    if(len(predicted)!=len(expected)):
      predicted = forecast['yhat'].iloc[:-p+1].values
    


        
    print('-'*40)
    mse = mean_squared_error(expected, predicted)
    print(' MSE: %.3f'% mse)
    rmse = math.sqrt(mean_squared_error(expected, predicted))
    print(' RMSE: %.3f'% rmse)
    mean = statistics.mean(predicted)
    print(' Mean: %.3f' % mean)
    stdev = statistics.stdev(predicted)
    print('Standard deviation:%.3f' % stdev)
    print('-'*40)

    #print(forecast['yhat'].iloc[-p:])
    
    date=forecast['ds'].iloc[-p:]
    #print(date.dt.strftime('%Y-%m-%dT%H:%M:%SZ'))

    return forecast.iloc[-p:]

while True:
  

  id_query = 'from(bucket: "IoT-sensor")\
    |> range(start: 2022-07-06T12:00:00Z)\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == "temperature")\
    |> filter(fn: (r) => r["id"] == "'+id+'")\
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'

  # check_id=client.query_api().query(org=org, query=id_query)
  check_id = influx.query(query=id_query)
  
  if not check_id:
    print('ESP32 id not found')
    break
  else:
    
    query_temperature = 'from(bucket: "IoT-sensor")\
      |> range(start: 2022-07-06T12:00:00Z)\
      |> filter(fn: (r) => r["_measurement"] == "sensor")\
      |> filter(fn: (r) => r["_field"] == "temperature")\
      |> filter(fn: (r) => r["id"] == "'+id+'")\
      |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'
    query_humidity = 'from(bucket: "IoT-sensor")\
      |> range(start: 2022-07-06T12:00:00Z)\
      |> filter(fn: (r) => r["_measurement"] == "sensor")\
      |> filter(fn: (r) => r["_field"] == "humidity")\
      |> filter(fn: (r) => r["id"] == "'+id+'")\
      |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'

    query_gas = 'from(bucket: "IoT-sensor")\
      |> range(start: 2022-07-06T12:00:00Z)\
      |> filter(fn: (r) => r["_measurement"] == "sensor")\
      |> filter(fn: (r) => r["_field"] == "gas")\
      |> filter(fn: (r) => r["id"] == "'+id+'")\
      |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'
    temperature="prophet_temperature.pdf"
    humidity="prophet_humidity.pdf"
    gas="prophet_gas.pdf"
    model_temperature = training(query_temperature,temperature)

    model_humidity = training(query_humidity,humidity)

    model_gas = training(query_gas,gas)

    for i, item in enumerate(model_temperature['yhat']):
        point_dict = dict({
          'time': model_temperature['ds'].iloc[i].isoformat() + 'Z',
          'fields': dict({
                'temperature': model_temperature['yhat'].iloc[i],
                'humidity': model_humidity['yhat'].iloc[i],
                'gas': model_gas['yhat'].iloc[i]
          })
        })
        influx.write_forecasting_prophet(point_dict)

  sleep(60 - time() % 60)