import os, winshell, wmi, time, configparser, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class Send:

    def warning_close (self, limit):

        os.system("TASKKILL /F /IM nanominer.exe")
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

    def time_to_send (self, now, maxim):

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

