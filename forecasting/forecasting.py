from datetime import tzinfo
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

from prophet import Prophet

from matplotlib.pyplot import figure

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
  |> range(start:-1h)\
  |> filter(fn: (r) => r["_measurement"] == "sensor")\
  |> filter(fn: (r) => r["_field"] == "temperature")'

result = client.query_api().query(org=org, query=query)

results = []
for table in result:
    for record in table.records:
        results.append((record.get_time().strftime("%Y-%m-%d %H:%M:%S"), record.get_value()))

df = pd.DataFrame (results, columns = ['ds', 'y'])
print (df)

df = df.iloc[:-1000]
m = Prophet(interval_width=0.95)
m.fit(df)

p=100
future = m.make_future_dataframe(periods=p, freq='1 s')

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
last_original_data= len(df)

#LAST REAL DATA

#PREDICTED DATA AFTER X_SECONDS


#pip install influxdb_client
#pip install pandas
fig1 = m.plot(forecast,uncertainty=True)
fig1.savefig('books_read.png')
fig1.show()
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from math import sqrt
#TEST COMPARISON EXPECTED AN
# D PREDICTED
predicted = forecast['yhat']
predicted= predicted.iloc[:-p]

expected = df['y'].values
predicted = predicted.values

print(len(expected))
print(len(predicted))

print(np.c_[expected,predicted])
numpy_array= np.c_[expected,predicted]

mae = mean_absolute_error(expected, predicted)
print('MAE: %f' % mae)
mse = mean_squared_error(expected, predicted)
print('MSE: %f' % mse)

mse = mean_squared_error(expected, predicted)
rmse = sqrt(mse)
print('RMSE: %f' % rmse)


x_seconds=2

print(expected[-1])
print(forecast['yhat'].iloc[last_original_data+x_seconds])