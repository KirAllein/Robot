import time


class Robot:  # Класс робота

    def __init__(self):
        self.local_map = []

    def moving(self, s_x, p_y): # функция движения робота
        d_x = 0  # переменная в которой храним значение координаты х робота
        d_y = 0  # переменная в которой храним значение координаты у робота
        delta_x, delta_y = 0, 0  # Сюда будем передавать значения изменения координаты
        local_map = self.look_around()  # Запрашиваем карту вокруг робота
        print('----------------')  # Это я черту печатаю, чтобы отделять вывод Мира от локальной карты робота
        for row in local_map:  # Печатаю построчно карту робота, чтобы знать, что он видит
            print(*row)
        if local_map[0][1] == 'X' or (
                local_map[0][0] == 'X' and local_map[1][0] == 0):  # Если перед роботом препятсивие
            # или слева вверху есть препятсвие, но при этом впереди свободно, делаем шаг влево
            delta_x = -1  # шаг влево
        elif (local_map[2][2] == 'X' or local_map[2][1] == 'X') and local_map[1][
            2] == 0:  # если справа внизу или под роботом есть препятствие
            # и при этом справа свободно, то делаем шаг вправо
            delta_x = 1  # шаг вправо
        elif (local_map[2][0] == 'X' or local_map[1][0] == 'X') and local_map[2][
            1] == 0:  # если слева внизу или слева препятсвие, то делаем шаг вниз
            delta_y = 1  # шаг вниз
        else:
            delta_y = -1  # Шаг вверх. Во всех состальных случаях шагаем на север
        return d_x + delta_x, d_y + delta_y  # возвращаем измененные значения координат на соответствующую дельту

    def look_around(self):  # функция, где робот смотрит вокруг себя
        self.local_map = []  # переменная, где хранится локальная карта
        global_map = world1.map  # запрашиваем глобальную карту
        robot = world1.get_robot_list()  # запрашиваем список роботов, откуда возьмем информацию о нужном нам роботе
        for y in range(len(global_map)):
            row = []  # переменная, куда будет класть отдельные строки карты
            for x in range(len(global_map[y])):
                if y in range(robot[0][1] - 1, robot[0][1] + 2) and x in range(robot[0][2] - 1, robot[0][
                                                                                                    2] + 2):  # проверяем находится ли точка
                    # вокруг робота (то есть может ли робот видеть эту зону)
                    if y == robot[0][1] and x == robot[0][2]:  # проверяем соответствует ли точка координатам робота
                        row.append(1)  # если соответствует, то добавляем на карту самого робота, он обозначен 1
                    else:
                        row.append(global_map[y][x])  # в остальных случаях добавляем точки вокруг робота
            if len(row) != 0:  # пустые строки не добавляем, нужны только те, что видит робот
                self.local_map.append(row)
        return self.local_map


# Робот на основании полученных данных прнимает решение, куда идти


class World: # Класс Мира

    def __init__(self, width, length):
        self.map = self.create_world(width, length)
        self.robot_list = []

    def create_world(self, width, length):
        world = [[0] * width for _ in range(length)]  # создаем поле размерами ширина х высота
        obstacle = [[3, 2], [5, 2], [3, 4], [5, 4]]   # задаем 4 угла препятстсвия, потом это по-другому будем передавать, пока так
        for y in range(length):
            for x in range(width):
                if obstacle[0][0] <= x <= obstacle[1][0] and obstacle[0][1] <= y <= obstacle[2][1]:  # рисуем препятствие
                    world[y][x] = 'X'  # препятствие у нас обозначено буквой х
        return world

    def add_robot(self, x, y):
        robot = [Robot(), x, y]  # добавляем робота в Мир
        self.robot_list.append(robot)

    def draw_map(self): # Класс рисования Мира
        c_y = self.robot_list[0][1]  # координата робота у
        c_x = self.robot_list[0][2] # координата робота х
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if x == c_x and y == c_y: #  если координаты сошлись на координатах робота, значит здесь робот
                    print(1, end=' ')
                else:
                    print(self.map[y][x], end=' ')  #  в остальных случаях рисуем просто поля Мира
            print()

    def get_robot_list(self): #  функция, чтобы получить список всех роботов
        return self.robot_list

    def step(self): # функция, где робот делает шаг в Мире
        for r in self.robot_list: #  обращаемя к списку роботов
            y = r[1] #  изначальна координата у
            x = r[2] # значальна координата х
            d_x, d_y = r[0].moving(x, y)  # Робот принимает решение о движении
            if 1 <= y <= len(self.map) - 2 and 1 <= x <= len(
                    self.map[0]) - 2:  # Сравниваем координаты робота и размеры Мира, чтобы не выйти за его пределы
                r[1] += d_y # Передаем новое значение у
                r[2] += d_x # передаем новое значение х
            else:
                exit()


# реализовать, чтобы он не убегал за края карты, в рамках step (done)
# И чтобы робот не втыкался в препятсвия (done)
# Передавать роботу локальную карту (маленький кусочек) (done)

world1 = World(10, 10)
world1.add_robot(5, 5)
world1.get_robot_list()
print()
while True:
    print(world1.get_robot_list())
    world1.draw_map()
    world1.step()
    world1.get_robot_list()
    print()
    time.sleep(2)
