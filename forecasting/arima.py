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
#import pickle
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

query = 'from(bucket: "IoT-sensor")\
  |> range(start: 2022-07-04T18:00:00Z, stop: 2022-07-04T19:50:00Z)\
  |> filter(fn: (r) => r["_measurement"] == "sensor")\
  |> filter(fn: (r) => r["_field"] == "temperature")\
  |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)'

result = client.query_api().query(org=org, query=query)

results = []
for table in result:
    for record in table.records:
        time= record.get_time()
        time = time + pd.Timedelta(hours=2)
        results.append((time.strftime("%Y-%m-%d %H:%M:%S"), record.get_value()))

df = pd.DataFrame (results, columns = ['ds', 'y'])
print (df)

#step 3: chek wheter the time-series is stationary through the Dickey-fuller test
nrows=(len(df.values))
splitPoint = int(nrows * 0.66)

train = df['y'][:splitPoint]
test = df['y'][splitPoint:]

result = adfuller(train)
print('ADF statistic: %f' %result[0])
print('p-value: %f' %result[1])

train_new = train.diff().dropna()

result = adfuller(train_new)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])


train_new2 = train_new.diff().dropna()

result = adfuller(train_new2)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

fig = tsaplots.plot_acf(train_new2, lags=10)

fig2= tsaplots.plot_pacf(train_new2, lags=10)

fig.savefig('1_ac.pdf')
fig2.savefig('1_pac.pdf')


import statsmodels.api as sm

acf, ci = sm.tsa.acf(train_new, alpha=0.05)
pacf, ci = sm.tsa.pacf(train_new, alpha=0.05)

"""
from pmdarima import auto_arima
stepwise_fit=auto_arima(df['y'],trace=True,suppress_warning=True)
print(stepwise_fit.summary())
auto_order=stepwise_fit.get_params().get("order")
"""
history = [x for x in train]
predictions = list()
time=list()

for t in test.index:
  #ARIMA(p,d,q)
  model = ARIMA(history, order=(1,1,1))##########################################################################################
  model_fit = model.fit()
  output = model_fit.forecast()
  yest = output[0]
  predictions.append(yest)
  obs= test[t]
  history.append(obs)
  time2=df['ds'][t]
  print ('%d), time=%s,predicted=%f, expected=%f' % (t,time2,yest, obs))

forecast = model_fit.get_forecast()
yhat = forecast.predicted_mean
yhat_conf_int = forecast.conf_int(alpha=0.05)

import warnings
from math import sqrt

from sklearn.metrics import mean_squared_error





print('-'*40)
rmse = sqrt(mean_squared_error(test, predictions))
print(rmse)
print('-'*40)

df['forecast'] = model_fit.predict(start=1,end=len(df),dynamic=False)
expected_predicted= df[['y','forecast']].plot(figsize=(12,8))

fig = expected_predicted.get_figure()
fig.savefig('2_expected_predicted.pdf')



datetime_object = datetime.strptime(df.iloc[-1]['ds'], '%Y-%m-%d %H:%M:%S')
df_pred=[datetime_object + DateOffset(minutes=x)for x in range(1,10)]

tm=pd.Series(df_pred).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

df_pred=pd.DataFrame(columns=['ds','y','forecast'])
df_pred['ds']=tm

df2 = pd.concat([df, df_pred])

df2 = df2.reset_index()

import numpy as np
df2['future'] = np.nan
df2['future'].iloc[-10:]=model_fit.forecast(steps=10)

print(df2)
real_future= df2[['y','future']].plot(figsize=(12,8))

fig2 = real_future.get_figure()
fig2.savefig('3_real_future.pdf')

future= df2[['future']].plot(figsize=(12,8))

fig2 = future.get_figure()
fig2.savefig('3_future.pdf')


future= df2[['forecast','future']].plot(figsize=(12,8))

fig2 = future.get_figure()
fig2.savefig('forecast_future.pdf')


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

plt.clf()
plt.plot(test)
plt.plot(df2, color='red')

plt.savefig('test_forecast.pdf')


print(type(tm))

print(tm.tolist())
print(tm.strftime('%Y-%m-%dT%H:%M:%SZ'))
# print(model_fit.forecast(steps=500))

""" 
# grid search ARIMA parameters for time series
import warnings
from math import sqrt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# evaluate an ARIMA model for a given order (p,d,q)
def evaluate_arima_model(X, arima_order):
	# prepare training dataset
	train_size = int(len(X) * 0.66)
	train, test = X[0:train_size], X[train_size:]
	history = [x for x in train]
	# make predictions
	predictions = list()
	for t in range(len(test)):
		model = ARIMA(history, order=arima_order)
		model_fit = model.fit()
		yhat = model_fit.forecast()[0]
		predictions.append(yhat)
		history.append(test[t])
	# calculate out of sample error
	rmse = sqrt(mean_squared_error(test, predictions))
	return rmse

# evaluate combinations of p, d and q values for an ARIMA model


# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):

	best_score, best_cfg = float("inf"), None
	for p in p_values:
		for d in d_values:
			for q in q_values:
				order = (p,d,q)
				try:
					rmse = evaluate_arima_model(dataset, order)
					if rmse < best_score:
						best_score, best_cfg = rmse, order
					print('ARIMA%s RMSE=%.3f' % (order,rmse))
				except:
					continue
	print('Best ARIMA%s RMSE=%.3f' % (best_cfg, best_score))



# load dataset
# evaluate parameters
p_values = [0, 1, 2, 4, 6, 8, 10]
d_values = range(0, 3)
q_values = range(0, 3)
warnings.filterwarnings("ignore")
evaluate_models(history, p_values, d_values, q_values)

print(auto_order)

"""