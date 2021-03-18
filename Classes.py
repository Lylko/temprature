from mysql.connector import connect, Error
import os, winshell, wmi, time, configparser, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import colorama
from colorama import Fore, Style

class MySQL:
    #status - включен/выключен контроль
    #command - номер команды: 0 - отсутствие комманды, 1 - выключение майнера.
    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""
        try:
            self.connection = connect(host='bzmtecj9fjfdtjr6klwk-mysql.services.clever-cloud.com', user='uqp9pfabsy8y9zyz', password='6rYvOA0kNm4cSYP2S1TA', database = 'bzmtecj9fjfdtjr6klwk')
        except:
            print('Connection failed')
        self.cursor = self.connection.cursor()


    def check_command(self,user_id):
        """Проверяем значение параметра command"""
        self.cursor.execute('SELECT * FROM `test` WHERE `user_id` = {}'.format(user_id))
        return (self.cursor.fetchall())

    def command_done(self, user_id, command = 0):
        return self.cursor.execute('UPDATE `test` SET `command` = {} WHERE `user_id` = {}'.format(command, user_id))

    def commit(self):
        self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


class Send:
    # mode: 0 - превышение температуры, 1 - команда извне, остальное - отсылка по таймеру

    def Sending_Mail (self, now, maxim, limit, User_data, mode):
        colorama.init()
        msg = MIMEMultipart()
        if mode == 0:
            os.system("TASKKILL /F /IM nanominer.exe")
            message = 'Температура рига превысилы поставленную метку в {}. Программа майнинга была отключена.'.format(limit)
            msg['Subject']="Превышен поставленый предел температуры."
            print('Температура будет проверена еще раз через 20 секунд.')
            time.sleep(20)
        elif mode == 1:
            os.system("TASKKILL /F /IM nanominer.exe")
            message = 'Программа майнинга была отключена по запросу из телеграмм-бота, максимальная температура за все время работы составила: {}'.format(maxim)
            msg['Subject']="Отключение майнера."
        else:
            message = 'Максимальная температура: {}'.format(maxim)
            msg['Subject']="Температура рига: {}.".format(now)

        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login(User_data[0],User_data[1])
            msg['From']= User_data[0]
            msg['To']=User_data[0]
            msg.attach(MIMEText(message, 'plain'))
            smtpObj.send_message(msg)
            print(Fore.GREEN + 'Отправлен отчет на почту {}'.format(msg['To']))
        except:
            print(Fore.RED + "Отправка не удалась.")
            pass
        print(Style.RESET_ALL)