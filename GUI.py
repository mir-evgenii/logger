import tkinter
import tkinter.messagebox
from typing import List
import json

from SSH import SSH


class GUI:

    def __init__(self):
        self.password = None
        self.host = None
        self.find_number = [None, ]
        self.find_date = None
        self.find_text_add = []
        self.ssh = None
        self.result = None
        self.win = None
        self.btn_del_ent = None
        self.btn_frame = None
        self.ent_frame = None
        self.find_number_frame = None
        self.find_date_frame = None
        self.find_file_frame = None
        self.file = None
        self.files = None

        logger_conf = json.load(open("logger_conf.json"))
        self.auth_type = logger_conf["Auth_type"]
        self.login = logger_conf["Login"]
        self.port = logger_conf["Port"]
        self.key = logger_conf["SSH_keyFile"]
        self.hosts = logger_conf["Hosts"]
        self.files = logger_conf["Files"]
        self.files_path = logger_conf["Files_path"]

        self.root = tkinter.Tk()
        self.root.title("Logger")
        self.auth()
        self.root.mainloop()

    def connect(self, event):
        password = self.password.get()
        host = self.host.get(self.host.curselection())
        self.ssh = SSH(host, self.login, password, self.port, self.auth_type, self.key)
        if self.ssh.error != 0:
            tkinter.messagebox.showerror("Ошибка!", self.ssh.error)
        else:
            self.main_window(host)

    def auth(self):
        password_text = tkinter.Label(self.root, text="Введите пароль", font="Arial 11")  # строка текста
        self.password = tkinter.Entry(self.root, width=20, bd=3, show='*')
        self.password.focus_set()

        btn = tkinter.Button(self.root, text="Войти")
        btn.bind("<Button-1>", self.connect)  # связь кнопки и функции
        self.root.bind("<Return>", self.connect)

        self.host = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, height=4)
        for i in self.hosts:
            self.host.insert(tkinter.END, i)

        if self.auth_type == 'password':
            password_text.pack(padx=5, pady=5)
            self.password.pack()
        self.host.pack(padx=10, pady=10)
        btn.pack(padx=10, pady=10)

    def main_window(self, title):
        self.win = tkinter.Toplevel(self.root)
        self.ent_frame = tkinter.Frame(self.win)
        self.btn_frame = tkinter.Frame(self.win)
        self.find_date_frame = tkinter.Frame(self.ent_frame)
        self.find_number_frame = tkinter.Frame(self.ent_frame)
        self.find_file_frame = tkinter.Frame(self.ent_frame)
        self.win.title(title)
        self.win.minsize(width=400, height=200)
        text = tkinter.Label(self.win, text="Искать", font="Arial 9")

        find_file_text = tkinter.Label(self.find_file_frame, text="Файл", font="Arial 9")
        self.file = tkinter.Listbox(self.find_file_frame, selectmode=tkinter.SINGLE, height=3)
        for i in self.files:
            self.file.insert(tkinter.END, i)

        find_number_text = tkinter.Label(self.find_number_frame, text="Критерий поиска", font="Arial 9")
        self.find_number[0] = tkinter.Entry(self.find_number_frame, width=20, bd=3)
        self.find_number[0].focus_set()
        find_date_text = tkinter.Label(self.find_date_frame, text="Дата", font="Arial 9")
        self.find_date = tkinter.Entry(self.find_date_frame, width=20, bd=3)
        btn = tkinter.Button(self.btn_frame, text="Найти")
        btn.bind("<Button-1>", self.grep)
        self.win.bind("<Return>", self.grep)
        self.result = tkinter.Label(self.win, text="Результат поиска", font="Arial 9")
        btn_add_ent = tkinter.Button(self.btn_frame, text="Добавить критерий поиска")
        btn_add_ent.bind("<Button-1>", self.add_ent)

        text.pack(padx=5, pady=5)
        self.find_file_frame.pack(side=tkinter.LEFT)
        find_file_text.pack()
        self.file.pack()
        self.find_date_frame.pack(side=tkinter.LEFT)
        find_date_text.pack()
        self.find_number_frame.pack(side=tkinter.LEFT)
        find_number_text.pack()
        self.find_date.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.find_number[0].pack(side=tkinter.LEFT, padx=5, pady=5)
        self.ent_frame.pack()
        self.btn_frame.pack()
        btn.pack(side=tkinter.LEFT, padx=5, pady=5)
        btn_add_ent.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.result.pack(padx=5, pady=5)

    def grep(self, event):
        date = self.find_date.get()

        if date == '':
            pass
        elif not(date.isdigit()):
            tkinter.messagebox.showerror("Ошибка!", "В поле дата нужно ввести дату в формате: ГГГГММДД")

        if len(self.find_number) == 1:
            number = self.find_number[0].get()
        else:
            number = []
            for i in self.find_number:
                number.append(i.get())
        file = self.file.get(self.file.curselection())
        result = self.ssh.grep(number, file, date, self.files_path)
        self.result.pack_forget()
        self.result = tkinter.Label(self.win, text=result, font="Arial 9")
        self.result.pack(padx=5, pady=5)

    def add_ent(self, event):
        self.find_number.append(tkinter.Entry(self.find_number_frame, width=20, bd=3))
        self.find_text_add.append(self.find_number[-1])
        for i in self.find_text_add:
            i.pack(side=tkinter.LEFT, padx=5, pady=5)
        if len(self.find_text_add) == 1:
            self.btn_del_ent = tkinter.Button(self.btn_frame, text="Удалить критерий поиска")
            self.btn_del_ent.bind("<Button-1>", self.del_ent)
            self.btn_del_ent.pack(side=tkinter.LEFT, padx=5, pady=5)

    def del_ent(self, event):
        self.find_text_add[-1].pack_forget()
        del(self.find_text_add[-1])
        del(self.find_number[-1])
        if len(self.find_text_add) < 1:
            self.btn_del_ent.pack_forget()
