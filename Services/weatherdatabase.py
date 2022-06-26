from os import path
import json
from datetime import datetime

class WeatherDatabase:
  def __init__(self):
    self.file_path = path.abspath(path.join(path.dirname(__file__), '../Weather/weather-service-database.json'))
    f = open(self.file_path, 'r')
    self.database = json.load(f)
    f.close()

  def index(self, latitude, longitude):
    print('WEATHER_DATABASE -> [WAIT] index')
    index = -1
    for i, row in enumerate(self.database):
      if row['latitude'] == latitude and row['longitude'] == longitude:
        index = i
        break
    print('WEATHER_DATABASE -> [LOG ] index: {:d}'.format(index))
    print('WEATHER_DATABASE -> [OK  ] index')
    return index

  def store(self, latitude, longitude, datetime):
    print('WEATHER_DATABASE -> [WAIT] store')
    index = self.index(latitude, longitude)
    if index == -1:
      self.database.append(dict({
        'latitude': latitude,
        'longitude': longitude,
        'datetime': datetime.isoformat()
      }))
    else:
      self.database[index]['datetime'] = datetime.isoformat()
    f = open(self.file_path, 'w')
    f.write(json.dumps(self.database, indent=2))
    f.close()
    print('WEATHER_DATABASE -> [OK  ] store')

  def retrieve(self, latitude, longitude):
    print('WEATHER_DATABASE -> [WAIT] retrieve')
    index = self.index(latitude, longitude)
    if index == -1:
      result_datetime = None
    else:
      result_datetime = datetime.fromisoformat(self.database[index]['datetime'])
    print('WEATHER_DATABASE -> [LOG ] datetime: {}'.format(result_datetime))
    print('WEATHER_DATABASE -> [OK  ] retrieve')
    return result_datetime
