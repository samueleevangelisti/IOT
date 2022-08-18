from datetime import tzinfo
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

org = 'IoT'
token = '5XSTceUB8mbuFxUkS5RgqZiQ2nStsdyPiFSX5pbxBNxUS5COqT-t5bhxTxk7v6cDzvRMvH6P1a0ywgVIr31M_g=='
url='http://localhost:8086'

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

def fun_report(bucket):
  fun_query = 'from(bucket: {bucket})\
    |> range(start: -24h, stop: now())\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> aggregateWindow(every: 24h, fn: mean, createEmpty: false)\
    |> yield(name: "mean")'.format(bucket = bucket)

  fun_result = client.query_api().query(org=org, query=fun_query)

  df = []
  for table in fun_result:
      for record in table.records:
        df.append(record.get_value())
  return df




def fun_sensor_filter(bucket, field):
  fun_query = 'from(bucket: {bucket})\
    |> range(start: -5m, stop: now())\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == {field})\
    |> aggregateWindow(every: 1w, fn: last, createEmpty: false)\
    |> yield(name: "last")'.format(bucket = bucket, field = field)

  fun_result = client.query_api().query(org=org, query=fun_query)

  for table in fun_result:
      for record in table.records:
        return record.get_value()