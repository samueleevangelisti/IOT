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

from pandas.tseries.offsets import DateOffset

from datetime import datetime
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
  |> range(start:-12h)\
  |> filter(fn: (r) => r["_measurement"] == "sensor")\
  |> filter(fn: (r) => r["_field"] == "temperature")\
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)'

result = client.query_api().query(org=org, query=query)

results = []
for table in result:
    for record in table.records:
        time= record.get_time()
        time = time + pd.Timedelta(hours=2)
        results.append((time.strftime("%Y-%m-%d %H:%M:%S"), record.get_value()))

df = pd.DataFrame (results, columns = ['ds', 'y'])

df['y_diff'] = df['y'].diff().dropna()
#df['ds'] = df['ds'] + pd.Timedelta(hours=2)
print (df)

z=df['y_diff'].plot()
figu = z.get_figure()
figu.savefig('differencing.pdf')




#step 3: chek wheter the time-series is stationary through the Dickey-fuller test
from statsmodels.tsa.stattools import adfuller
nrows=(len(df.values))
splitPoint = int(nrows * 0.80)
train = df['y'][:splitPoint]
test = df['y'][splitPoint:]
result = adfuller(train)
print('ADF statistic: %f' % result[0])
print('p-value: %f' %result[1])

train_new = train.diff().dropna()
result = adfuller(train_new)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])


from pmdarima import auto_arima
stepwise_fit=auto_arima(df['y'],trace=True,suppress_warning=True)
print(stepwise_fit.get_params().get("order"))
"""
print('='*70)

train = df[:splitPoint]
test = df[splitPoint:]

from pmdarima import auto_arima
stepwise_fit=auto_arima(df['y'],trace=True,suppress_warning=True)
print(stepwise_fit.summary())


model2=ARIMA(train['y'], order=(1,0,3))
model2=model2.fit()
print(model2.summary())
start=len(train)
end= len(train)+len(test)-1
pred=model2.predict(start=start,end=end,typ='levels')
print(pred)
print('='*70)

pred.plot(legend=True)
a=test['y'].plot(legend=True)

fig5 = a.get_figure()
fig5.savefig('figure.pdf')


print( model2.forecast())
"""
history = [x for x in train_new]
predictions = list()
time=list()



for t in test.index:
  model = ARIMA(history, order=stepwise_fit.get_params().get("order"))##########################################################################################
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


df['forecast'] = model_fit.predict(start=1,end=len(df),dynamic=False)


ax= df[['y','forecast']].plot(figsize=(12,8))


fig5 = ax.get_figure()
fig5.savefig('figure.pdf')

plt.plot(test)
plt.plot(predictions, color='red')



#!!!!!!!!!!!!!!!!!!!!!!!!!fig6=results.plot_predict(1,264)

datetime_object = datetime.strptime(df.iloc[-1]['ds'], '%Y-%m-%d %H:%M:%S')
future_dates=[datetime_object+ DateOffset(minutes=x)for x in range(1,10)]

tm=pd.Series(future_dates)

future_dataset_df=pd.DataFrame(columns=['ds','y'])
future_dataset_df['ds']=tm

frames = [df, future_dataset_df]

future_df = pd.concat(frames)
future_df = future_df.reset_index()
print(future_df)



future_df['forecast'] = model_fit.predict(start = 1, end = len(future_df), dynamic= False)
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


import math
from sklearn.metrics import mean_squared_error

rmse = math.sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f'% rmse)



df2 = pd. DataFrame (predictions)
df2. set_index(test.index, inplace=True)


#df3 = pd. DataFrame (df['forecast'])
#df3. set_index(test.index, inplace=True)

plt.clf()
plt.plot(test)
plt.plot(df2, color='red')
plt.savefig('my_plot.pdf')

print('--'*20)
print(len(df['y_diff']))

a_diff = df['y_diff']


a_diff_cumsum = a_diff.cumsum()
rebuilt = a_diff_cumsum.fillna(0) + 2
# Rebuilding  
a_diff_cumsum = a_diff.cumsum()
rebuilt = a_diff_cumsum.fillna(0) + df['y'].iloc[0]

df['forecast2']=rebuilt
print(df['forecast2'])
az=df[['y', 'forecast']].plot(figsize=(12, 8))
print(df)
figur = az.get_figure()
figur.savefig('diff_real.pdf')
#next_2 = model_fit.predict(n_periods=1)
#print(next_2)
print(len(df['y_diff']))

#model2=ARIMA(train['y'])
