#pip install influxdb_client
#pip install pandas
#pip install searborn
#pip install statsmodels
#pip install sklearn
#pip install prophet
from posixpath import split
import pandas as pd
import seaborn as sns
import random
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from pandas.tseries.offsets import DateOffset
from datetime import datetime
from statsmodels.graphics import tsaplots
import numpy as np
import pickle
from time import time, sleep
import statistics

def training(query):
    result = client.query_api().query(org=org, query=query)

    results = []
    for table in result:
        for record in table.records:
            time= record.get_time()
            time = time + pd.Timedelta(hours=2)
            results.append((time.strftime("%Y-%m-%d %H:%M:%S"), record.get_value()))

    df = pd.DataFrame (results, columns = ['ds', 'y'])

    #step 3: chek wheter the time-series is stationary through the Dickey-fuller test
    nrows=(len(df.values))
    splitPoint = int(nrows * 0.66)

    train = df['y'][:splitPoint]
    test = df['y'][splitPoint:]

    history = [x for x in train]
    predictions = list()
    time=list()
    #Choose the best order for p,d,q for the arima model    
    from pmdarima import auto_arima
    stepwise_fit=auto_arima(df['y'],trace=True,suppress_warning=True)
    print(stepwise_fit.summary())
    auto_order=stepwise_fit.get_params().get("order")
  
    for t in test.index:
    #ARIMA(p,d,q)
        model = ARIMA(history, order=auto_order)
        model_fit = model.fit()
        output = model_fit.forecast()
        yest = output[0]
        predictions.append(yest)
        obs= test[t]
        history.append(obs)
        time2=df['ds'][t]
        print ('%d), time=%s,predicted=%f, expected=%f' % (t,time2,yest, obs))
        
        
    import math
    from sklearn.metrics import mean_squared_error

    print('-'*40)

    mse = math.mean_squared_error(test, predictions)
    print(' MSE: %.3f'% mse)
    

    rmse = math.sqrt(mean_squared_error(test, predictions))
    print(' RMSE: %.3f'% rmse)
    
    mean = statistics.mean(predictions)
    print(' Mean: %.3f' % mean)
    
    stdev = statistics.stdev(predictions)
    print('Standard deviation:%.3f' % stdev)
    
    print('-'*40)
        
    df['forecast'] = model_fit.predict(start=1,end=len(df),dynamic=False)
    expected_predicted= df[['y','forecast']].plot(figsize=(12,8))

    fig = expected_predicted.get_figure()
    fig.savefig('2_expected_predicted.pdf')
    return model_fit



bucket = 'IoT-sensor'
org = 'IoT'
token = 'sqnivYR104DFOVkJRUZd0FCzsKAhDobdVvw3tOtulrqyiTe-jnUbNiXJmIHq49atiF2zXk2mFQUC_kZJeA_AuQ=='
url='http://localhost:8086'

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

query_api = client.query_api()
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
  pickle.dump(model_temperature, open('model_temperature.pkl', 'wb'))


  model_humidity = training(query_humidity)
  pickle.dump(model_humidity, open('model_humidity.pkl', 'wb'))


  model_gas = training(query_gas)
  pickle.dump(model_gas, open('model_gas.pkl', 'wb'))

  sleep(60 - time() % 60)

