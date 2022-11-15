#pip install influxdb_client
#pip install pandas
#pip install searborn
#pip install statsmodels
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
from statsmodels.tsa.stattools import adfuller
import csv
import math
from sklearn.metrics import mean_squared_error
def training(query,name_file):
    result = client.query_api().query(org=org, query=query)
    print(result)
    results = []
    for table in result:
        for record in table.records:
            time= record.get_time()
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
    
    result = adfuller(train)
    plt.clf()
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])

    train_new = train.diff().dropna()
    result = adfuller(train_new)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    fig_autocorrelation = tsaplots.plot_acf(train_new, lags=10)
    
    fig_partial = tsaplots.plot_pacf(train_new, lags=10)

    
    fig_autocorrelation.savefig('autocorrelation_'+name_file)
    
    fig_partial.savefig('partial_autocorrelation_'+name_file)
    plt.clf()
   

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
        
    print('-'*40)
    mse = mean_squared_error(test, predictions)
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
    fig.savefig(name_file)
        
    datetime_object = datetime.strptime(df.iloc[-1]['ds'], '%Y-%m-%d %H:%M:%S')
    df_pred=[datetime_object + DateOffset(minutes=x)for x in range(1,11)]
    
    tm=pd.Series(df_pred).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    file = open('date.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(tm)
    file.close()

    return model_fit

bucket = 'IoT-sensor'
org = 'IoT'
#token = 'WOqKy-gIeRs9U-IlbEzZdLZcTZHpwPsx2NpibTGWbYFq_IuDZVEAcMZ1VtrYKnjFEjs2vsQJl6H2vvXvfClfPw=='
token = '996mqBkUkAAnmEBU-l3WKyzl4AXfPVhdeGWPhIJBR79k6LNpeP1rRGqiWuw8dqzXbHZUL7H9wcHMLKu4auclyg=='
url='http://localhost:8086'

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

query_api = client.query_api()
id = input("Enter ESP32 id: ")
while True:
  test='temperature'
  query_temperature = 'from(bucket: "IoT-sensor")\
    |> range(start: 2022-07-06T13:00:00Z , stop:2022-07-07T02:00:00Z)\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == "temperature")\
    |> filter(fn: (r) => r["id"] == "'+id+'")\
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'

  query_humidity = 'from(bucket: "IoT-sensor")\
    |> range(start: 2022-07-06T12:00:00Z , stop:2022-07-07T02:00:00Z)\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == "humidity")\
    |> filter(fn: (r) => r["id"] == "'+id+'")\
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'

  query_gas = 'from(bucket: "IoT-sensor")\
    |> range(start: 2022-07-06T12:00:00Z , stop:2022-07-07T02:00:00Z)\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == "gas")\
    |> filter(fn: (r) => r["id"] == "'+id+'")\
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'
  temperature="arima_temperature.jpg"
  humidity="arima_humidity.jpg"
  gas="arima_gas.jpg"
  print('TEMPERATURE ------------------------------')
  model_temperature = training(query_temperature,temperature)
  pickle.dump(model_temperature, open(''+id+'_model_temperature.pkl', 'wb'))
  print('HUMIDITY ------------------------------')
  model_humidity = training(query_humidity,humidity)
  pickle.dump(model_humidity, open(''+id+'_model_humidity.pkl', 'wb'))
  print('GAS ------------------------------')
  model_gas = training(query_gas,gas)
  pickle.dump(model_gas, open(''+id+'_model_gas.pkl', 'wb'))

  sleep(120 - time() % 120)

