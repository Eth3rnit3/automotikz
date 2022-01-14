import datetime, os
from automations import HEALTING_MAX_DAY
from lywsd03mmc import Lywsd03mmcClient
from PyP100 import PyP100

DEVICE_USER = os.environ.get('DEVICE_USER')
DEVICE_PASS = os.environ.get('DEVICE_PASS')
HEALTING_DEVICE = os.environ.get('HEALTING_DEVICE')
VENTILATION_DEVICE = os.environ.get('VENTILATION_DEVICE')
HUMIDITY_DEVICE = os.environ.get('HUMIDITY_DEVICE')

def read_data(mac_address: str):
  print("{timestamp} - READ - Sensor data with command {mac_address}".format(mac_address=mac_address, timestamp=str(datetime.datetime.now())))
  client = Lywsd03mmcClient(mac_address)
  return client.data

def device_client(address: str):
  p100 = PyP100.P100(address, DEVICE_USER, DEVICE_PASS)
  p100.handshake()
  p100.login()
  return p100

def heating_device():
  return device_client(HEALTING_DEVICE)

def ventilation_device():
  return device_client(VENTILATION_DEVICE)

def humidity_device():
  return device_client(HUMIDITY_DEVICE)