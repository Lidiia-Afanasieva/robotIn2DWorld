import tkinter as tk

# --- functions ---


def second_window():
    window.destroy()

    second = tk.Tk()

    button = tk.Button(second, text='CLOSE SECOND', command=second.destroy)
    button.pack()

    second.mainloop()

# --- main ---

window = tk.Tk()

button = tk.Button(window, text='CLOSE FIRST', command=second_window)
button.pack()

window.mainloop()
