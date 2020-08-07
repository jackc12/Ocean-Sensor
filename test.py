class OxygenSensor():
	def do_sample(self, data_names=['Temp'], n_samples=6, interval=5, wait_for=10):
		self.n_samples = n_samples
		self.written_samples = 0
		self.wait_for = wait_for
		sat_and_temp = 'empty!'
		self.e = 'error'
		end_at = time.time() + self.wait_for
		failed_conductivity = True
		while time.time() <= end_at and self.written_samples < self.n_samples:
			while [data_name not in sat_and_temp for data_name in data_names]:
		# 		try:
		# 			self.ser.flushInput()
		# 			self.ser.write(bytes('do sample','utf-8'))
		# 			self.ser.write(bytes('\r\n','utf-8'))
		# 			self.ser_bytes = self.ser.readline()
		# 			sat_and_temp = ' '.join(self.ser_bytes.decode('utf-8').strip().split()[-5::2]) + '\n'
		# 			failed_conductivity = False
		# 			break
		# 		except Exception as e:
		# 			self.e = e
		# 			failed_conductivity = True
		# 	if failed_conductivity:
		# 		write_file(f_name='error.txt', msg='{} {} at {}\n'.format('error in do_sample:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		# 		print('wrote to error.txt! error in Conductivity.get_sample!')
		# 		quit()
		# 	else:
		# 		if len(sat_and_temp.split()) == 3:
		# 			write_file(f_name='oxygen.txt', msg='{} Oxygen: {} Saturation: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), sat_and_temp.split()[0], sat_and_temp.split()[1], sat_and_temp.split()[2]))
		# 			print('{} Oxygen: {} Saturation: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), sat_and_temp.split()[0], sat_and_temp.split()[1], sat_and_temp.split()[2]))
		# 			self.written_samples += 1
		# 	time.sleep(interval)
		# time.sleep(2)

o = OxygenSensor()
o.get_sample(['Temp', 'slatt'])