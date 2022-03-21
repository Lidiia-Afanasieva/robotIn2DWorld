import random
import numpy as np
import tkinter as tk
import tkinter.font as tk_font
import time
from main import *


length_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')
weight_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')
sensor_count_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')
color_count_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')
step_count_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')



def pause():
    time.sleep(5)


def create_graphic_map(step):
    global canvas
    global my_font

    CELL_SIZE = 50

    root.configure(bg='#96AFB9', relief='groove')

    tk.Label(root, text=f'COLOR_COUNT : {color_count}', font=my_font, bg='#96AFB9').grid(row=0)
    tk.Label(root, text=f'SENSOR_COUNT : {sensor_count}', font=my_font, bg='#96AFB9').grid(row=1)
    tk.Label(root, text=f'STEP : {step} / {step_count}', font=my_font, bg='#96AFB9').grid(row=2)

    canvas = tk.Canvas(root, width=CELL_SIZE * ROOM_LENGTH, height=CELL_SIZE * ROOM_WIDTH, bg='#96AFB9')
    canvas.grid(row=4)

    tk.Button(root, text='5_SECOND_PAUSE', command=pause, bg='#749BA9', font=my_font).grid(row=6)

    for i in range(ROOM_LENGTH):
        for j in range(ROOM_WIDTH):
            x1, y1 = i * CELL_SIZE, j * CELL_SIZE
            x2, y2 = i * CELL_SIZE + CELL_SIZE, j * CELL_SIZE + CELL_SIZE
            canvas.create_rectangle((x1, y1), (x2, y2), fill=color_map[i][j])
            if prediction[0] == i and prediction[1] == j:
                canvas.create_oval((x1 + 10, y1 + 10), (x2 - 10, y2 - 10), fill='black')
            if real_i == i and real_j == j:
                canvas.create_oval((x1 + 15, y1 + 15), (x2 - 15, y2 - 15), fill='red')

    root.update_idletasks()
    root.update()
    time.sleep(0.5)
    canvas.destroy()


def take_and_go():
    global ROOM_LENGTH
    global ROOM_WIDTH
    global color_count
    global sensor_count
    global step_count

    ROOM_LENGTH = int(length_entry.get())
    ROOM_WIDTH = int(weight_entry.get())
    color_count = int(color_count_entry.get())
    sensor_count = int(sensor_count_entry.get())
    step_count = int(step_count_entry.get())

    root.destroy()


def autonomous_flag():
    global auto_flag

    auto_flag = True

    root.destroy()


def user_settings():
    root.title('SETTINGS')

    text_output = 'Enter the size of room side: \n3 <= count <= 25!\n ' \
                  'Sensor count must be: \n1 <= count <= 5!\n ' \
                  'Color count should be: \n2 <= count < inf!\n' \
                  'Enjoy!'
    tk.Label(root, text=text_output, bg='#96AFB9', fg='black', font=my_font, wraplength=300).grid(row=0)

    tk.Label(root, text="ROOM_LENGTH", font=my_font, bg='#96AFB9').grid(row=1)
    tk.Label(root, text="ROOM_WEIGHT", font=my_font, bg='#96AFB9').grid(row=2)
    tk.Label(root, text="SENSOR_COUNT", font=my_font, bg='#96AFB9').grid(row=3)
    tk.Label(root, text="COLOR_COUNT", font=my_font, bg='#96AFB9').grid(row=4)
    tk.Label(root, text="STEPS_COUNT", font=my_font, bg='#96AFB9').grid(row=5)

    length_entry.grid(row=1, column=1)
    weight_entry.grid(row=2, column=1)
    sensor_count_entry.grid(row=3, column=1)
    color_count_entry.grid(row=4, column=1)
    step_count_entry.grid(row=5, column=1)

    root.wm_geometry()

    tk.Button(root, text='DONE', command=take_and_go, width=20, font=my_font, bg='#749BA9').grid(row=6, column=0)
    tk.Button(root, text='AUTONOMOUS MODE', command=autonomous_flag, font=my_font, bg='#749BA9').grid(row=6, column=1)

    root.mainloop()