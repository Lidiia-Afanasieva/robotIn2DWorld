import random
import numpy as np
import tkinter as tk
import tkinter.font as tk_font
import time


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

auto_flag = False
root = tk.Tk()
root.wm_geometry("+0+0")
root.configure(bg='#96AFB9', relief='groove')
canvas = tk.Canvas()
my_font = tk_font.Font(family='Comic Sans MS', size=15, weight="bold", slant="italic")

ROOM_LENGTH = 7
ROOM_WIDTH = 5
sensor_count = 1
color_count = 0
step_count = 10


def find_max_element(arr: list) -> tuple:  # вернёт индексы максимального числа
    gen = ((i, j) for i in range(ROOM_LENGTH) for j in range(ROOM_WIDTH))
    return max(gen, key=lambda x: arr[x[0]][x[1]])


def sense_in_2d(p_map: list, real_color: str, real_i, real_j) -> list:
    p_new = []

    for i in range(ROOM_LENGTH):

        for j in range(ROOM_WIDTH):

            if sensor_count == 1:

                if real_color == color_map[i][j]:
                    # совпадение цвета - вероятность увеличится
                    p_new.append(P_HIT * p_map[i][j])

                else:
                    # несовпадение цвета - вероятность уменьшится
                    p_new.append(P_MISS * p_map[i][j])

            elif sensor_count == 2:

                if real_color == color_map[i][j] and \
                        color_map[real_i][(real_j + 1) % len(p_map[0])] == color_map[i][(j + 1) % len(p_map[0])]:

                    # совпадение цвета - вероятность увеличится
                    p_new.append((P_HIT ** 2) * p_map[i][j])

                else:
                    # несовпадение цвета - вероятность уменьшится
                    p_new.append((P_MISS ** 2) * p_map[i][j])

            elif sensor_count == 3:

                if real_color == color_map[i][j] and \
                        color_map[real_i][(real_j + 1) % len(p_map[0])] == color_map[i][(j + 1) % len(p_map[0])] and \
                        color_map[real_i][(real_j - 1) % len(p_map[0])] == color_map[i][(j - 1) % len(p_map[0])]:

                    # совпадение цвета - вероятность увеличится
                    p_new.append((P_HIT ** 3) * p_map[i][j])

                else:
                    # несовпадение цвета - вероятность уменьшится
                    p_new.append((P_MISS ** 3) * p_map[i][j])

            elif sensor_count == 4:

                if real_color == color_map[i][j] and \
                        color_map[real_i][(real_j + 1) % len(p_map[0])] == color_map[i][(j + 1) % len(p_map[0])] and \
                        color_map[real_i][(real_j - 1) % len(p_map[0])] == color_map[i][(j - 1) % len(p_map[0])] and \
                        color_map[(real_i + 1) % len(p_map[0])][real_j] == color_map[(i + 1) % len(p_map[0])][j]:

                    # совпадение цвета - вероятность увеличится
                    p_new.append((P_HIT ** 4) * p_map[i][j])

                else:
                    # несовпадение цвета - вероятность уменьшится
                    p_new.append((P_MISS ** 4) * p_map[i][j])

            elif sensor_count == 5:

                if real_color == color_map[i][j] and \
                        color_map[real_i][(real_j + 1) % len(p_map[0])] == color_map[i][(j + 1) % len(p_map[0])] and \
                        color_map[real_i][(real_j - 1) % len(p_map[0])] == color_map[i][(j - 1) % len(p_map[0])] and \
                        color_map[(real_i + 1) % len(p_map[0])][real_j] == color_map[(i + 1) % len(p_map[0])][j] and \
                        color_map[(real_i - 1) % len(p_map[0])][real_j] == color_map[(i - 1) % len(p_map[0])][j]:

                    # совпадение цвета - вероятность увеличится
                    p_new.append((P_HIT ** 5) * p_map[i][j])

                else:
                    # несовпадение цвета - вероятность уменьшится
                    p_new.append((P_MISS ** 5) * p_map[i][j])

    summ_p = sum(p_new)
    p_new = [x / summ_p for x in p_new]

    return np.array(p_new).reshape((ROOM_LENGTH, ROOM_WIDTH))


def move_in_2d(p_map: list, step: int) -> list:
    p_new = []

    for i in range(ROOM_LENGTH):

        for j in range(ROOM_WIDTH):
            current_probability = p_map[i][(j + step) % ROOM_WIDTH] * P_FORWARD
            current_probability += p_map[i][j] * P_STAY
            current_probability += p_map[(i - step) % ROOM_LENGTH][(j + step) % ROOM_WIDTH] * P_LEFT
            current_probability += p_map[(i + step) % ROOM_LENGTH][(j + step) % ROOM_WIDTH] * P_RIGHT

            p_new.append(current_probability)

    return np.array(p_new).reshape((ROOM_LENGTH, ROOM_WIDTH))


def get_false_count():
    print(f'false_count = {false_count}')
    return None


def color_count_find():
    middle_side = (ROOM_LENGTH + ROOM_WIDTH) // 2
    if middle_side <= 3:
        color_t = 2

    else:
        color_t = 3 + middle_side // 5

    return color_t


def get_hex_color():
    return '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))


def create_color_map():
    global color_count

    if auto_flag:
        color_count = color_count_find()

    color_measurements = [get_hex_color() for _ in range(color_count)]
    c_map = np.array([random.choice(color_measurements) for _ in np.nditer(p_map)]).reshape((ROOM_LENGTH, ROOM_WIDTH))

    print(f'color count is {color_count}')

    return c_map


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


def start_simulating():
    root.title('SIMULATING')

    global p_map
    global real_i
    global real_j
    global false_count
    global prediction
    global step_count

    print(p_map)
    print(color_map)
    print(f'start element is: {color_map[real_i][real_j]}')

    for k in range(step_count):

        print('//////////////////////')

        # first part of algorythm
        p_map = sense_in_2d(p_map, color_map[real_i][real_j], real_i, real_j)
        print('sensor_count :', sensor_count)
        print('color_count :', color_count)
        prediction = find_max_element(p_map)

        print('sense: \n', end='')
        print(p_map)
        print(f' real = {real_i, real_j}, prediction = {prediction}')

        if real_i != prediction[0] or real_j != prediction[1]:
            false_count += 1

        # second part of algorythm
        p_map = move_in_2d(p_map, 1)
        real_j = (real_j - 1) % len(p_map[0])
        prediction = find_max_element(p_map)

        print('move:  \n', end='')
        print(p_map)
        print(f' real = {real_i, real_j}, prediction = {prediction} \n')

        if real_i != prediction[0] or real_j != prediction[1]:
            false_count += 1

        create_graphic_map(k)

    root.destroy()

# //////////////////////////////////
# START
# //////////////////////////////////


length_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')
weight_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')
sensor_count_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')
color_count_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')
step_count_entry = tk.Entry(root, width=30, bg='#A28FA7', justify='center')

user_settings()

p_map = np.zeros((ROOM_LENGTH, ROOM_WIDTH))
p_map[real_i][real_j] = 1

color_map = create_color_map()

root = tk.Tk()
root.wm_geometry("+0+0")

start_simulating()
get_false_count()
