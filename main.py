# -*- coding: utf-8 -*-
"""roborIn2DWorld.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hejjgCiBbOL_Pxjd7drwJfIQZkTk6DVJ
"""
import os
import random
import sys
from tkinter import ttk

import numpy as np
import tkinter as tk
import time
import copy

# Temps initialisation

P_HIT = 0.8  # вероятность что датчик прав
P_MISS = 0.2  # вероятность что датчик ошибся

P_FORWARD = 0.6  # вероятность того, что робот идёт прямо
P_STAY = 0.1  # вероятность того, что робот не сдвинулся
P_LEFT = 0.15  # вероятность того, что робот по диагонали влево
P_RIGHT = 0.15  # вероятность того, что робот идёт по диагонали вправо

real_i = 2  # ожидаемая координата игрека
real_j = 2  # ожидаемая координата икса
prediction = (0, 0)  # предсказание в какой мы точке
false_count = 0  # количество несовпадения перемещений

p_map = np.zeros((5, 5), int)
p_map[2][2] = 1

ROOM_LENGTH = len(p_map)
ROOM_WIDTH = len(p_map[0])


def find_max_element(arr: list) -> tuple:  # вернёт индексы максимального числа
    gen = ((i, j) for i in range(ROOM_LENGTH) for j in range(ROOM_WIDTH))
    return max(gen, key=lambda x: arr[x[0]][x[1]])


def sense_in_2d(p_map: list, real_color: str) -> list:
    p_new = []

    for i in range(ROOM_LENGTH):

        for j in range(ROOM_WIDTH):

            if real_color == color_map[i][j]:
                # совпадение цвета - вероятность увеличится
                p_new.append(P_HIT * p_map[i][j])

            else:
                # несовпадение цвета - вероятность уменьшится
                p_new.append(P_MISS * p_map[i][j])
    summ_p = sum(p_new)
    p_new = [x / summ_p for x in p_new]

    return np.array(p_new).reshape((ROOM_LENGTH, ROOM_WIDTH))


def move_in_2d(p_map: list, step: int) -> list:
    p_new = []

    for i in range(ROOM_LENGTH):

        for j in range(ROOM_WIDTH):
            current_probability = p_map[(i + step) % ROOM_LENGTH][j] * P_FORWARD
            current_probability += p_map[i][j] * P_STAY
            current_probability += p_map[(i + step) % ROOM_WIDTH][(j - step) % ROOM_WIDTH] * P_LEFT
            current_probability += p_map[(i + step) % ROOM_WIDTH][(j + step) % ROOM_WIDTH] * P_RIGHT

            p_new.append(current_probability)

    return np.array(p_new).reshape((ROOM_LENGTH, ROOM_WIDTH))


def get_false_count():
    print(f'false_count = {false_count}')
    return None


def color_count_find():

    middle_side = (ROOM_LENGTH + ROOM_WIDTH) // 2
    if middle_side <= 3:
        color_count = 2

    else:
        color_count = 3 + middle_side // 5

    return color_count


def get_hex_color():
    return '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))


def create_color_map():

    color_count = color_count_find()

    color_measurements = [get_hex_color() for _ in range(color_count)]
    c_map = np.array([random.choice(color_measurements) for _ in np.nditer(p_map)]).reshape((ROOM_LENGTH, ROOM_WIDTH))

    print(f'color count is {color_count}')

    return c_map


def close():
    root.destroy()


def create_graphic_map():

    CELL_SIZE = 50


    canvas = tk.Canvas(root, width=CELL_SIZE * ROOM_LENGTH, height=CELL_SIZE * ROOM_WIDTH)

    cell_colors = ['#2cebe9', '#300a7e']
    ci = 0  # color index

    for i in range(ROOM_LENGTH):
        for j in range(ROOM_WIDTH):
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE + CELL_SIZE
            canvas.create_rectangle((x1, y1), (x2, y2), fill=color_map[i][j])
            if real_i == i and real_j == j:                          
                canvas.create_oval((x1 + 10, y1 + 10), (x2 - 10, y2 - 10), fill='black')
    #b = tk.Button(root, text='Create new window and close current', command=root.after(1000, root.destroy()))
    #frm = ttk.Frame(root, padding=10)
    #rm.grid()
    #ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    #ttk.Button(root, text="Quit", command=root.destroy).grid(column=1, row=0)
    canvas.pack()
    button = tk.Button(root, text='MOVE', command=close)
    button.pack()
    root.wm_geometry("+%d+%d" % ((root.winfo_screenwidth() - root.winfo_reqwidth()) / 2, (root.winfo_screenheight() - root.winfo_reqheight()) / 2))
    root.mainloop()
    #root.after(1000, root.destroy())
    # time.sleep()

# //////////////////////////////////
# START
# //////////////////////////////////


measurements = ['black', 'red', 'yellow']  # так лучше
color_map = create_color_map()


print(p_map)
print(color_map)
print(f'start element is: {color_map[real_i][real_j]}')

for k in range(10):

    print('//////////////////////')

    # first part of algorythm 
    p_map = sense_in_2d(p_map, color_map[real_i][real_j])
    prediction = find_max_element(p_map)

    print('sense: \n', end='')
    print(p_map)
    print(f' real = {real_i, real_j}, prediction = {prediction}')

    if real_i != prediction[0] or real_j != prediction[1]:
        false_count += 1

    # second part of algorythm 
    p_map = move_in_2d(p_map, 1)
    real_i = (real_i - 1) % len(p_map)
    prediction = find_max_element(p_map)

    print('move:  \n', end='')
    print(p_map)
    print(f' real = {real_i, real_j}, prediction = {prediction} \n')

    if real_i != prediction[0] or real_j != prediction[1]:
        false_count += 1
    root = tk.Tk()
    create_graphic_map()  

get_false_count()
# root = tk.Tk()
# create_graphic_map()
# на случай двухцветной работы
# color_map = np.array([['red', 'red', 'green', 'red'],
#                      ['green', 'green', 'red', 'green'],
#                      ['red', 'red', 'green', 'green'],
#                      ['red', 'green', 'red', 'red']])

# на случай 3хцветной работы
# color_map = np.array([['yellow', 'red', 'red', 'black'],
#                       ['black', 'red', 'yellow', 'yellow'],
#                       ['red', 'black', 'black', 'red'],
#                       ['red', 'red', 'yellow', 'red']])
# def move_in_2d(p_map: list, step: int) -> list:
#     p_new = np.zeros((room_length, room_width))

#     for i in range(room_length):

#         for j in range(room_width):

#             p_new[(j+1) % room_length][i] += p_map[j][i]*p_forward
#             p_new[(j+1) % room_length][(i+1)%room_length] += p_map[j][i]*p_left
#             p_new[(j+1) % room_length][i-1] += p_map[j][i]*p_right

#             # p_new.append(current_probability)   

#     return p_new

matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
# print(find_max_element(matrix))
# print([j for i in matrix for j in i])
