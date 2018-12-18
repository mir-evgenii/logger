import tkinter
# from SSH import SSH


class GUI:

    def __init__(self):

        window = tkinter.Tk()

        btn = tkinter.Button(window, text="Click me", width=50, height=15, bg="white", fg="black")
        btn.bind("<Button-1>", self.auth)
        btn.pack()
        window.mainloop()

    def auth(self, event):
        print('Yet another hello world')
