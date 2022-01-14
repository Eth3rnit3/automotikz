#!/usr/bin/env python

# nohup python3 -u /home/pi/domoticz/scripts/customs/xiaomi_sensors.py > /home/pi/domoticz/scripts/customs/xiaomi_sensors.log &
# nohup touch /home/pi/test.txt && echo "GOOD" > /home/pi/test.txt &

import urllib.request
import base64, os, sys, signal, datetime, time
from threading import Thread
from lywsd03mmc import Lywsd03mmcClient
from PyP100 import PyP100

PID_FILE = '/tmp/domoticz-auto-sensor.pid'
DOMOTICZ_BASE_URL = 'http://127.0.0.1:8080/json.htm?type=command'
HEALTING_MIN_DAY = 22
HEALTING_MAX_DAY = 25
HEALTING_MIN_NIGHT = 16
HEALTING_MAX_NIGHT = 20
HUMIDITY_MIN = 50
HUMIDITY_MAX = 70
HEALTING_DEVICE_IDX = 3
VENTILATION_DEVICE_IDX = 4
HUMIDITY_DEVICE_IDX = 5

def domoticzrequest(url):
  request = urllib.request.Request(url)
  domoticzusername = ""
  domoticzpassword = ""
  base64string = base64.encodebytes(('%s:%s' % (domoticzusername, domoticzpassword)).encode()).decode().replace('\n', '')
  request.add_header("Authorization", "Basic %s" % base64string)
  response = urllib.request.urlopen(request)
  print('UPDATE - Domoticz updated successfull')
  return response.read()

def heating_device():
  p100 = PyP100.P100("192.168.1.31", "eth3rnit3@gmail.com", "Nidaigle031088")
  p100.handshake()
  p100.login()
  return p100

def ventilation_device():
  p100 = PyP100.P100("192.168.1.30", "eth3rnit3@gmail.com", "Nidaigle031088")
  p100.handshake()
  p100.login()
  return p100

def humidity_device():
  p100 = PyP100.P100("192.168.1.32", "eth3rnit3@gmail.com", "Nidaigle031088")
  p100.handshake()
  p100.login()
  return p100

def run_automations(values):
  print('{timestamp} - RUN - Automations...'.format(timestamp=str(datetime.datetime.now())))
  current_time = datetime.datetime.now().time()
  is_day = (current_time <= datetime.time(12, 00)) | (current_time >= datetime.time(18, 00))
  is_night = (current_time >= datetime.time(12, 00)) & (current_time <= datetime.time(18, 00))

  if is_day:
    print('RUN - Day automations')
    if (values.temperature < HEALTING_MIN_DAY):
      print('{timestamp} - ALERT - LOW HEALTING'.format(timestamp=str(datetime.datetime.now())))
      #heating_device().turnOn()
      update_domoticz_switch('Healting', HEALTING_DEVICE_IDX, 'On')
    elif (values.temperature > HEALTING_MAX_DAY):
      print('{timestamp} - ALERT - HIGHT HEALTING'.format(timestamp=str(datetime.datetime.now())))
      #heating_device().turnOff()
      update_domoticz_switch('Healting', HEALTING_DEVICE_IDX, 'Off')

  if is_night:
    print('RUN - Night automations')
    if (values.temperature < HEALTING_MIN_NIGHT):
      print('{timestamp} - ALERT - LOW HEALTING'.format(timestamp=str(datetime.datetime.now())))
      #heating_device().turnOn()
      update_domoticz_switch('Healting', HEALTING_DEVICE_IDX, 'On')
    elif (values.temperature > HEALTING_MAX_NIGHT):
      print('{timestamp} - ALERT - HIGHT HEALTING'.format(timestamp=str(datetime.datetime.now())))
      #heating_device().turnOff()
      update_domoticz_switch('Healting', HEALTING_DEVICE_IDX, 'Off')

  if (values.humidity >= HUMIDITY_MAX):
    print('{timestamp} - ALERT - HIGHT HUMIDITY'.format(timestamp=str(datetime.datetime.now())))
    #ventilation_device().turnOn()
    update_domoticz_switch('Ventilation', VENTILATION_DEVICE_IDX, 'On')
    update_domoticz_switch('Humidity', HUMIDITY_DEVICE_IDX, 'Off')
  elif (values.humidity <= (HUMIDITY_MAX - (HUMIDITY_MAX * 0.25))):
    print('{timestamp} - ALERT - LOW HUMIDITY'.format(timestamp=str(datetime.datetime.now())))
    #ventilation_device().turnOff()
    update_domoticz_switch('Ventilation', VENTILATION_DEVICE_IDX, 'Off')
    update_domoticz_switch('Humidity', HUMIDITY_DEVICE_IDX, 'On')

def read_data(address):
  print("{timestamp} - READ - Sensor data with command {address}".format(address=address, timestamp=str(datetime.datetime.now())))
  client = Lywsd03mmcClient(address)
  return client.data

def read_sensor_1():
  address = 'A4:C1:38:50:19:6F'
  idx_temp = 2
  values = read_data(address)
  print("{timestamp} - UPDATE - Domoticz sensor {idx_temp}".format(idx_temp=idx_temp, timestamp=str(datetime.datetime.now())))
  update_domoticz_sensor(values, idx_temp)
  run_automations(values)

def read_sensor_2():
  address = 'A4:C1:38:B9:F9:B9'
  idx_temp = 1
  values = read_data(address)
  print("{timestamp} - UPDATE - Domoticz sensor {idx_temp}".format(idx_temp=idx_temp, timestamp=str(datetime.datetime.now())))
  update_domoticz_sensor(values, idx_temp)
  run_automations(values)

def read_sensor_3():
  address = 'A4:C1:38:B9:F9:B9'
  idx_temp = 3
  values = read_data(address)
  print("{timestamp} - UPDATE - Domoticz sensor {idx_temp}".format(idx_temp=idx_temp, timestamp=str(datetime.datetime.now())))
  update_domoticz_sensor(values, idx_temp)
  run_automations(values)

def update_domoticz_sensor(values, idx_temp):
  temperature = values.temperature
  humidity    = values.humidity
  battery     = values.battery

  val_comfort = "0"
  if float(humidity) < 40:
      val_comfort = "2"
  elif float(humidity) <= 70:
      val_comfort = "1"
  elif float(humidity) > 70:
      val_comfort = "3"
  url = '{base_url}&param=udevice&idx={idx_temp}&nvalue=0&svalue={temperature};{humidity};{val_comfort}&battery={battery}'.format(
    base_url=DOMOTICZ_BASE_URL, idx_temp=idx_temp, temperature=temperature, humidity=humidity, val_comfort=val_comfort, battery=battery
  )
  print('UPDATE - Sensor {idx_temp} with values => {temperature}°C - {humidity}%'.format(
    idx_temp=idx_temp, temperature=temperature, humidity=humidity
  ))
  domoticzrequest(url)

def update_domoticz_switch(name: str, idx_switch: int, state: str):
  url = '{base_url}&param=switchlight&idx={idx_switch}&switchcmd={state}'.format(
    base_url=DOMOTICZ_BASE_URL, idx_switch=idx_switch, state=state
  )
  print('UPDATE - Switch {name} with idx {idx_switch} to state {state}'.format(name=name, idx_switch=idx_switch, state=state))
  domoticzrequest(url)

def auto_ventilation():
  while True:
    print('INFO - AutoVentilation turn On')
    update_domoticz_switch('Ventilation', VENTILATION_DEVICE_IDX, 'On')
    time.sleep(60 * 10)
    print('INFO - AutoVentilation turn Off')
    update_domoticz_switch('Ventilation', VENTILATION_DEVICE_IDX, 'Off')
    time.sleep(60 * 10)

def pid_exist():
  return os.path.exists(PID_FILE)

def clear_pid_file():
  if pid_exist():
    pid = open(PID_FILE).read()
    try:
      os.kill(int(pid), signal.SIGKILL)
    except OSError:
      print('INFO - Old process already killed')
    os.remove(PID_FILE)

def write_pid_file():
  clear_pid_file()
  file = open(PID_FILE, 'w')
  file.write(str(os.getpid()))
  file.close()

def run():
  write_pid_file()
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

run()