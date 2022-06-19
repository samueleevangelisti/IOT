import random
from time import sleep
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS



bucket = 'IoT-weather'
org = 'IoT'
token = 'URCbPPWYX6rl5KDvRVMfLFilMzEUvcGtOesPblLPTuUSt3PXIUkYDYUgVqKLhgrrf9Xhl52mkSwYKALf6OSxYw=='
url = 'http://localhost:8086'

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)

for i in range(60):
  p = influxdb_client.Point('my_measurement').tag('location', 'Prague').field('temperature', random.randint(10, 40))
  write_api.write(bucket=bucket, org=org, record=p)
  print('Write {:0>2d}/60'.format(i + 1))
  sleep(1)
