import urllib.request
import base64, os

DOMOTICZ_HOST = os.environ.get('DOMOTICZ_HOST')
DOMOTICZ_PORT = os.environ.get('DOMOTICZ_PORT')
DOMOTICZ_USER = os.environ.get('DOMOTICZ_USER')
DOMOTICZ_PASSWORD = os.environ.get('DOMOTICZ_PASSWORD')

base64string = base64.encodebytes(('%s:%s' % (DOMOTICZ_USER, DOMOTICZ_PASSWORD)).encode()).decode().replace('\n', '')
base_url = 'http://{host}:{port}/json.htm?type=command'.format(host=DOMOTICZ_HOST, port=DOMOTICZ_PORT)

def domoticzrequest(url):
  request = urllib.request.Request(url)
  request.add_header("Authorization", "Basic %s" % base64string)
  response = urllib.request.urlopen(request)
  print('UPDATE - Domoticz updated successfull')
  return response.read()

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
    base_url=base_url, idx_temp=idx_temp, temperature=temperature, humidity=humidity, val_comfort=val_comfort, battery=battery
  )
  print('UPDATE - Sensor {idx_temp} with values => {temperature}°C - {humidity}%'.format(
    idx_temp=idx_temp, temperature=temperature, humidity=humidity
  ))
  domoticzrequest(url)

def update_domoticz_switch(name: str, idx_switch: int, state: str):
  url = '{base_url}&param=switchlight&idx={idx_switch}&switchcmd={state}'.format(
    base_url=base_url, idx_switch=idx_switch, state=state
  )
  print('UPDATE - Switch {name} with idx {idx_switch} to state {state}'.format(name=name, idx_switch=idx_switch, state=state))
  domoticzrequest(url)