# -*- coding: utf-8 -*-
"""roborIn2DWorld.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hejjgCiBbOL_Pxjd7drwJfIQZkTk6DVJ
"""

import random
import numpy as np
import copy

p_map = np.zeros((4, 4), int)
p_map[2][2] = 1
measurements = ['black', 'red', 'yellow']  # пока похуй, пусть будет два

pHit = 0.8  # вероятность что датчик прав
pMiss = 0.2  # вероятность что датчик ошибся

p_forward = 0.6  # вероятность того, что робот идёт прямо
p_stay = 0.1  # вероятность того, что робот не сдвинулся 
p_left = 0.15  # вероятность того, что робот по диагонали в лево
p_right = 0.15  # вероятность того, что робот идёт по диагонали вправо

color_map = np.array([random.choice(measurements) for item in np.nditer(p_map)]).reshape((4, 4))
# color_map = np.array([['red', 'red', 'green', 'red'],
#                      ['green', 'green', 'red', 'green'],
#                      ['red', 'red', 'green', 'green'],
#                      ['red', 'green', 'red', 'red']])
color_map = np.array([['yellow', 'red', 'red', 'black'],
                     ['black', 'red', 'yellow', 'yellow'],
                     ['red', 'black', 'black', 'red'],['red', 'red', 'yellow', 'red']])

real_i = 2  # ожидаемая координата игрека
real_j = 2  # ожидаемая координата икса
prediction = (0, 0)  # предсказание в какой мы точке
false_count = 0  # количество несовпадения перемещений

room_length = len(p_map)
room_width = len(p_map[0])

print(p_map)
print(color_map)

def find_max_element(arr : list) -> tuple:  # вернёт индексы максимального числа
    gen = ((i, j) for i in range(room_length) for j in range(room_width))
    return(max(gen, key = lambda x: arr[x[0]][x[1]]))

matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
# print(find_max_element(matrix))
# print([j for i in matrix for j in i])

def sense_2d(p_map: list, real_color: str) -> list:
    p_new = []

    for i in range(room_length):

        for j in range(room_width):

            if real_color == color_map[i][j]:
                # совпадение цвета - вероятность увеличится
                p_new.append(pHit * p_map[i][j])
            
            else:
                # несовпадение цвета - вероятность уменьшится
                p_new.append(pMiss * p_map[i][j])
    summ_p = sum(p_new)
    p_new = [x / summ_p for x in p_new]     

    return np.array(p_new).reshape((room_length, room_width))

# def move_2d(p_map: list, step: int) -> list:
#     p_new = np.zeros((room_length, room_width))

#     for i in range(room_length):

#         for j in range(room_width):
            
#             p_new[(j+1) % room_length][i] += p_map[j][i]*p_forward
#             p_new[(j+1) % room_length][(i+1)%room_length] += p_map[j][i]*p_left
#             p_new[(j+1) % room_length][i-1] += p_map[j][i]*p_right
        
#             # p_new.append(current_probability)   
    
#     return p_new

def move_2d(p_map: list, step: int) -> list:
    p_new = []

    for i in range(room_length):

        for j in range(room_width):

            current_probability = p_map[(i+step) % room_length][j] * p_forward
            current_probability += p_map[i][j] * p_stay
            current_probability += p_map[i][(j-step) % room_width] * p_left
            current_probability += p_map[i][(j+step) % room_width] * p_right
        
            p_new.append(current_probability)   
    
    return np.array(p_new).reshape((room_length, room_width))

print(f'false_count= {false_count}')

for k in range(10):
    print('//////////////////////')

    # first part of algorythm 
    p_map = sense_2d(p_map, color_map[real_i][real_j])
    prediction = find_max_element(p_map)

    print('sense: \n', end = '')
    print(p_map)
    print(f' real = {real_i, real_j}, prediction = {prediction}')

    if real_i != prediction[0] or real_j != prediction[1]:
        false_count += 1

    # second part of algorythm 
    p_map = move_2d(p_map, 1)
    real_i = (real_i - 1) % len(p_map)                                             
    prediction = find_max_element(p_map)

    print('move:  \n', end = '')
    print(p_map)
    print(f' real = {real_i, real_j}, prediction = {prediction}\n')
    
    if real_i != prediction[0] or real_j != prediction[1]:
        false_count += 1

# def sense_2d(p_map, real_color):
#     p_new = []

#     for i in range(4):

#         for j in range(4):

#             hit = (real_color == color_map[i][j])
#             p_new.append(p_map[i][j] * (hit * pHit + (1-hit) * pMiss))
        
#     s = sum(p_new)
#     p_new = [x / s for x in p_new] 
    
#     return np.array(p_new).reshape((4, 4))