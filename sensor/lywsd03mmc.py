#!/usr/bin/env python

import urllib.request
import yaml
import base64
import os
import sys
import re

domoticz_host = os.getenv('DOMOTICZ_HOST', '127.0.0.1')
domoticz_port = os.getenv('DOMOTICZ_PORT',  '8080')
domoticz_pcl  = os.getenv('DOMOTICZ_PROTOCOL',  'http')
user          = os.getenv('DOMOTICZ_USER',  '')
password      = os.getenv('DOMOTICZ_PASSWORD',  '')

base64string  = base64.encodebytes(('%s:%s' % (user, password)).encode()).decode().replace('\n', '')
fltRegex     = re.compile(r'([0-9]*\.[0-9]+)')
intRegex      = re.compile(r'([0-9]+)')

def domoticzrequest (url):
  request = urllib.request.Request(url)
  request.add_header("Authorization", "Basic %s" % base64string)
  response = urllib.request.urlopen(request)
  return response.read()

def load_sensors():
  with open('lywsd03mmc.yaml') as f:
    return yaml.safe_load(f)['sensors']

def read_and_update_sensors():
  sensors = load_sensors()
  for sensor in sensors:
    try:
      stream = os.popen('lywsd03mmc {mac_address}'.format(mac_address=sensor['mac_address']))
      output = stream.read()
      result = output.split("\n")

      match = fltRegex.search(result[1])
      temperature = match.group(1)

      match = intRegex.search(result[2])
      humidity = match.group(1)

      match = intRegex.search(result[3])
      battery = match.group(1)

      val_comfort = "0"
      if float(humidity) < 40:
          val_comfort = "2"
      elif float(humidity) <= 70:
          val_comfort = "1"
      elif float(humidity) > 70:
          val_comfort = "3"
      url = '{domoticz_pcl}://{domoticz_host}:{domoticz_port}/json.htm?type=command&param=udevice&idx={idx_temp}&nvalue=0&svalue={temperature};{humidity};{val_comfort}&battery={battery}'.format(
        domoticz_pcl=domoticz_pcl, domoticz_host=domoticz_host, domoticz_port=domoticz_port, idx_temp=sensor['domoticz_idx'], temperature=temperature, humidity=humidity, val_comfort=val_comfort, battery=battery
      )
      domoticzrequest(url)
    except:
      print('Unexpected error with sensor {sensor}'.format(sensor=sensor))
      print(sys.exc_info()[0])
      continue

  sys.exit(1)

read_and_update_sensors()
