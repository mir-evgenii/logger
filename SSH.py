import socket, paramiko
# from GUI import GUI
# from Parser import Parser


class SSH:

    def __init__(self, host, user, password, port):

        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.data = None

        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=host, username=user, password=password, port=port)
        except paramiko.ssh_exception.AuthenticationException:
            self.error = 'Не правильный пароль!'
        except paramiko.ssh_exception.NoValidConnectionsError:
            self.error = 'Не правильный порт!'
        except NameError:
            self.error = 'Не правильное имя пользователя!'
        except socket.gaierror:
            self.error = 'Не правильный хост'

    def grep(self, number='', file='', time=''):
        self.stdin, self.stdout, self.stderr = self.client.exec_command(
            "grep '{0}' logs/{1}.{2}".format(number, file, time))
        self.data = self.stdout.read() + self.stderr.read()
        return self.data
