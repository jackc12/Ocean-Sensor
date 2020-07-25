import serial
import time
import datetime

class Sensor:
    def __init__(self, name):
        print('{} created'.format(name))
    def connect(self):
        try:
            self.ser = serial.Serial(port='/dev/cu.usbserial-1410', baudrate='9600', timeout=5)
            self.ser.flushInput()
        except:
            print('failed connect')    
    def do_sample(self):
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
            f.write('Conductivity: {} Temperature: {}\n'.format(cond_and_temp.split()[1], cond_and_temp.split()[3]))
    def close(self):
        self.ser.close()

oxygen = Sensor('oxygen')
oxygen.connect()
oxygen.do_sample()
oxygen.close()