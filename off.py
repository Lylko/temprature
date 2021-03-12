import os, winshell, wmi, time, configparser, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#----------------------------------------------------------------------------
class Send:

    def Sending_Mail (self, now, maxim, limit, User_data, mode):
        msg = MIMEMultipart()
        if mode == 0:
            os.system("TASKKILL /F /IM nanominer.exe")
            message = 'Температура рига превысилы поставленную метку в {}. Программа майнинга была отключена.'.format(limit)
            msg['Subject']="Превышен поставленый предел температуры."
            print('Температура будет проверена еще раз через 20 секунд.')
            time.sleep(20)
        else:
            message = 'Максимальная температура: {}'.format(maxim)
            msg['Subject']="Температура рига: {}.".format(now)

        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(User_data[0],User_data[1])
        msg['From']= User_data[0]
        msg['To']=User_data[0]
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
Maximum_temperature = 0

#------------------------config check------------------------------------------
while 1:
    config.read('config.ini')
    Temperature_limit = int(config.get('Timing','maximum_temperature'))
    timer = int(config.get('Timing','Time_to_send'))
    User_data = []
    User_data.append(str(config.get('User' , 'Mail')))
    User_data.append(str(config.get('User' , 'Password')))
    Dev_mode = int(config.get('User' , 'Developer_mode'))

    if (Temperature_limit<30 or Temperature_limit>120 or timer<60 or timer>86240) and Dev_mode == 0:
        print('Configure error. Please, check your settings. Process will be autorestarted after 20 sec.')
        time.sleep(20)
    else:
        break
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

            if Current_tempreture > Maximum_temperature:
                Maximum_temperature = Current_tempreture

            if Current_tempreture>Temperature_limit:
                s.Sending_Mail(Current_tempreture, Maximum_temperature, Temperature_limit, User_data, 0)

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
                                Temperature_data.append(Current_tempreture)
                            else:
                                Time_data.append('{}:{}:{}'.format(str(Hours).zfill(2), str(Minutes).zfill(2), str(Seconds).zfill(2)))
                                Temperature_data.append(Current_tempreture)


            if time.time() - current_time_limit >= timer:
                current_time_limit = time.time()
                s.Sending_Mail(Current_tempreture, Maximum_temperature, Temperature_limit, User_data, 1)

            time.sleep(0.5)
            c.Hardware[0].Update()