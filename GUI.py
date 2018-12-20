import tkinter
import tkinter.messagebox
from typing import List

from SSH import SSH


class GUI:

    def __init__(self):
        self.login = None
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

        self.root = tkinter.Tk()
        self.root.title("Logger")
        self.auth()
        self.root.mainloop()

    def connect(self, event):
        user = self.login.get()
        password = self.password.get()
        host = self.host.get(self.host.curselection())
        port = 22
        self.ssh = SSH(host, user, password, port)
        if self.ssh.error != 0:
            tkinter.messagebox.showerror("Ошибка!", self.ssh.error)
        else:
            self.main_window(host)

    def auth(self):
        login_text = tkinter.Label(self.root, text="Введите логин", font="Arial 11")  # строка текста
        self.login = tkinter.Entry(self.root, width=20, bd=3)
        self.login.insert(0, 'oper')  # значение поля по умолчанию
        password_text = tkinter.Label(self.root, text="Введите пароль", font="Arial 11")  # строка текста
        self.password = tkinter.Entry(self.root, width=20, bd=3, show='*')
        self.password.focus_set()

        btn = tkinter.Button(self.root, text="Войти")
        btn.bind("<Button-1>", self.connect)  # связь кнопки и функции
        self.root.bind("<Return>", self.connect)

        r = ['logger-nsk', 'logger-bg', 'localhost']  # список
        self.host = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, height=4)
        for i in r:
            self.host.insert(tkinter.END, i)

        login_text.pack(padx=5, pady=5)
        self.login.pack()
        password_text.pack(padx=5, pady=5)
        self.password.pack()
        self.host.pack(padx=10, pady=10)
        btn.pack(padx=10, pady=10)

    def main_window(self, title):
        self.win = tkinter.Toplevel(self.root)
        self.ent_frame = tkinter.Frame(self.win)
        self.btn_frame = tkinter.Frame(self.win)
        self.win.title(title)
        self.win.minsize(width=400, height=200)
        text = tkinter.Label(self.win, text="Искать", font="Arial 9")
        self.find_number[0] = tkinter.Entry(self.ent_frame, width=20, bd=3)
        self.find_number[0].focus_set()
        self.find_date = tkinter.Entry(self.ent_frame, width=20, bd=3)
        btn = tkinter.Button(self.btn_frame, text="Найти")
        btn.bind("<Button-1>", self.grep)
        self.win.bind("<Return>", self.grep)
        self.result = tkinter.Label(self.win, text="Результат поиска", font="Arial 9")
        btn_add_ent = tkinter.Button(self.btn_frame, text="Добавить критерий поиска")
        btn_add_ent.bind("<Button-1>", self.add_ent)

        text.pack(padx=5, pady=5)
        self.find_date.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.find_number[0].pack(side=tkinter.LEFT, padx=5, pady=5)
        self.ent_frame.pack()
        self.btn_frame.pack()
        btn.pack(side=tkinter.LEFT, padx=5, pady=5)
        btn_add_ent.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.result.pack(padx=5, pady=5)

    def grep(self, event):
        date = self.find_date.get()

        for i in date:
            if i in "1234567890":
                pass
            else:
                tkinter.messagebox.showerror("Ошибка!", "В первое поле нужно ввести дату в формате: ГГГГММДД")

        if len(self.find_number) == 1:
            number = self.find_number[0].get()
        else:
            number = []
            for i in self.find_number:
                number.append(i.get())
        result = self.ssh.grep(number, 'log', date)
        self.result.pack_forget()
        self.result = tkinter.Label(self.win, text=result, font="Arial 9")
        self.result.pack(padx=5, pady=5)

    def add_ent(self, event):
        self.find_number.append(tkinter.Entry(self.ent_frame, width=20, bd=3))
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
        if len(self.find_text_add) < 1:
            self.btn_del_ent.pack_forget()
