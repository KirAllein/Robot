import time


class Robot:
    name = None
    robot_position = None
    step = None
    step1 = None
    step2 = None

    def __init__(self):
        self.step1 = None
        self.step2 = None

    def moving(self, robot_position, step1=0, step2=0):
        self.step1 = step1 # шаги робота по у
        self.step2 = step2 # шаги робота по х
        # flag = True
        self.robot_position = robot_position  # изначальная позиция робота
        robot_position = [robot_position[0]-step2, robot_position[1] - step1]  # Движение робота на север, отнимаем от координаты у шаг
        # flag = World.get_robot_position()
        return robot_position # возвращаем позицию робота после шага
    # def get_position(self,):
    #     World.get_robot_position(robot_position)

    # def moving_sideways(self, robot_position, step1=0, step2=0): # движение в сторону
    #     self.step1 = step1  # шаги робота по у
    #     self.step2 = step2 # шаги робота по х
    #     self.robot_position = robot_position  # изначальная позиция робота
    #     robot_position = [robot_position[0]-step2, robot_position[1]-step1]  # Движение робота на запад, отнимаем от координаты х шаг
    #     return robot_position # возвращаем позицию робота после шага


class World:
    coord_y = None
    coord_x = None
    obstacle1 = None
    obstacle2 = None
    obstacle3 = None
    obstacle4 = None

    def __init__(self, coord_x, coord_y, obstacle1, # Важно при инициализации важно не перепутать int и init
                 obstacle2, obstacle3, obstacle4):
        self.set_world(coord_x, coord_y, obstacle1,
                       obstacle2, obstacle3, obstacle4)

    def set_world(self, coord_x, coord_y, obstacle1, obstacle2, obstacle3, obstacle4):  # Создание мира
        self.coord_y = coord_y  # координата у
        self.coord_x = coord_x  # координата х
        self.obstacle1 = obstacle1  # верхний левый угол препятствия
        self.obstacle2 = obstacle2  # верхний правый угол препятсвия
        self.obstacle3 = obstacle3  # нижний левый угол препятсвия
        self.obstacle4 = obstacle4  # нижний правй угол препятствия
        robot1 = Robot()
        world = [['x'] * coord_x for _ in range(coord_y)]  # Тут прикол был: я сначала написал world = [['x']*coord_x] * coord_y.
        # А это оказывается создает ссылки на один и тот же вложенный список и если меняю 1 элемент в одном списке,
        # то соответствующие элементы во всех других списках тоже меняются.
        # А надо писать либо как сейчас написано, либо world = [['x' for _ in range(n)] for _ in range(n)]
        n = 0 # переменная, куда значения шага будем класть. -1 сначала, чтобы робота в начальной позиции обозначить
               # и после 1 шага робот сдвинулся на 0
        m = 0
        flag = True # флаг, по которому будем подолжать или останавливать движение
        for _ in range(17): # пока флаг передает истину
            robot_position = robot1.moving([4, 9], n, m) # задаем начальные координаты робота
            for y in range(coord_y):
                for x in range(coord_x):
                    if obstacle1[0] <= x <= obstacle2[0] and obstacle1[1] <= y <= obstacle3[1]: # отталкиваясь от углов препятствия,
                                                                                                # рисуем само препятсвие
                        world[y][x] = 'O'  # Рисуем препятствие
                    elif x == robot_position[0] and y == robot_position[1]: # проверяем совпадение координат робота
                        world[y][x] = 'K' # Находим робота
                        if world[robot_position[1]-1][x] == 'O': # проверка не уперся ли робот в препятсвие
                            p = robot_position
                            m += 1
                           # flag = False # если уперся, то останавливаем движение
                        elif world[y][robot_position[0]+1] == 'O': # проверяем есть ли препятствие справа
                            n += 1
                        elif [robot_position[0]+1, robot_position[1]+1] == obstacle1 or world[robot_position[1]+1][x] == 'O':
                            m -= 1
                        else:
                            n += 1  # инициализируем переменную шага и обозначаем, что каждую итерацию она будет увеличиваться на 1
                    else:
                        world[y][x] = 'x' # Обычная клетка поля
            for row in world:
                print(*row)  # выводим Мир построчно
            print(f'____________{robot_position}____________') # отделяем миры чертой
            time.sleep(2) # пауза, чтобы вывод сразу не уезжал

    # def get_world(self, coord_x, coord_y, obstacle1, obstacle2, obstacle3, obstacle4):
    #     for row in self.set_world(coord_x, coord_y, obstacle1, obstacle2, obstacle3, obstacle4):
    #         print(*row)

    # def get_robot_position(self):
    #     robot1 = Robot()
    #     robot_position = robot1.moving([4, 9])
    #     robot_position = robot_position
    #     world = self.set_world(10, 10, [3, 2], [5, 2], [3, 4], [5, 4])
    #     flag = True
    #     for i in world:
    #         for j in i:
    #             if j == 'O':
    #                 if robot_position[1] - 1 == i.index(j):
    #                     flag = False
    #     return flag


world1 = World(10, 10, [3, 2], [5, 2], [3, 4], [5, 4])





# robot1 = Robot()
# robot1.moving([4, 9], 1)

# world1.get_world(10, 10, [3, 2], [5, 2], [3, 4], [5, 4], [4, 9])

# steps = 0
# coord_x = 10
# coord_y = 10
#
# obstacle = ([3, 2], [5, 2], [3, 4], [5, 4])
# flag = True
#
# while flag:
#     steps += 1
#     robot = [4, 10 - steps]
#     for y in range(coord_y):
#         for x in range(coord_x):
#             if y == robot[1] and x == robot[0]:
#                 print('K', end=' ')
#                 if robot[1] == obstacle[3][1]+1:
#                     flag = False
#             elif obstacle[0][0] <= x <= obstacle[1][0] and obstacle[0][1] <= y <= obstacle[2][1]:
#                 print('O', end=' ')
#             else:
#                 print('x', end=' ')
#         print()
#     print(f'-----------------{steps}---------------------------')
#     time.sleep(3)

# for y in range(coord_y):
#     for x in range(coord_x):
#         if y == 9 and x == (y + 1) / 2 - 1:
#             print('K', end=' ')
#             robot = [x, y]
#         elif obstacle[0][0] <= x <= obstacle[1][0] and obstacle[0][1] <= y <= obstacle[2][1]:
#             print('O', end=' ')
#         else:
#             print('x', end=' ')
#     print()
# print('--------------------------------------------')
# time.sleep(3)
