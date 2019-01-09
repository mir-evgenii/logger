# from SSH import SSH
import json

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
        self.str = str.split()
        i_num = 0
        for i in self.str:
            i_num += 1
            i = i.upper()
            for f in self.find_fields:
                f = f.upper()
                if f in i:
                    for num_sep in range(2):
                        if num_sep == 0:
                            for s in self.separators:
                                try:
                                    s_n = i.find(s)
                                    if not(s_n == -1) and not(i[s_n+1:] == ''):
                                        self.str_parser = self.str_parser + f
                                        self.str_parser = self.str_parser + " - " + i[s_n+1:] + "\n"
                                        break
                                    else:
                                        continue
                                except IndexError:
                                    continue
                        else:
                            for s in self.separators:
                                try:
                                    s_n = self.str[i_num+1].find(s)
                                    if not(s_n == -1) and i_num+2 < len(self.str):
                                        self.str_parser = self.str_parser + f
                                        self.str_parser = self.str_parser + " - " + self.str[i_num+2] + "\n"
                                        break
                                    else:
                                        continue
                                except IndexError:
                                    continue
                else:
                    continue

        return self.str_parser
