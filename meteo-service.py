from datetime import datetime, timedelta
from meteostat import Stations, Hourly
from time import sleep



latitude = 43.777734
logitude = 12.941052

while True:
  end = datetime.now()
  start = end - timedelta(hours = 1)

  hourly = Hourly(Stations().nearby(latitude, logitude).fetch(1), start, end).fetch().iloc[:, :1]

  sleep(3600)
