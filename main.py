import time


class Robot:  # Класс робота

    def __init__(self):
        self.local_map = []
        self.direction = 0

    def moving(self, global_x, global_y, local_map):  # функция движения робота
        directions = [[0,-1],[-1,0],[0,1],[1,0]]
        x_ch = directions[self.direction][0] + 1
        y_ch = directions[self.direction][1] + 1
        if local_map[y_ch][x_ch] != 0 :
            self.direction += 1
        if self.direction > 3:
            self.direction = 0
        print(self.direction)
        print('___________________________________________________')
        for row in local_map:
            print(*row)
        print(directions[self.direction])
        return directions[self.direction] # возвращаем измененные значения координат на соответствующую дельту

class World:  # Класс Мира

    def __init__(self, width, length, obstacle=[]):
        self.map = self.create_world(width, length, obstacle)
        self.robot_list = []


    def create_world(self, width, length, obstacle):
        self.width = width
        self.length = length
        world = [[0] * width for _ in range(length)]  # создаем поле размерами ширина х высота
        for y in range(length):
            for x in range(width):
                if len(obstacle) != 0:
                    if obstacle[0][0] <= x <= obstacle[1][0] and obstacle[0][1] <= y <= obstacle[2][1]:  # рисуем препятствие
                        world[y][x] = 'X'  # препятствие у нас обозначено буквой х


        world[2][3] = 'X'
        world[2][4] = 'X'
        world[2][5] = 'X'
        world[2][6] = 'X'
        world[2][2] = 'X'
        # world[6][3] = 'X'
        # world[7][3] = 'X'
        # world[4][5] = 'X'
        # world[5][5] = 'X'
        # world[6][5] = 'X'
        # world[7][5] = 'X'


        return world

    def add_robot(self, y, x, world_name):
        robot = [Robot(), y, x]  # добавляем робота в Мир
        if self.map[y][x] == 0: # проверка свободна ли клетка, куда хотим добавить робота
            self.robot_list.append(robot)
        else:
            print('ERROR')


    def draw_map(self):  # Класс рисования Мира
        c_y = self.robot_list[0][1]  # координата робота у
        c_x = self.robot_list[0][2]  # координата робота х
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if x == c_x and y == c_y:  # если координаты сошлись на координатах робота, значит здесь робот
                    print('R', end=' ')
                else:
                    print(self.map[y][x], end=' ')  # в остальных случаях рисуем просто поля Мира
            print()

    def get_robot_list(self):  # функция, чтобы получить список всех роботов
        return self.robot_list

    def step(self):  # функция, где робот делает шаг в Мире
        for i, r in enumerate(self.robot_list):  # обращаемя к списку роботов
            y = r[1]  # изначальна координата у
            x = r[2]  # значальна координата х
            d_x, d_y = r[0].moving(x, y, self.determine_robot_position(i))  # Робот принимает решение о движении
            # Сравниваем координаты робота и размеры Мира, чтобы не выйти за его пределы
            r[1] += d_y  # Передаем новое значение у
            r[2] += d_x  # передаем новое значение х
            print(r[1],r[2])
            if r[1] < 0:
                r[1] = 0
            if r[2] < 0:
                r[2] = 0
            if r[1] >= self.length:
                r[1] = self.length - 1
            if r[2] >= self.width:
                r[2] = self.width - 1  # Не даем роботу выйти за края
            if self.map[r[1]][r[2]] != 0:
                r[1],r[2] = y, x


    def determine_robot_position(self, robot_num):
        robot_map = [['X','X','X'],['X','X','X'],['X','X','X']]
        # Сделать так, чтобы граница карты предствлялась как препятствие и через for заполняем клеточки относительно положения робота
        global_map = world1.map  # запрашиваем глобальную карту
        robot = world1.get_robot_list()[robot_num]  # запрашиваем список роботов, откуда возьмем информацию о нужном нам роботе
        r_x = robot[2]
        r_y = robot[1]
        for y in range(3):
            for x in range(3):
                g_x = r_x - 1 + x
                g_y = r_y - 1 + y
                if g_x < 0:
                    continue
                if g_y < 0:
                    continue
                if g_x >= self.width:
                    continue
                if g_y >= self.length:
                    continue
                robot_map[y][x] = global_map[g_y][g_x]
                robot_map[1][1] = 'R'
        return robot_map


world1 = World(10, 5)
world1.add_robot(4,4, world1)
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
# 1. Робот добавляется на поле препятствия ( поправил)
# 2. Код останавливается, когда робот попадает на край препятствия (поправил)
# 3. Отображается только 1 робот, остальные роботы не отображаются
# 3/1. Нельзя отрисовать Мир без робота
# 4. Препятствие захардкожена в классе Мир. (Fixed)
# 5. Нельзя создать Мир без препятствий (Fixed)
# 6. Локальная карта передается роботу из класса Мир, и робот довольствуется только тем, что ему передано (Done)
# 7. Ошибка при приближении к границе Мира (Done)
# 8. Если доходим до края Мира, это должно восприниматся как препятствие (Done)
# 9. Проверка наличия препятствия ориентирует только на латинскую буквы X (Done)
# 10. Робот не видит дыру в заборе
# 11. Научить робота ходить по диагонале
# 12. Робот проходит сквозь препятствие слева


# 13. Робот проходит сквозь препятствие, если движется по краю (fixed)
# 14. Робот всегда должен знать свои глобальные координаты
# 15. Робот должен двигаться по препятставию в форме П


# 16. Сделать правильное заполнение локальной карты, чтобы всегда три линиии (Done)
# 17. поправить moving. Всегда по локальной карте смотрим, доступность нужного направления и если оно свободно, то двигаемся в нем, если нет
# то перебираем следующие. текущее направление и сначала проверяем свободно ли его. Задача - сохранять текущее направление
# если текущее направление недоступно, то пытаемся повернуть
# 18. При обходе препятствия запоминаем глобальные координаты, когда в первый раз встретил препятствие


# Вернуться к исходному заданию и подумать как это реализовать


