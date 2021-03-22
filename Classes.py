import os
import winshell
import wmi
import time
import configparser
import smtplib
import colorama
import os.path
import json
from mysql.connector import connect, Error
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from colorama import Fore, Style

class Global:
    def __init__(self):

        try:
            config = configparser.ConfigParser()
            config.read('settings/config.ini')
            lang = config.get('User', 'lang')
            open('{}.json'.format(lang, mode = "r", encoding = "UTF-8"))
        except:
            lang = 'en'
        filename = "language/{}.json".format(lang)
        myfile =  open(filename, mode = "r", encoding = "UTF-8")
        self.json_data = json.load(myfile)

    def language(self):
        return (self.json_data)


class MySQL(Global):
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


class Send(Global):
    # mode: 0 - превышение температуры, 1 - команда извне, остальное - отсылка по таймеру

    def Sending_Mail (self, now, maxim, limit, User_data, mode):
        colorama.init()
        msg = MIMEMultipart()
        if mode == 0:
            os.system("TASKKILL /F /IM nanominer.exe")
            message = 'Температура рига превысилы поставленную метку в {}. Программа майнинга была отключена.'.format(limit)
            msg['Subject']="Превышен поставленый предел температуры."
            print(self.json_data['Temperaute will be rechecked after 20 seconds.'])
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
            print(Fore.GREEN + str(self.json_data["Sent to {}"]).format(msg['To']))
        except:
            print(Fore.RED + self.json_data["Sending failed."])
            pass
        print(Style.RESET_ALL)


class config_class(Global):

    def create_config_file(self):
        if os.path.exists('settings/') == True:
            pass
        else:
            os.mkdir("settings")
        init = colorama.init()
        print(Fore.RED + self.json_data["The configuration file was not found. Creating a new file. Please go through the installation."])
        config = configparser.ConfigParser()
        config.add_section('Timing')

        print(Style.RESET_ALL)

        config.add_section('User')

        while 1:
            enter = input(self.json_data['Set language (en/ru): '])
            if enter == "en" or enter == "ru":
                config.set('User', 'lang', enter)
                break
            else:
                print (Fore.RED + self.json_data["Please, try again."])
                print(Style.RESET_ALL)


        while 1: 
            enter = str(input(self.json_data['Set the maximum temperature for your rig (minimum - 40, maximum - 120): ']))
            if enter.isdigit() == True:
                if int(enter) >= 40 and int(enter) <=120:
                    config.set('Timing', 'maximum_temperature', enter)
                    print(Fore.GREEN + self.json_data["The parameter is accepted. "])
                    print(Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED + self.json_data["The value does not match the parameters. Try again (you must enter values without spaces). "])
                    print(Style.RESET_ALL)
            else:
                print(Fore.RED + self.json_data["The value does not match the parameters. Try again (you must enter values without spaces). "])
                print(Style.RESET_ALL)

        while 1:
            enter = str(input(self.json_data["Set how often notifications will be sent to the mail (minimum - 60, maximum - 86240): "]))
            if enter.isdigit() == True:
                if int(enter) >= 60 and int(enter)<= 86240:
                    config.set('Timing', 'Time_to_send', enter)
                    print(Fore.GREEN + self.json_data["The parameter is accepted. "])
                    print(Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED + self.json_data["The value does not match the parameters. Try again (you must enter values without spaces). "])
                    print(Style.RESET_ALL)
            else:
                print(Fore.RED + self.json_data["The value does not match the parameters. Try again (you must enter values without spaces). "])
                print(Style.RESET_ALL)
    

        while 1:
            mail = str(input(self.json_data["Enter your mail id: "]))
            config.set('User', 'Mail', mail )
            passw = str(input(self.json_data["Enter password from your mail id: "]))
            config.set('User', 'Password', passw)
            try:
                print(Fore.GREEN + self.json_data["Attempting to log in ... "])
                smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
                smtpObj.starttls()
                smtpObj.login(mail,passw)
                print(Fore.GREEN + self.json_data["Successful."])
                break
            except:
                print(Fore.RED + self.json_data["The password or mail was entered incorrectly. Try again. "])
                print(Style.RESET_ALL)
        
        config.set('User', 'Developer_mode', '0')

        with open('settings/config.ini', "w") as config_file:
            config.write(config_file)

        print(Fore.GREEN + self.json_data["The setup was successful "])
        print(Style.RESET_ALL)