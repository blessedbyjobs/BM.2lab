import math, parser, os
from collections import deque
import numpy as np


def f(file, x, y):
    if file == '0':
        return 0
    elif file == '1':
        return x + 1 - y
    elif file == '2':
        return x**2 + 2*x - y
    elif file == '3':
        return 3*x**2 + x**3 - y


def convert(array):
    send = []
    num = ""
    for i in range(len(array)):
        if array[i] != "\n" and array[i] != " " or array[i] == ".":
            num += array[i]
        elif num != "" and num != "-" and num != "+":
            send.append(float(num))
            num = ""

    return send


def get_available_num():
    list = os.listdir(os.getcwd())  # dir is your directory path
    count = 0
    for x in list:
        if "test" in x:
            count += 1
    return count


def get_available():
    list = os.listdir(os.getcwd())  # dir is your directory path
    answer = []
    for x in list:
        if "test" in x and "result" not in x:
            answer.append(x)
    print(answer)
    return answer


def is_file_available(name):
    list = os.listdir(os.getcwd())
    print(name)
    if name in list:
        return True
    return False


def pick_the_file():
    print("Доступно", get_available_num(), " файлов")
    file = input("Введите номер файла, начиная с 0: ")
    if is_file_available("test" + file + ".txt"):
        return file
    print("Ошибка")
    return ""


def step_check(h, h_min, h_max):
    if h <= h_min:
        h = h_min
    elif h > h_max:
        h = h_max
    return h


def step(formula, x0, y0, h):
    k1 = h * f(formula, x0, y0)
    k2 = h * f(formula, x0 + h/2.0, y0 + k1/2.0)
    k3 = h * f(formula, x0 + h, y0 - k1 + 2*k2)

    y1 = y0 + (k1 + k3)/2.0
    e = y0 + (k1 + 4*k2 + k3)/6.0

    return y1, e


def setup(file):
    fh = open("test" + file + ".txt")
    a, b, c, y0 = [float(x) for x in next(fh).split()]
    h_min, h_max, eps = [float(x) for x in next(fh).split()]
    formula = fh.readline()

    algorithm(a, b, c, y0, h_min, h_max, eps, file)


def get_pair(file):
    with open("data" + file + ".txt") as read_file:
        [last_line] = deque(read_file, maxlen=1) or ['']
    x0 = float(last_line[2:last_line.find(" ")])
    y0 = float(last_line[last_line.find("y") + 2: last_line.find("e")])
    return x0, y0


def algorithm(a, b, c, y0, h_min, h_max, eps, file):
    ft = open("data" + file + ".txt", "w+")
    ft.close()

    h = (b - a) / 10.0
    h = step_check(h, h_min, h_max)

    dot_counter = 1
    n_ud = 0

    if c == a:
        x0 = a
        with open("data" + file + ".txt", 'a') as filek:
            filek.write("x={:<25}  y={:^25}  eps={:>25}  h={:>25}\n".format(x0, y0, 0.0, 0.0))

        x = np.empty([2])
        first = second = third = False
        while x0 < b:
            y, e = step(file, x0, y0, h)
            eps_n = abs(e - y)
            if y <= e:
                if eps_n != 0:
                    h *= (eps / eps_n) ** (1.0 / 3.0)
                else:
                    h *= 2
                h = step_check(h, h_min, h_max)
                if eps_n > eps:
                    n_ud += 1

                if b - (x0 + h) >= h_min:
                    x0 += h
                else:
                    """if first or second or third:
                        x0 = x[1]
                        h = h_min
                        y, e = step(file, x0, y0, h)
                        print("здесь")
                    else:
                        if b - x0 >= 2 * h_min:
                            x[0] = b - h_min
                            h -= h_min
                            x0 = x[0]
                            y, e = step(file, x0, y0, h)
                            x[1] = b

                            print(y)
                            print("1 случай")
                            first = True
                        else:
                            if b - x0 <= 1.5 * h_min:
                                x[0] = x[1] = b
                                x0 = x[0]
                                print("2 случай")
                                second = True
                            else:
                                if 1.5 * h_min < (b - x0) < 2 * h_min:
                                    x[0] = x0 + (b - x0) / 2.0
                                    x[1] = b
                                    x0 = x[0]
                                    print("3 случай")
                                    third = True"""
                    x0 = b
                y0 = y
                dot_counter += 1

                with open("data" + file + ".txt", 'a') as filek:
                    filek.write("x={:<25}  y={:^25}  eps={:>25}  h={:>25}\n".format(x0, y0, eps_n, h))
            else:
                h *= (eps / eps_n) ** (1.0 / 3.0)
                h = step_check(h, h_min, h_max)
        print("Общее число точек: ", dot_counter)
        print("Число неудовлетворяющих точек: ", n_ud)
    elif c == b:
        x0 = b
        with open("data" + file + ".txt", 'a') as filek:
            filek.write("x={:<25}  y={:^25}  eps={:>25}\n".format(x0, y0, 0.0))
        stop = False
        while x0 > a and stop is False:
            y, e = step(file, x0, y0, h)
            eps_n = abs(e - y)
            if y <= e:
                if eps_n != 0:
                    h *= math.pow(eps / eps_n, 1.0 / 3.0)
                else:
                    h *= 2
                h = step_check(h, h_min, h_max)
                if eps_n > eps:
                    n_ud += 1
                # print("x = ", x0, "; y(x) = ", y0, "; погрешность = ", eps_n)
                if x0 == a:
                    if stop is False:
                        stop = True
                x0 -= h
                if x0 < a:
                    x0 = a
                y0 = y
                if stop is False:
                    dot_counter += 1

                with open("data" + file + ".txt", 'a') as filek:
                    filek.write("x={:<25}  y={:^25}  eps={:>25}\n".format(x0, y0, eps_n))
            else:
                h *= math.pow(eps / eps_n, 1.0 / 3.0)
                h = step_check(h, h_min, h_max)
        print("Общее число точек: ", dot_counter)
        print("Число неудовлетворяющих точек: ", n_ud)


def main():
    print("< Решение задачи Коши с заданной точностью с автоматическим выбором максимальной длины шага > ")
    print("< Метод второго порядка метода Рунге-Кутта > ")
    print("< Метод третьего порядка для уточнения решения метода Рунге-Кутта > ")
    print("< Выполнил Рябков Алексей >")

    ans = pick_the_file()
    if ans != "":
        setup(ans)


main()
