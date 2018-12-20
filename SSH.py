import socket, paramiko, datetime
# from GUI import GUI
# from Parser import Parser


class SSH:

    def __init__(self, host, login, password, port, auth_type, key):

        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.data = None

        self.error = 0

        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if auth_type == 'password':
                self.client.connect(hostname=host, username=login, password=password, port=port)
            elif auth_type == 'key':
                self.client.connect(hostname=host, username=login, port=port, key_filename=key)
            else:
                self.error = 'Не верное значение типа авторизации!'
        except socket.gaierror:
            self.error = 'Не правильный хост!'
        except paramiko.ssh_exception.AuthenticationException:
            self.error = 'Не правильный пароль или имя пользователя!'
        except paramiko.ssh_exception.NoValidConnectionsError:
            self.error = 'Не правильный порт!'
        except paramiko.ssh_exception.SSHException:
            self.error = 'Не верный тип авторизации!'

    def grep(self, number='', file='', date=''):
        if len(number) == 1:
            if date == '':
                query = "grep '{0}' logs/{1}".format(number, file)
            else:
                if date == datetime.datetime.today().strftime("%Y%m%d"):
                    query = "grep '{0}' logs/{1}".format(number, file)
                else:
                    date = datetime.datetime.strptime(date, "%Y%m%d")
                    one_day = datetime.timedelta(1)
                    date = date + one_day
                    date = date.strftime("%Y%m%d")
                    if date == datetime.datetime.today().strftime("%Y%m%d"):
                        query = "grep '{0}' logs/{1}-{2}".format(number, file, date)
                    else:
                        query = "xzgrep '{0}' logs/{1}-{2}.xz".format(number, file, date)
            self.stdin, self.stdout, self.stderr = self.client.exec_command(query)
        elif len(number) > 1:
            for i in number:
                print(i)
            return "it work!"
        else:
            return 0
        self.data = self.stdout.read() + self.stderr.read()
        return self.data
