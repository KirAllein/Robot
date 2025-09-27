import time


class Robot:  # Класс робота

    def __init__(self):
        self.local_map = []

    def moving(self, s_x, p_y):  # функция движения робота
        d_x = 0  # переменная в которой храним значение координаты х робота
        d_y = 0  # переменная в которой храним значение координаты у робота
        delta_x, delta_y = 0, 0  # Сюда будем передавать значения изменения координаты
        local_map = self.look_around()  # Запрашиваем карту вокруг робота
        x_r = -1
        y_r = -1
        for i, row in enumerate(local_map):
            try:
                x_r = row.index(1)
                y_r = i
                break
            except ValueError:
                continue
        print('----------------')  # Это я черту печатаю, чтобы отделять вывод Мира от локальной карты робота
        for row in local_map:  # Печатаю построчно карту робота, чтобы знать, что он видит
            print(*row)
        if len(local_map) == 3 and len(local_map[0]) == 3:
            if (local_map[0][1] != 0 and local_map[1][0] == 0) or (
                    local_map[0][0] != 0 and local_map[0][0] != 1 and local_map[1][
                0] == 0):  # Если перед роботом препятсивие
                # или слева вверху есть препятствие, но при этом впереди свободно, делаем шаг влево
                delta_x = -1  # шаг влево
            elif (local_map[2][0] != 0 or local_map[1][0] != 0) and local_map[2][
                1] == 0:  # если слева внизу или слева препятствие, то делаем шаг вниз
                delta_y = 1  # шаг вниз
            elif ((local_map[2][2] != 0 or local_map[2][1] != 0) and local_map[1][
                2] == 0):  # если справа внизу или под роботом есть препятствие
                # и при этом справа свободно, то делаем шаг вправо
                delta_x = 1  # шаг вправо
            else:
                delta_y = -1  # Шаг вверх. Во всех остальных случаях шагаем на север
        else:
            if (x_r == 1 and y_r == 0 and len(local_map[y_r]) == 3) or (x_r == 0 and y_r == 0):
                delta_x = 1  # шаг вправо
            elif (x_r == 1 and y_r == 1 and len(local_map) == 3) or (
                    x_r == 1 and y_r == 0 and len(local_map[y_r]) == 2):
                delta_y = 1  # шаг вниз
            elif (x_r == 1 and y_r == 1) or (x_r == 1 and y_r == 0) and len(local_map) == 2:
                delta_x = -1  # шаг влево
            else:
                delta_y = -1  # шаг вверх
        return d_x + delta_x, d_y + delta_y  # возвращаем измененные значения координат на соответствующую дельту

    def look_around(self):  # функция, где робот смотрит вокруг себя
        self.local_map = world1.determine_robot_position(0)  # вызов функции из Мира, передающей локальную карту
        return self.local_map


class World:  # Класс Мира

    def __init__(self, width, length, obstacle=[]):
        self.map = self.create_world(width, length, obstacle)
        self.robot_list = []

    def create_world(self, width, length, obstacle):
        world = [[0] * width for _ in range(length)]  # создаем поле размерами ширина х высота
        for y in range(length):
            for x in range(width):
                if len(obstacle) != 0:
                    if obstacle[0][0] <= x <= obstacle[1][0] and obstacle[0][1] <= y <= obstacle[2][
                        1]:  # рисуем препятствие
                        world[y][x] = 'X'  # препятствие у нас обозначено буквой х

        # world[0][5] = 'X'
        # world[1][5] = 'X'
        # world[2][5] = 'X'
        # world[3][5] = 'X'
        # world[0][2] = 'X'
        # world[1][2] = 'X'
        # world[2][2] = 'X'

        return world

    def add_robot(self, x, y):
        robot = [Robot(), x, y]  # добавляем робота в Мир
        self.robot_list.append(robot)

    def draw_map(self):  # Класс рисования Мира
        c_y = self.robot_list[0][1]  # координата робота у
        c_x = self.robot_list[0][2]  # координата робота х
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if x == c_x and y == c_y:  # если координаты сошлись на координатах робота, значит здесь робот
                    print(1, end=' ')
                else:
                    print(self.map[y][x], end=' ')  # в остальных случаях рисуем просто поля Мира
            print()

    def get_robot_list(self):  # функция, чтобы получить список всех роботов
        return self.robot_list

    def step(self):  # функция, где робот делает шаг в Мире
        for r in self.robot_list:  # обращаемя к списку роботов
            y = r[1]  # изначальна координата у
            x = r[2]  # значальна координата х
            d_x, d_y = r[0].moving(x, y)  # Робот принимает решение о движении
            if 0 <= y <= len(self.map) - 1 and 0 <= x <= len(
                    self.map[0]) - 1:  # Сравниваем координаты робота и размеры Мира, чтобы не выйти за его пределы
                r[1] += d_y  # Передаем новое значение у
                r[2] += d_x  # передаем новое значение х
            else:
                exit()

    def determine_robot_position(self, robot_num):
        robot_position = []
        global_map = world1.map  # запрашиваем глобальную карту
        robot = world1.get_robot_list()[
            robot_num]  # запрашиваем список роботов, откуда возьмем информацию о нужном нам роботе
        for y in range(len(global_map)):
            row = []  # переменная, куда будет класть отдельные строки карты
            for x in range(len(global_map[y])):
                if y in range(robot[1] - 1, robot[1] + 2) and x in range(robot[2] - 1,
                                                                         robot[2] + 2):  # проверяем находится ли точка
                    # вокруг робота (то есть может ли робот видеть эту зону)
                    if y == robot[1] and x == robot[2]:  # проверяем соответствует ли точка координатам робота
                        row.append(1)  # если соответствует, то добавляем на карту самого робота, он обозначен 1
                    else:
                        row.append(global_map[y][x])  # в остальных случаях добавляем точки вокруг робота
            if len(row) != 0:  # пустые строки не добавляем, нужны только те, что видит робот
                robot_position.append(row)
        return robot_position


world1 = World(10, 10,[[3,4], [5,3], [3,6], [5,6]])
world1.add_robot(8, 4)
world1.get_robot_list()
print()
while True:
    print(world1.get_robot_list())
    world1.draw_map()
    world1.step()
    world1.get_robot_list()
    print()
    time.sleep(2)

# Список замечаний:
# 1. Робот добавляется на поле препятствия
# 2. Код останавливается, когда робот попадает на край препятствия
# 3. Отображается только 1 робот, остальные роботы не отображаются
# 4. Препятствие захардкожена в классе Мир. (Fixed)
# 5. Нельзя создать Мир без препятствий (Fixed)
# 6. Локальная карта передается роботу из класса Мир, и робот довольствуется только тем, что ему передано (Done)
# 7. Ошибка при приближении к границе Мира (Done)
# 8. Если доходим до края Мира, это должно восприниматся как препятствие (Dnoe)
# 9. Проверка наличия препятствия ориентирует только на латинскую буквы X (Done)
# 10. Робот не видит дыру в заборе
# 11. Научить робота ходить по диагонале
# 12. Робот проходит сквозь препятствие слева
