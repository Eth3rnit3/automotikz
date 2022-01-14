import os, signal

PID_FILE = '/tmp/domoticz-auto-sensor.pid'

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

def start(process):
  write_pid_file()
  process()