import os, winshell, wmi, time, configparser, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#----------------------------------------------------------------------------
class Send:


    def warning_close (self, limit, User_data):

        os.system("TASKKILL /F /IM nanominer.exe")
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(User_data[0],User_data[1])
        message = 'Температура рига превысилы поставленную метку в {}. Программа майнинга была отключена.'.format(limit)
        msg = MIMEMultipart()
        msg['From']= User_data[0]
        msg['To']=User_data[0]
        msg['Subject']="Превышен поставленый предел температуры."
        msg.attach(MIMEText(message, 'plain'))
        smtpObj.send_message(msg)
        print('Отправлен отчет на почту {}'.format(msg['To']))

    def time_to_send (self, now, maxim, User_data):

        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(User_data[0],User_data[1])
        message = 'Максимальная температура: {}'.format(maxim)
        msg = MIMEMultipart()
        msg['From']=User_data[0]
        msg['To']=User_data[0]
        msg['Subject']="Температура рига: {}.".format(now)
        msg.attach(MIMEText(message, 'plain'))
        smtpObj.send_message(msg)
        print('Отправлен отчет на почту {}'.format(msg['To']))

#-----------------------------------------------------------------------------

#------------------------------------dll reding-------------------------------
import clr # the pythonnet module.
clr.AddReference(os.getcwd() + r'\OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer

c = Computer()
c.GPUEnabled = True
c.Open()
#------------------------------------------------------------------------------

s = Send()

#--------------------------config-setting reading------------------------------
config = configparser.ConfigParser()
config.read('config.ini')

maxim = 0
limit = int(config.get('Timing','maximum_temperature'))
timer = int(config.get('Timing','Time_to_send'))

User_data = []
User_data.append(str(config.get('User' , 'Mail')))
User_data.append(str(config.get('User' , 'Password')))
#------------------------------------------------------------------------------

#---------------------get current time in global mode--------------------------
current_time = int(time.time())
#------------------------------------------------------------------------------

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


			if int(time.time()) - current_time >= timer:
				current_time = int(time.time())
				s.time_to_send(now, maxim, User_data)

			time.sleep(0.5)
			c.Hardware[0].Update()