import os, winshell, wmi, time, configparser, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sending import Send

import clr # the pythonnet module.
clr.AddReference(os.getcwd() + r'\OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer

c = Computer()
c.GPUEnabled = True
c.Open()

s = Send()

config = configparser.ConfigParser()
config.read('config.ini')

maxim = 0
limit = int(config.get('Timing','maximum_temperature'))
timer = int(config.get('Timing','Time_to_send'))

while True:
	for a in range(0, len(c.Hardware[0].Sensors)):
		if "/nvidiagpu/0/temperature" in str(c.Hardware[0].Sensors[a].Identifier):

			now = c.Hardware[0].Sensors[a].get_Value()
			print(now)

			if now > maxim:
				maxim = now

			if now>limit:
				try:
					s.warning_close(limit)
				except:
					print('Была превышена температура')
					pass


			timer -= 3
			if timer <=0:
				s.time_to_send(now, maxim)
				timer = int(config.get('Timing','Time_to_send'))

			time.sleep(3)
			c.Hardware[0].Update()