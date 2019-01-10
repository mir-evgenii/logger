import socket, paramiko, datetime
# from GUI import GUI
from Parser import Parser


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

    def grep(self, number='', file='', date='', path=''):
        if isinstance(number, str):
            query = self.query(number, file, date, path)
        elif isinstance(number, list):
            query = self.query(number[0], file, date)
            for i in number[1:]:
                query = query + " | grep '{0}'".format(i)
        else:
            return 0  # должен вернуть ошибку?
        self.stdin, self.stdout, self.stderr = self.client.exec_command(query)
        self.data = self.stdout.read() + self.stderr.read()
        parser = Parser()
        self.data = parser.parser(self.data.decode("utf-8"))
        return self.data

    def query(self, number='', file='', date='', path=''):
        if date == '':
            query = "grep '{0}' {1}/{2}".format(number, path, file)
        else:
            if date == datetime.datetime.today().strftime("%Y%m%d"):
                query = "grep '{0}' {1}/{2}".format(number, path, file)
            else:
                date = datetime.datetime.strptime(date, "%Y%m%d")
                one_day = datetime.timedelta(1)
                date = date + one_day
                date = date.strftime("%Y%m%d")
                if date == datetime.datetime.today().strftime("%Y%m%d"):
                    query = "grep '{0}' {1}/{2}-{3}".format(number, path, file, date)
                else:
                    query = "xzgrep -a '{0}' {1}/{2}-{3}.xz".format(number, path, file, date)
        return query
