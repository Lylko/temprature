from mysql.connector import connect, Error
import os, winshell, wmi, time, configparser, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import colorama
from colorama import Fore, Style
import os.path

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


class config_class:

    def create_config_file():
        if os.path.exists('settings/') == True:
            pass
        else:
            os.mkdir("settings")
        init = colorama.init()
        print(Fore.RED + 'Файл настройки не найден. Создаем новый файл. Пожалуйста, пройдите установку.')
        config = configparser.ConfigParser()
        config.add_section('Timing')

        print(Style.RESET_ALL)

        while 1:
            enter = str(input('Установите максимальную температуру вашего рига (минимум - 40, максимум - 120): '))
            if enter.isdigit() == True:
                if int(enter) >= 40 and int(enter) <=120:
                    config.set('Timing', 'maximum_temperature', enter)
                    print(Fore.GREEN + 'Параметр принят.')
                    print(Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED + 'Значение не удовлетворяет параметрам. Попробуйте еще раз (вводить значения надо без пробелов).')
                    print(Style.RESET_ALL)
            else:
                print(Fore.RED + 'Значение не удовлетворяет параметрам. Попробуйте еще раз (вводить значения надо без пробелов).')
                print(Style.RESET_ALL)

        while 1:
            enter = str(input('Установите как часто будут высылаться уведомления на почту (минимум - 60, максимум - 86240): '))
            if enter.isdigit() == True:
                if int(enter) >= 60 and int(enter)<= 86240:
                    config.set('Timing', 'Time_to_send', enter)
                    print(Fore.GREEN + 'Параметр принят.')
                    print(Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED + 'Значение не удовлетворяет параметрам. Попробуйте еще раз (вводить значения надо без пробелов).')
                    print(Style.RESET_ALL)
            else:
                print(Fore.RED + 'Значение не удовлетворяет параметрам. Попробуйте еще раз (вводить значения надо без пробелов).')
                print(Style.RESET_ALL)
    
        config.add_section('User')

        while 1:
            mail = str(input('Введите mail id вашей почты: '))
            config.set('User', 'Mail', mail )
            passw = str(input('Введите пароль от вашей почты: '))
            config.set('User', 'Password', passw)
            try:
                print(Fore.GREEN + 'Попытка авторизации...')
                smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
                smtpObj.starttls()
                smtpObj.login(mail,passw)
                print(Fore.GREEN + 'Авторизация успешна.')
                break
            except:
                print(Fore.RED + 'Пароль или почта были введены неправильно. Попробуйте еще раз.')
                print(Style.RESET_ALL)
        
        config.set('User', 'Developer_mode', '0')

        with open('settings/config.ini', "w") as config_file:
            config.write(config_file)

        print(Fore.GREEN + 'Настройка произведена успешно!')
        print(Style.RESET_ALL)




