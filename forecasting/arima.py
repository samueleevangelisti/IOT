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
  |> range(start:-3m)\
  |> filter(fn: (r) => r["_measurement"] == "sensor")\
  |> filter(fn: (r) => r["_field"] == "temperature")'

result = client.query_api().query(org=org, query=query)

results = []
for table in result:
    for record in table.records:
        time= record.get_time()
        time = time + pd.Timedelta(hours=2)
        results.append((time.strftime("%Y-%m-%d %H:%M:%S"), record.get_value()))

df = pd.DataFrame (results, columns = ['ds', 'y'])
#df['ds'] = df['ds'] + pd.Timedelta(hours=2)
print (df)

#step 3: chek wheter the time-series is stationary through the Dickey-fuller test
from statsmodels.tsa.stattools import adfuller
nrows=(len(df.values))
splitPoint = int(nrows * 0.60)
train = df['y'][:splitPoint]
test = df['y'][splitPoint:]
result = adfuller(train)
print('ADF statistic: %f' % result[0])
print('p-value: %f' %result[1])

train_new = train.diff().dropna()
result = adfuller(train_new)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])




from statsmodels.tsa.arima.model import ARIMA
history = [x for x in train]
predictions = list()
time=list()
print('-'*70)
print(test)
print('-'*70)
for t in test.index:
  model = ARIMA(history, order=(0,0,1))
  model_fit = model. fit()
  output = model_fit.forecast()
  yest = output[0]
  predictions.append(yest)
  obs= test[t]
  history.append(obs)
  time2=df['ds'][t]
  print ('%d), time=%s,predicted=%f, expected=%f' % (t,time2,yest, obs))

forecast = model_fit.get_forecast()
print(forecast.summary_frame())

yhat = forecast.predicted_mean
yhat_conf_int = forecast.conf_int(alpha=0.05)

print('Temperature Model Evaluation Summary:')
print('-'*40)
print('Mean: {}'.format(yhat))
print('Confidence Interval: {}'.format(yhat_conf_int))


df['forecast'] = model_fit.predict(start=1,end=len(df),dynamic=True)
ax= df[['y','forecast']].plot(figsize=(12,8))

fig5 = ax.get_figure()
fig5.savefig('figure.pdf')

#!!!!!!!!!!!!!!!!!!!!!!!!!fig6=results.plot_predict(1,264)

from pandas.tseries.offsets import DateOffset

from datetime import datetime
datetime_object = datetime.strptime(df.iloc[-1]['ds'], '%Y-%m-%d %H:%M:%S')
future_dates=[datetime_object+ DateOffset(seconds=x)for x in range(0,24)]
print('#'*50)
print(df)
print('#'*50)
print(future_dates)
print('#'*50)
tm=pd.Series(future_dates)
print(tm)
future_dataset_df=pd.DataFrame(columns=['ds','y'])
future_dataset_df['ds']=tm

frames = [df, future_dataset_df]

future_df = pd.concat(frames)
future_df = future_df.reset_index()
print(future_df)



future_df['forecast'] = model_fit.predict(start = 1, end = len(future_df), dynamic= True)
ay=future_df[['y', 'forecast']].plot(figsize=(12, 8))
print(future_df)
fig5 = ay.get_figure()
fig5.savefig('figure2.pdf')
import math
from sklearn.metrics import mean_squared_error

rmse = math.sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f'% rmse)

df2 = pd. DataFrame (predictions)
df2. set_index(test.index, inplace=True)

print(len(predictions))
print(len(test))

import math
from sklearn.metrics import mean_squared_error

rmse = math.sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f'% rmse)


df2 = pd. DataFrame (predictions)
df2. set_index(test.index, inplace=True)
plt.plot(test)
plt.plot(df2, color='red')
plt.savefig('my_plot.png')

print(df)
print(predictions)