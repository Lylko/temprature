import os, winshell, wmi, time, configparser, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import clr # the pythonnet module.
clr.AddReference(os.getcwd() + r'\OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer

c = Computer()
c.GPUEnabled = True
c.Open()

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
					os.system("TASKKILL /F /IM nanominer.exe")
				 #------------------------------------------------message----------------------------------------------
					smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
					smtpObj.starttls()
					smtpObj.login('unknownyunicode@gmail.com','QWSAqwsa7907')
					message = 'Температура рига превысилы поставленную метку в {}. Программа майнинга была отключена.'.format(limit)
					msg = MIMEMultipart()       
					msg['From']='unknownyunicode@gmail.com'
					msg['To']='androsov406@gmail.com'
					msg['Subject']="Превышен поставленый предел температуры."
					msg.attach(MIMEText(message, 'plain'))
					smtpObj.send_message(msg)
					print('Отправлен отчет на почту {}'.format(msg['To']))
				 #------------------------------------------------------------------------------------------------------
				except:
					print('Была превышена температура')
					pass
			timer -= 3
			if timer <=0:
				smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
				smtpObj.starttls()
				smtpObj.login('unknownyunicode@gmail.com','QWSAqwsa7907')
				message = 'Максимальная температура: {}'.format(maxim)					
				msg = MIMEMultipart()       
				msg['From']='unknownyunicode@gmail.com'
				msg['To']='androsov406@gmail.com'
				msg['Subject']="Температура рига: {}.".format(now)
				msg.attach(MIMEText(message, 'plain'))
				smtpObj.send_message(msg)
				print('Отправлен отчет на почту {}'.format(msg['To']))
				timer = int(config.get('Timing','Time_to_send'))
			time.sleep(3)
			c.Hardware[0].Update()