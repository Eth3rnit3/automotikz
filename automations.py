import datetime, time, os
from domoticz import update_domoticz_switch

HEALTING_MIN_DAY = int(os.environ.get('HEALTING_MIN_DAY'))
HEALTING_MAX_DAY = int(os.environ.get('HEALTING_MAX_DAY'))
HEALTING_MIN_NIGHT = int(os.environ.get('HEALTING_MIN_NIGHT'))
HEALTING_MAX_NIGHT = int(os.environ.get('HEALTING_MAX_NIGHT'))
HUMIDITY_MIN = int(os.environ.get('HUMIDITY_MIN'))
HUMIDITY_MAX = int(os.environ.get('HUMIDITY_MAX'))
HEALTING_DEVICE_IDX = int(os.environ.get('HEALTING_DEVICE_IDX'))
VENTILATION_DEVICE_IDX = int(os.environ.get('VENTILATION_DEVICE_IDX'))
HUMIDITY_DEVICE_IDX = int(os.environ.get('HUMIDITY_DEVICE_IDX'))

def auto_ventilation():
  while True:
    print('INFO - AutoVentilation turn On')
    update_domoticz_switch('Ventilation', VENTILATION_DEVICE_IDX, 'On')
    time.sleep(60 * 10)
    print('INFO - AutoVentilation turn Off')
    update_domoticz_switch('Ventilation', VENTILATION_DEVICE_IDX, 'Off')
    time.sleep(60 * 10)

def run_automations(values):
  print('{timestamp} - RUN - Automations...'.format(timestamp=str(datetime.datetime.now())))
  current_time = datetime.datetime.now().time()
  is_day = (current_time <= datetime.time(12, 00)) | (current_time >= datetime.time(18, 00))
  is_night = (current_time >= datetime.time(12, 00)) & (current_time <= datetime.time(18, 00))

  if is_day:
    print('RUN - Day automations')
    if (values.temperature < HEALTING_MIN_DAY):
      print('{timestamp} - ALERT - LOW HEALTING'.format(timestamp=str(datetime.datetime.now())))
      update_domoticz_switch('Healting', HEALTING_DEVICE_IDX, 'On')
    elif (values.temperature > HEALTING_MAX_DAY):
      print('{timestamp} - ALERT - HIGHT HEALTING'.format(timestamp=str(datetime.datetime.now())))
      update_domoticz_switch('Healting', HEALTING_DEVICE_IDX, 'Off')

  if is_night:
    print('RUN - Night automations')
    if (values.temperature < HEALTING_MIN_NIGHT):
      print('{timestamp} - ALERT - LOW HEALTING'.format(timestamp=str(datetime.datetime.now())))
      update_domoticz_switch('Healting', HEALTING_DEVICE_IDX, 'On')
    elif (values.temperature > HEALTING_MAX_NIGHT):
      print('{timestamp} - ALERT - HIGHT HEALTING'.format(timestamp=str(datetime.datetime.now())))
      update_domoticz_switch('Healting', HEALTING_DEVICE_IDX, 'Off')

  if (values.humidity >= HUMIDITY_MAX):
    print('{timestamp} - ALERT - HIGHT HUMIDITY'.format(timestamp=str(datetime.datetime.now())))
    update_domoticz_switch('Ventilation', VENTILATION_DEVICE_IDX, 'On')
    update_domoticz_switch('Humidity', HUMIDITY_DEVICE_IDX, 'Off')
  elif (values.humidity <= (HUMIDITY_MAX - (HUMIDITY_MAX * 0.25))):
    print('{timestamp} - ALERT - LOW HUMIDITY'.format(timestamp=str(datetime.datetime.now())))
    update_domoticz_switch('Ventilation', VENTILATION_DEVICE_IDX, 'Off')
    update_domoticz_switch('Humidity', HUMIDITY_DEVICE_IDX, 'On')