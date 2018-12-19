import tkinter
import tkinter.messagebox
from SSH import SSH


class GUI:

    def __init__(self):
        self.login = None
        self.password = None
        self.host = None
        self.find_text = None
        self.ssh = None
        self.result = None
        self.win = None

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
        self.win.title(title)
        self.win.minsize(width=400, height=200)
        text = tkinter.Label(self.win, text="Искать", font="Arial 9")
        self.find_text = tkinter.Entry(self.win, width=20, bd=3)
        btn = tkinter.Button(self.win, text="Найти")
        btn.bind("<Button-1>", self.grep)
        self.win.bind("<Return>", self.grep)
        self.result = tkinter.Label(self.win, text="Результат поиска", font="Arial 9")

        text.pack(padx=5, pady=5)
        self.find_text.pack(padx=5, pady=5)
        btn.pack(padx=5, pady=5)
        self.result.pack(padx=5, pady=5)

    def grep(self, event):
        number = self.find_text.get()
        result = self.ssh.grep(number, 'log', '20181217')
        self.result.pack_forget()
        self.result = tkinter.Label(self.win, text=result, font="Arial 9")
        self.result.pack(padx=5, pady=5)
