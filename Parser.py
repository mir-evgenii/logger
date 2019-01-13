# from SSH import SSH
import json, re

class Parser:

    def __init__(self):
        self.str = None
        self.str_parser = ''

        logger_parser_conf = json.load(open("logger_parser_conf.json"))
        self.find_fields = logger_parser_conf["Find_fields"]
        self.separators = logger_parser_conf["Separators"]
        self.limiters = logger_parser_conf["Limiters"]

    def parser(self, str=''):
        # str = 'Number: NUMBER = 1234'

        self.str_parser = self.date_parser(str)

        self.str = str.split()
        i_num = 0
        for i in self.str:
            i_num += 1

            time = self.time_parser(i)
            if time != 0:
                self.str_parser = self.str_parser + 'TIME - ' + time + '\n'

            gateway = self.gateway_parser(i)
            if gateway != 0:
                self.str_parser = self.str_parser + 'GATEWAY - ' + gateway + '\n'

            action = self.action_parser(i)
            if action != 0:
                self.str_parser = self.str_parser + 'ACTION - ' + action + '\n'

                # добавить множество из месяцев !!!!!!!!!!
            if i == 'Dec':
                self.str_parser = self.str_parser + '__________\n'

            i = i.upper()
            for f in self.find_fields:
                stop = False
                f = f.upper()
                if f in i:
                    for num_sep in range(2):
                        if stop:
                            break
                        if num_sep == 0:
                            for s in self.separators:
                                try:
                                    s_n = i.find(s)
                                    if not(s_n == -1) and not(i[s_n+1:] == ''):
                                        self.str_parser = self.str_parser + f
                                        self.str_parser = self.str_parser + " - " + i[s_n+1:] + "\n"
                                        stop = True
                                        break
                                    else:
                                        continue
                                except IndexError:
                                    continue
                        else:
                            for s in self.separators:
                                try:
                                    s_n = self.str[i_num].find(s)
                                    if not(s_n == -1) and i_num+1 < len(self.str):
                                        self.str_parser = self.str_parser + f
                                        self.str_parser = self.str_parser + " - " + self.str[i_num+1] + "\n"
                                        break
                                    else:
                                        continue
                                except IndexError:
                                    continue
                else:
                    continue

        return self.str_parser

    def date_parser(self, str=''):
        self.str = str.split()
        i_num = 0
        for i in self.str:
            i_num += 1
            remch = re.match(r'\d\d', i)
            if i == 'Dec':
                self.str_parser = self.str_parser + 'Dec '
            elif remch.group().isdigit() and len(remch.group()) == 2:
                self.str_parser = self.str_parser + i + '\n'
                break
            else:
                continue
        return self.str_parser

    def time_parser(self, str=''):
        remch = re.match(r'\d\d:\d\d:\d\d', str)
        if isinstance(remch, object) and not(remch is None):
            return remch.group()
        else:
            return 0

    def gateway_parser(self, str=''):
        remch = re.match(r'...#\d{3,4}#', str)
        if isinstance(remch, object) and not (remch is None):
            return remch.group()[4:-1]
        else:
            return 0

    def action_parser(self, str=''):
        for a in ['CHECK', 'PAY']:
            str = str.upper()
            s_n = str.find(a)
            if not(s_n == -1):
                return str[s_n:-1]
            else:
                continue
        return 0
