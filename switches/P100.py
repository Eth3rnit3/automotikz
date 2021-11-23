#!/usr/bin/env python

import yaml
from PyP100 import PyP100
import sys, os

user          = os.getenv('PATO_USER')
password      = os.getenv('PATO_PASSWORD')

def load_switches():
  with open('P100.yaml') as f:
    return yaml.safe_load(f)['switches']

def find_switch(name):
  for switch in load_switches():
    if switch['name'].lower() == name.lower():
      return switch

def run(switch_name, action):
  swt = find_switch(switch_name)
  if swt:
    p100 = PyP100.P100(swt['ip'], user, password)
    p100.handshake()
    p100.login()
    print('Connexion to {name} successful'.format(name=switch_name))

    if action.lower() == 'on':
      p100.turnOn()
      print('Switch {name} was turned ON'.format(name=switch_name))
    if action.lower() == 'off':
      p100.turnOff()
      print('Switch {name} was turned OFF'.format(name=switch_name))
  else:
    print('Switch {name} was not found int the switches list'.format(name=switch_name))

run(sys.argv[1], sys.argv[2])

# Usage
# python3 ./P100.py Ventilateur on
# python3 ./P100.py Chauffage off