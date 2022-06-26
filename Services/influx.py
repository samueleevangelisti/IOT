from os import path
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class Influx:
  def __init__(self):
    f = open(path.abspath(path.join(path.dirname(__file__), '../Influx/influx-config.json')), 'r')
    self.config = json.load(f)
    f.close()
    self.client = InfluxDBClient(url=self.config['url'], token=self.config['token'], org=self.config['organization'])
    self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    self.query_api = self.client.query_api()

  def write(self, bucket_str, record):
    print('INFLUX -> [WAIT] write')
    try:
      self.write_api.write(bucket=self.config['bucket'][bucket_str], org=self.config['organization'], record=record)
      print('INFLUX -> [OK  ] write')
      return True
    except:
      print('INFLUX -> [ERR ] write')
      return False

  def write_sensor(self, data_dict):
    return self.write('sensor', data_dict)
  
  def write_weather(self, data_dict):
    return self.write('weather', data_dict)
    