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

#--------------------------config-settings reading------------------------------

config = configparser.ConfigParser()
config.read('config.ini')
maxim = 0

#------------------------config check------------------------------------------
while 1:
    config.read('config.ini')
    limit = int(config.get('Timing','maximum_temperature'))
    timer = int(config.get('Timing','Time_to_send'))
    User_data = []
    User_data.append(str(config.get('User' , 'Mail')))
    User_data.append(str(config.get('User' , 'Password')))
    Dev_mode = int(config.get('User' , 'Developer_mode'))

    if (limit<40 or limit>120 or timer<60 or timer>86240) and Dev_mode == 0:
        print('Configure error. Please, check your settings. Process will be autorestarted after 20 sec.')
        time.sleep(20)
    else:
        break
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


#---------------------get current time in global mode--------------------------
current_time = current_time_limit = time.time()
#------------------------------------------------------------------------------


#--------------------------------Work with time--------------------------------
Hours = Minutes = Seconds = 0
Time_data = ['{}:{}:{}'.format(str(Hours).zfill(2), str(Minutes).zfill(2), str(Seconds).zfill(2))]
Temperature_data = [0]
#------------------------------------------------------------------------------

while True:
    for a in range(0, len(c.Hardware[0].Sensors)):
        if "/nvidiagpu/0/temperature" in str(c.Hardware[0].Sensors[a].Identifier):

            Current_tempreture = c.Hardware[0].Sensors[a].get_Value()
            print(Current_tempreture)

            if Current_tempreture > maxim:
                maxim = Current_tempreture

            if Current_tempreture>limit:
                try:
                    s.warning_close(limit)
                except:
                    print('Была превышена температура')
                    pass

            if time.time()-current_time >=30:
                            current_time = time.time()
                            Seconds += 30
                            if Seconds == 60:
                                Minutes+=1
                                Seconds = 0
                            if Minutes == 60:
                                Hours += 1
                                Minutes = 0
                            if len(Time_data)>5:
                                del(Time_data[0])
                                Time_data.append('{}:{}:{}'.format(str(Hours).zfill(2), str(Minutes).zfill(2), str(Seconds).zfill(2)))
                            else:
                                Time_data.append('{}:{}:{}'.format(str(Hours).zfill(2), str(Minutes).zfill(2), str(Seconds).zfill(2)))


            if time.time() - current_time_limit >= timer:
                current_time_limit = time.time()
                s.time_to_send(Current_tempreture, maxim, User_data)
            time.sleep(0.5)
            c.Hardware[0].Update()