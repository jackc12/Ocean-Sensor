import serial, time, datetime

def write_file(f_name='error.txt', msg='you didn\'t pass any arguments to write_file'):
	with open(f_name, 'a') as f:
		f.write(msg)

class Sensor:
	def __init__(self, port='/dev/ttyUSB0', baudrate='9600', timeout=5, wait_for=10):
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.wait_for = wait_for
	def connect(self, wait_for=5):
		print('YAH')
		self.wait_for = wait_for
		end_at = time.time() + self.wait_for
		failed_connection = True
		while time.time() <= end_at:
		    try:
		        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
		        self.ser.flushInput()
		        failed_connection = False
		        break
		    except Exception as e:
		        failed_connection = True
		        self.e = e
		if failed_connection:
			write_file(f_name='error.txt', msg='{} {} at {}'.format('error in connect:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			print('wrote to error.txt! error in connect!')
			quit()
	def disconnect(self, wait_for=5):
		self.wait_for = wait_for
		self.ser.flushInput()
		end_at = time.time() + self.wait_for
		failed_disconnect = True
		while time.time() <= end_at:
			try:
				self.ser.close()
				failed_disconnect = False
				break
			except Exception as e:
				failed_disconnect = True
				self.e = e
		if failed_disconnect:
			write_file(f_name='error.txt', msg='{} {} at {}'.format(self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			print('wrote to error.txt! error in disconnect!')
			quit()

class ConductivitySensor(Sensor):
	def do_sample(self, n_samples=6, interval=5, wait_for=10):
		self.n_samples = n_samples
		self.written_samples = 0
		self.wait_for = wait_for
		cond_and_temp = 'empty!'
		self.e = 'len(cond_and_temp) < 4'
		end_at = time.time() + self.wait_for
		failed_conductivity = True
		while time.time() <= end_at and self.written_samples < self.n_samples:
			while 'Conductivity:' not in cond_and_temp and 'Temperature:' not in cond_and_temp:
				try:
					self.ser.flushInput()
					self.ser.write(bytes('do sample','utf-8'))
					self.ser.write(bytes('\r\n','utf-8'))
					self.ser_bytes = self.ser.readline()
					cond_and_temp = ' '.join(self.ser_bytes[:-2].decode('utf-8').strip().split()[-4:]) + '\n'
					failed_conductivity = False
					break
				except Exception as e:
					failed_conductivity = True
					self.e = e
			if failed_conductivity:
				write_file(f_name='error.txt', msg='{} {} at {}\n'.format('error in do_sample:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
				print('wrote to error.txt! error in Conductivity.get_sample!')
				quit()
			else:
				if len(cond_and_temp.split()) >= 4:
					write_file(f_name='cond_and_temp.txt', msg='{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), cond_and_temp.split()[1], cond_and_temp.split()[3]))
					print('{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), cond_and_temp.split()[1], cond_and_temp.split()[3]))
					self.written_samples += 1
			time.sleep(interval)

class OxygenSensor(Sensor):
	def do_sample(self, n_samples=6, interval=5, wait_for=10):
		print('OK')
		self.n_samples = n_samples
		self.written_samples = 0
		self.wait_for = wait_for
		sat_and_temp = 'empty!'
		self.e = 'len(sat_and_temp) < 4'
		end_at = time.time() + self.wait_for
		failed_conductivity = True
		while time.time() <= end_at and self.written_samples < self.n_samples:
			while 'Oxygen:' not in sat_and_temp and 'Saturation:' not in sat_and_temp and 'Temperature:' not in sat_and_temp:
				try:
					self.ser.flushInput()
					self.ser.write(bytes('do sample','utf-8'))
					self.ser.write(bytes('\r\n','utf-8'))
					self.ser_bytes = self.ser.readline()
					sat_and_temp = ' '.join(self.ser_bytes[:-2].decode('utf-8').strip().split()[-4:]) + '\n'
					failed_conductivity = False
					break
				except Exception as e:
					failed_conductivity = True
					self.e = e
			if failed_conductivity:
				write_file(f_name='error.txt', msg='{} {} at {}\n'.format('error in do_sample:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
				print('wrote to error.txt! error in Conductivity.get_sample!')
				quit()
			else:
				if len(sat_and_temp.split()) >= 4:
					print()
					write_file(f_name='cond_and_temp.txt', msg='{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), sat_and_temp.split()[1], sat_and_temp.split()[3]))
					print('{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), sat_and_temp.split()[1], sat_and_temp.split()[3]))
					self.written_samples += 1
			time.sleep(interval)


# conductivity = ConductivitySensor(port='/dev/ttyUSB0', baudrate='9600', timeout=5, wait_for=5)
# conductivity.connect(wait_for=5)
# conductivity.do_sample(n_samples=6, interval=3, wait_for=40)
# conductivity.disconnect(wait_for=5)

oxygen = OxygenSensor(port='/dev/ttyUSB0', baudrate='9600', timeout=5, wait_for=5)
oxygen.connect(wait_for=5)
oxygen.do_sample(n_samples=6, interval=3, wait_for=40)
oxygen.disconnect(wait_for=5)
