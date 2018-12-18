import tkinter
from SSH import SSH


class GUI:

    def __init__(self):

        self.ent = None
        self.but = None
        self.tex = None

        self.login_text = None
        self.login = None
        self.password_text = None
        self.password = None
        self.host = None

        self.root = tkinter.Tk()
        self.root.title("Logger")
        self.auth()
        # self.main_window()
        # self.test()
        self.root.mainloop()

    def hi(self, event):
        # print('Yet another hello world')
        user = self.login.get()
        password = self.password.get()
        # host = self.host.get()
        host = 'localhost'
        port = 22
        ssh = SSH(host, user, password, port)
        grep = ssh.grep('t', 'log', '20181217')
        print(grep)

    def auth(self):
        self.login_text = tkinter.Label(self.root, text="Введите логин", font="Arial 11")  # строка текста
        self.login = tkinter.Entry(self.root, width=20, bd=3)
        self.password_text = tkinter.Label(self.root, text="Введите пароль", font="Arial 11")  # строка текста
        self.password = tkinter.Entry(self.root, width=20, bd=3)

        btn = tkinter.Button(self.root, text="Войти")
        btn.bind("<Button-1>", self.hi)  # связь кнопки и функции
        self.root.bind("<Return>", self.hi)

        r = ['logger-nsk', 'logger-bg', 'localhost']  # список
        self.host = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, height=4)
        for i in r:
            self.host.insert(tkinter.END, i)

        self.login_text.pack(padx=5, pady=5)
        self.login.pack()
        self.password_text.pack(padx=5, pady=5)
        self.password.pack()
        btn.pack(padx=10, pady=10)
        self.host.pack(padx=10, pady=10)

    def main_window(self):
        lab0 = tkinter.Label(self.root, text="Поиск", font="Arial 9")  # строка текста
        ent0 = tkinter.Entry(self.root, width=20, bd=3)

        btn = tkinter.Button(self.root, text="Найти")
        btn.bind("<Button-1>", self.hi)

        frm = tkinter.Frame(self.root, width=500, height=100, bg='grey')

        # Не работает с pack и Frame
        # frm = tkinter.Text(self.root, width=40, height=3, font='14')
        # scr = tkinter.Scrollbar(self.root, command=frm.yview)
        # frm.configure(yscrollcommand=scr.set)
        # frm.grid(row=0, column=0)
        # scr.grid(row=0, column=1)

        lab0.pack(padx=5, pady=5)
        ent0.pack()
        btn.pack(padx=10, pady=10)
        frm.pack(padx=10, pady=10)

    def test(self):
        self.ent = tkinter.Entry(self.root, width=1)
        self.but = tkinter.Button(self.root, text="Вывести")
        self.tex = tkinter.Text(self.root, width=20, height=3, font="12", wrap=tkinter.WORD)
        self.ent.grid(row=0, column=0, padx=20)
        self.but.grid(row=0, column=1)
        self.tex.grid(row=0, column=2, padx=20, pady=10)
        self.but.bind("<Button-1>", self.output)

    def output(self, event):
        s = self.ent.get()

        if s == "1":
            self.tex.delete(1.0, tkinter.END)
            self.tex.insert(tkinter.END, "Обслуживание клиентов на втором этаже")
        elif s == "2":
            self.tex.delete(1.0, tkinter.END)
            self.tex.insert(tkinter.END, "Пластиковые карты выдают в соседнем здании")
        else:
            self.tex.delete(1.0, tkinter.END)
            self.tex.insert(tkinter.END, "Введите 1 или 2 в поле слева")
