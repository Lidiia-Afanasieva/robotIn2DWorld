from tkinter import Tk, Label, Button


class QBox:
    """ Class that is an object"""

    def __init__(self, master):
        """ Class init Method"""
        self.master = master
        master.title("Question Box")
        self.label = Label(master, text="Welcome to the Question Box")
        self.button = Button(master, command=self.change, text="Clickme", fg='Black')

        self.label.pack()
        self.button.pack()

    def change(self):
        self.label.pack_forget()


def main():
    root = Tk()
    QBox(root)
    root.mainloop()


if __name__ == '__main__':
    main()