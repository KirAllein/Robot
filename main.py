
class Robot:  # Класс робота

    def __init__(self):
        self.local_map = []
        self.direction = 0
        self.robot_met_obstacle = False
        self.obstacle_coordination = [-1,-1]

    def moving(self, global_x, global_y, local_map):  # функция движения робота
        directions = [[0,-1],[-1,0],[0,1],[1,0]]
        if self.robot_met_obstacle:
            if global_x == self.obstacle_coordination[1] and global_y == self.obstacle_coordination[0]:
                return [0,0]
        if self.robot_met_obstacle:
            self.direction -= 1
            if self.direction < 0:
                self.direction = 3
        x_ch = directions[self.direction][0] + 1
        y_ch = directions[self.direction][1] + 1
        while local_map[y_ch][x_ch] != 0:
            if not self.robot_met_obstacle:
                self.obstacle_coordination = [global_y,global_x]
                self.robot_met_obstacle = True
            self.direction += 1
            if self.direction > 3:
                self.direction = 0
            x_ch = directions[self.direction][0] + 1
            y_ch = directions[self.direction][1] + 1
        return directions[self.direction] # возвращаем измененные значения координат на соответствующую дельту
class World:  # Класс Мира

    def __init__(self, width, length, obstacle=[]):
        self.map = self.create_world(width, length, obstacle)
        self.robot_list = []
        self.field = []

    def create_world(self, width, length, obstacle):
        self.width = width
        self.length = length
        world = [[0] * width for _ in range(length)]  # создаем поле размерами ширина х высота
        for y in range(length):
            for x in range(width):
                if len(obstacle) != 0:
                    if obstacle[0][0] <= x <= obstacle[1][0] and obstacle[0][1] <= y <= obstacle[2][1]:  # рисуем препятствие
                        world[y][x] = 2  # препятствие у нас обозначено 2


        world[2][2] = 2
        world[3][2] = 2
        world[4][2] = 2
        world[5][2] = 2
        world[6][2] = 2
        world[2][4] = 2
        world[3][4] = 2
        world[4][4] = 2
        world[5][4] = 2
        world[6][4] = 2
        world[2][3] = 2

        return world

    def add_robot(self, y, x, world_name):
        robot = [Robot(), y, x]  # добавляем робота в Мир
        if self.map[y][x] == 0: # проверка свободна ли клетка, куда хотим добавить робота
            self.robot_list.append(robot)
        else:
            print('ERROR')


    def draw_map(self):  # Класс рисования Мира
        for i, j in enumerate(self.robot_list):
            self.field = []
            c_y = self.robot_list[i][1]  # координата робота у
            c_x = self.robot_list[i][2]  # координата робота х
            for y in range(len(self.map)):
                row = []
                for x in range(len(self.map[y])):
                    if x == c_x and y == c_y:  # если координаты сошлись на координатах робота, значит здесь робот
                        row.append(1)
                    else:
                        row.append(self.map[y][x])
                self.field.append(row)
        return self.field

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
        robot_map = [[2,2,2],[2,2,2],[2,2,2]]
        global_map = self.map  # запрашиваем глобальную карту
        robot = self.robot_list[robot_num]  # запрашиваем список роботов, откуда возьмем информацию о нужном нам роботе
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
                robot_map[1][1] = 1
        return robot_map



# Список замечаний:
# Поправить отрисовку нескольких роботов
# Научить робота ходить по диагонале
# Подумать над рисовательным фреймоворком
# Распутать Х и У