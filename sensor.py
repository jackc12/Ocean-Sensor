import serial
import time
import datetime

class Sensor:
    def __init__(self, name):
        print('instance of {} created'.format(name))
    def connect(self, port, baudrate, timeout):
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            self.ser.flushInput()
            return True
        except:
            print('failed connect') 
            return False    
    def do_sample(self, n_samples, interval):
        for _ in range(n_samples):
            cond_and_temp = ''
            while 'Conductivity:' not in cond_and_temp and 'Temperature:' not in cond_and_temp:
                try:
                    self.ser.write(bytes('do sample','utf-8'))
                    self.ser.write(bytes('\r\n','utf-8'))
                    self.ser_bytes = self.ser.readline()
                    cond_and_temp = ' '.join(self.ser_bytes[:-2].decode('utf-8').strip().split()[-4:]) + '\n'
                except:
                    print('failed do_sample')
            with open('cond_and_temp.txt', 'a') as f:
                f.write('{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), cond_and_temp.split()[1], cond_and_temp.split()[3]))
            time.sleep(interval)
    def close(self):
        try:
            self.ser.close()
            return True
        except:
            print('failed close')
            return False

oxygen = Sensor('oxygen')
oxygen_connected, oxygen_closed = False, False
while not oxygen_connected:
    oxygen_connected = oxygen.connect(port='/dev/cu.usbserial-1410', baudrate='9600', timeout=5)
oxygen.do_sample(n_samples=6, interval=10)
while not oxygen_closed:
    oxygen_closed = oxygen.close()