import serial, time, datetime

def write_file(f_name='error.txt', msg='you didn\'t pass any arguments to write_file'):
    with open(f_name, 'a') as f:
        f.write(msg)

class Sensor:
    def __init__(self, port='/dev/cu.usbserial-1410', baudrate='9600', timeout=5, wait_for=10):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.wait_for = wait_for
    def connect(self):
        end_at = time.time() + self.wait_for
        failed_connection = True
        while time.time() <= end_at:
            try:
                self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
                self.ser.flushInput()
                failed_connection = False
            except Exception as e:
                failed_connection = True
                self.e = e
        if failed_connection:
            write_file(f_name='error.txt', msg='{} {} at {}'.format('error in connect:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            print('wrote\n\n{}\n\nto error.txt'.format('error in connect:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            quit()
    def disconnect(self):
        end_at = time.time() + self.wait_for
        failed_disconnect = True
        while time.time() <= end_at:
            try:
                self.ser.close()
                failed_disconnect = False
            except Exception as e:
                failed_disconnect = True
                self.e = e
        if failed_disconnect:
            write_file(f_name='error.txt', msg='{} {} at {}'.format('error in disconnect:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            print('wrote\n\n{}\n\nto error.txt'.format('error in disconnect:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            quit()

class ConductivitySensor(Sensor):
    def do_sample(self, n_samples=6, interval=10):
        for _ in range(n_samples):
            cond_and_temp = ''
            end_at = time.time() + self.wait_for
            failed_conductivity = True
            while time.time() <= end_at:
                while 'Conductivity:' not in cond_and_temp and 'Temperature:' not in cond_and_temp:
                    try:
                        self.ser.write(bytes('do sample','utf-8'))
                        self.ser.write(bytes('\r\n','utf-8'))
                        self.ser_bytes = self.ser.readline()
                        cond_and_temp = ' '.join(self.ser_bytes[:-2].decode('utf-8').strip().split()[-4:]) + '\n'
                        failed_conductivity = False
                    except Exception as e:
                        failed_conductivity = True
                        self.e = e
                if failed_conductivity:
                    write_file(f_name='error.txt', msg='{} {} at {}'.format('error in do_sample:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
                    print('wrote\n\n{}\n\nto error.txt'.format('error in do_sample:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
                    quit()
                else:
                    write_file(f_name='cond_and_temp.txt', msg='{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), cond_and_temp.split()[1], cond_and_temp.split()[3]))
                    print('wrote\n\n{}\n\nto cond_and_temp.txt'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), cond_and_temp.split()[1], cond_and_temp.split()[3]))
                time.sleep(interval)

class OxygenSensor(Sensor):
    def other_command(self):
        print('I will do the command for the oxygen sensor')


conductivity = ConductivitySensor(port='/dev/cu.usbserial-1410', baudrate='9600', timeout=5, wait_for=10)
conductivity.connect()
conductivity.do_sample(n_samples=6, interval=10)

conductivity.disconnect()
