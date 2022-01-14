import time, sys, datetime, os
from threading import Thread
from runtime import start, pid_exist
from automations import auto_ventilation, run_automations
from domoticz import update_domoticz_sensor
from sensors import read_data

def read_sensor_1():
  address = os.environ.get('SENSOR_ADDRESS_1')
  idx_temp = 2
  values = read_data(address)
  print("{timestamp} - UPDATE - Domoticz sensor {idx_temp}".format(idx_temp=idx_temp, timestamp=str(datetime.datetime.now())))
  update_domoticz_sensor(values, idx_temp)
  run_automations(values)

def read_sensor_2():
  address = os.environ.get('SENSOR_ADDRESS_2')
  idx_temp = 1
  values = read_data(address)
  print("{timestamp} - UPDATE - Domoticz sensor {idx_temp}".format(idx_temp=idx_temp, timestamp=str(datetime.datetime.now())))
  update_domoticz_sensor(values, idx_temp)
  run_automations(values)

def app():
  auto_ventilation_th = Thread(target=auto_ventilation)
  auto_ventilation_th.start()
  while pid_exist():
    try:
      th = Thread(target=read_sensor_1)
      th.start()
      time.sleep(20)
      th = Thread(target=read_sensor_2)
      th.start()
      time.sleep(20)
    except:
      e = sys.exc_info()[0]
      print("{timestamp} - ERROR - While process sensor, error => {err}".format(err=str(e), timestamp=str(datetime.datetime.now())))
      pass

start(app)