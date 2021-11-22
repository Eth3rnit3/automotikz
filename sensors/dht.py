#!/usr/bin/env python

import os
import sys
import yaml
import Adafruit_DHT
from requests.auth import HTTPBasicAuth
import requests

domoticz_host = os.getenv('DOMOTICZ_HOST', '127.0.0.1')
domoticz_port = os.getenv('DOMOTICZ_PORT',  '8080')
domoticz_pcl  = os.getenv('DOMOTICZ_PROTOCOL',  'http')
user          = os.getenv('DOMOTICZ_USER',  '')
password      = os.getenv('DOMOTICZ_PASSWORD',  '')

def update_widget(idx, values):
  url = '{domoticz_pcl}://{domoticz_host}:{domoticz_port}/json.htm?type=command&param=udevice&idx={idx}&nvalue=0&svalue={values}'.format(
    domoticz_pcl=domoticz_pcl, domoticz_host=domoticz_host, domoticz_port=domoticz_port, idx=idx, values=values
  )
  response = requests.get(url, auth=HTTPBasicAuth(user,password))
  try:
    if  response.status_code != 200:
      print("Erreur API Domoticz")
    else:
      print('Sensor with id {idx} has been updated!'.format(idx=idx))
  except:
    print("Error while updating sensor value with domoticz api", sys.exc_info()[0])

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


