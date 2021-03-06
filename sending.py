import os, winshell, wmi, time, configparser, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



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

