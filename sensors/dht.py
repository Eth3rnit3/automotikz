#!/usr/bin/env python

import sys
import yaml
import Adafruit_DHT
from ..shared.domoticz import update_widget

def load_sensors():
  with open('dht.yaml') as f:
    return yaml.safe_load(f)['sensors']

def read_and_update_sensors():
  sensors = load_sensors()
  for sensor in sensors:
    try:
      humidity, temperature = Adafruit_DHT.read_retry(sensor['sensor'], sensor['pin'])
      if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        values = str('{0:0.1f};{1:0.1f};2').format(temperature, humidity)
        update_widget(sensor['domoticz_idx'], values)
      else:
        print("Error while getting sensor value, trying next")
    except:
      print('Unexpected error with sensor {sensor}'.format(sensor=sensor))
      print(sys.exc_info()[0])
      continue

  sys.exit(1)

read_and_update_sensors()


