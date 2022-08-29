import pickle
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from influx import Influx
bucket = 'IoT-sensor'
org = 'IoT'
token = 'sqnivYR104DFOVkJRUZd0FCzsKAhDobdVvw3tOtulrqyiTe-jnUbNiXJmIHq49atiF2zXk2mFQUC_kZJeA_AuQ=='
url='http://localhost:8086'

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

pickled_model = pickle.load(open('model_temperature.pkl', 'rb'))

forecast=pickled_model.forecast(steps=10)
print(forecast)
pickled_model = pickle.load(open('model_humidity.pkl', 'rb'))

forecast=pickled_model.forecast(steps=10)
print(forecast)

pickled_model = pickle.load(open('model_gas.pkl', 'rb'))

forecast=pickled_model.forecast(steps=10)

print(forecast)
write_api = client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket=['bucket']['forecasting']['arima'], org=org, record=forecast[0])