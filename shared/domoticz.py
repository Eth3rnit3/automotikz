#!/usr/bin/env python

import os
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