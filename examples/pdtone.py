import os, socket, time, subprocess, atexit, tempfile

class PDTone():
  def __init__(self, pd_file=None):
    self.port = 3000
    self.tempfile = None
    if pd_file == None:
      self.tempfile, self.pd_file = tempfile.mkstemp()
      self.create_pd_file()
    else:
      self.pd_file = pd_file
    self.pid = None
    self.proc_pd = None

    atexit.register(self.stop_pd)

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.start_pd()
    self.connect()

  def start_pd(self):
    pdfile = os.path.join(os.getcwd(), self.pd_file)
    self.proc_pd = subprocess.Popen(['/usr/bin/pd', '-nogui', pdfile], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    pid = subprocess.check_output(['/bin/pidof','pd'], )
    time.sleep(0.5)
    self.pid = int(pid.split(' ')[0])
    print("Started PD with PID: " + str(pid))
  
  def connect(self):
    attempts = 10
    while attempts:
      print("Attempting to connect to PD")
      try:
        self.socket.connect(('127.0.0.1',self.port))
        print("Connected to PD")
        break
      except socket.error:
        time.sleep(0.5)
      attempts-=1

  def stop_pd(self):
    if self.proc_pd != None:
      print("Killing PD instance")
      self.proc_pd.terminate()
      self.proc_pd = None
      self.pid = None
    if self.tempfile != None:
      print("Removing temp file")
      os.close(self.tempfile)
      os.remove(self.pd_file)

  def send(self, cmd):
    self.socket.send(cmd + ';')

  def power_on(self):
    self.send('power 1')

  def power_off(self):
    self.send('power 0')
  
  def tone(self, f):
    self.send('tone ' + str(f))

  def note(self, f, duration):
    self.tone(f)
    self.power_on()
    time.sleep(duration)
    self.power_off()

  def create_pd_file(self):
    print("Populating temp PD file: " + self.pd_file)
    f = open(self.pd_file, 'w')
    f.write("#N canvas -1 43 1024 694 10;")
    f.write("#X obj 234 309 dac~;")
    f.write("#X obj 251 204 osc~ 440;")
    f.write("#X obj 572 145 netreceive " + str(self.port) + ";")
    f.write("#X obj 585 349 s tone;")
    f.write("#X obj 218 90 r tone;")
    f.write("#X obj 695 315 s volume;")
    f.write("#X obj 665 506 tgl 15 0 empty empty empty 17 7 0 10 -262144 -1 -1 0")
    f.write("300;")
    f.write("#X obj 618 220 route tone volume power;")
    f.write("#X obj 808 315 s power;")
    f.write("#X obj 655 454 r power;")
    f.write("#X msg 661 560 \; pd dsp \$1 \;;")
    f.write("#X connect 1 0 0 0;")
    f.write("#X connect 2 0 7 0;")
    f.write("#X connect 4 0 1 0;")
    f.write("#X connect 6 0 10 0;")
    f.write("#X connect 7 0 3 0;")
    f.write("#X connect 7 1 5 0;")
    f.write("#X connect 7 2 8 0;")
    f.write("#X connect 9 0 6 0;")
    f.close()
