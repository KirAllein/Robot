import copy # импорт модуля копирования

import parse_image # импорт файла для парсинга изображения


class Robot:  # Класс робота

    def __init__(self):
        self.local_map = [] # карта, которую видит робот
        self.direction = 0 # направление движения робота
        self.robot_met_obstacle = False # маркер встречено ли препятсвия
        self.obstacle_coordination = [-1, -1] # координаты места встречи препятствия

    def moving(self, global_x, global_y, local_map):  # функция движения робота. global_x, global_y - глобальные координаты робота на всей карте, local_map - карта, котору видит робот
        directions = [[0, -1], [-1, 0], [0, 1], [1, 0]] # список направлений движения
        count = 0 # счетчик попыток выбрать препятсивие
        if self.robot_met_obstacle: # когда робот встречает препятсвие
            if global_x == self.obstacle_coordination[1] and global_y == self.obstacle_coordination[0]: # если глобальные координаты робота равны координатам встречи с препятствием и робот уже встречал препятствие, т.е. это не в первый раз
                return [0, 0] # робот останавливается и не двигается
        if self.robot_met_obstacle: # Если препятствие было встречено
            self.direction -= 1 # изменение вектора движения
            if self.direction < 0: # если выбрана изначальное направление
                self.direction = 3 # Возврщаемся к последнему
        x_ch = directions[self.direction][0] + 1 # переменная х для проверки
        y_ch = directions[self.direction][1] + 1 # переменная у для проверки
        while local_map[y_ch][x_ch] != 0: # пока на координате, куда хотим сходить свободно
            if not self.robot_met_obstacle: # если робот пока не встретил препятствие
                self.obstacle_coordination = [global_y, global_x]  # место встречи с препятствием приравниваем к глобальным координатам
                self.robot_met_obstacle = True # меняем маркер встречи с препятствием на Правду
            self.direction += 1 # меняем вектор движения на следующий
            if self.direction > 3: # если выбрано последнее направление
                self.direction = 0 # возвращаемся к первому
            x_ch = directions[self.direction][0] + 1 # переменная х для проверки
            y_ch = directions[self.direction][1] + 1 # переменная у для проверки
            count += 1 # Прибвляем 1 к счетчику попыток найти нужное направление
            if count >= 10: # если количество попыток выбрать направление движения превысило 10
                return [0, 0] # робот не двигается
        return directions[self.direction]  # возвращаем измененные значения координат на соответствующую дельту


class World:  # Класс Мира

    def create_from_map(self, image): # функция создания Мира через преобразование картинки
        parser = parse_image.Parse(image) # создаем экземпляр класса Parser
        self.width = parser.width # приравниваем собственную ширину Мира к ширине распарсенной картинки
        self.length = parser.length # то же самое для длинны Мира
        field = parser.parse_image() # получаем результат работы функции parse_image для созданного экземпляра parser
        self.map = [[0] * self.width for _ in range(self.length)]  # создаем поле размерами ширина х, длинна y
        for y in range(self.length):
            for x in range(self.width):
                if field[x][y] == 1 : # когда находим единицу в поле, ставим туда робота
                    self.add_robot(y,x)
                else:
                    self.map[y][x] = field[x][y] # в остальных случаях в карту Мира печатаем клетку полученнго поля из картинки

    def __init__(self, width=None, length=None, obstacle=[], map=None):
        self.robot_list = []
        if map: # если карта уже существует, т.е. была создана из картинки
            self.create_from_map(map)  # создаем Мир, исходя из этой карты
        else: # если нет
            self.map = self.create_world(width, length, obstacle) # создаем Мир исходя из переданных размеров и препятствий
        self.field = self.draw_map() # в любом случае в переменную поля кладем нарисованную карту

    def create_world(self, width, length, obstacle): # функция создания Мира. В нее передам длинну, ширину и координату углов препятствия
        self.width = width
        self.length = length
        world = [[0] * width for _ in range(length)]  # создаем поле размерами ширина х высота у
        for y in range(length):
            for x in range(width):
                if len(obstacle) != 0: # проверяем сущеуствует ли в Мире препятствия
                    if obstacle[0][0] <= x <= obstacle[1][0] and obstacle[0][1] <= y <= obstacle[2][
                        1]:  # рисуем препятствие
                        world[y][x] = 2  # препятствие у нас обозначено 2

        return world

    def add_robot(self, y, x): # функция добавления робота в Мир
        robot = [Robot(), y, x]  # добавляем робота в Мир
        if self.map[y][x] == 0:  # проверка свободна ли клетка, куда хотим добавить робота
            self.robot_list.append(robot)
        else:
            print('ERROR')

    def draw_map(self):  # Класс рисования Мира
        self.field = copy.deepcopy(self.map)  # предаем в переменную собственного поля копию собственной карты, но через deepcope, чтобы был отдельный объект, а не ссылка
        for e, r in enumerate(self.robot_list): # перебираем пронумированный список роботов
            y = r[1] # присваем у первую координату робота
            x = r[2] # присваем х вторую коориднату робота
            self.field[y][x] = 2 + e # добавляем 2 с прибавлением номера робота в Мир, чтобы matplotlib рисовал роботов разными цветам, если их несколько
        return self.field # возвращаем собственное поле

    def get_robot_list(self):  # функция, чтобы получить список всех роботов
        return self.robot_list

    def step(self):  # функция, где робот делает шаг в Мире
        for i, r in enumerate(self.robot_list):  # обращаемя к списку роботов
            y = r[1]  # изначальна координата у
            x = r[2]  # значальна координата х
            self.field = self.draw_map()
            d_x, d_y = r[0].moving(x, y, self.determine_robot_position(i))  # Робот принимает решение о движении
            # Сравниваем координаты робота и размеры Мира, чтобы не выйти за его пределы
            r[1] += d_y  # Передаем новое значение у
            r[2] += d_x  # передаем новое значение х
            if r[1] < 0: # если новое значение у меньше нуля, то есть робот может выйти за пределы карты
                r[1] = 0 # делаем его 0
            if r[2] < 0: # если второе значение меньше 0, то есть робот может выйти за пределы карты
                r[2] = 0 # снова делаем его 0
            if r[1] >= self.length: # сравниваем значение с длинной карты, чтобы оно не было больше или равно
                r[1] = self.length - 1 # Не даем роботу выйти за края сверху
            if r[2] >= self.width:
                r[2] = self.width - 1  # Не даем роботу выйти за края сбоку
            if self.field[r[1]][r[2]] != 0: # проверяем наличие препятствие на поле, куда хотим шагнут. Если препятствие есть
                r[1], r[2] = y, x # Возвращаем прежнее значение координат, т.е. робот не двигается

    def determine_robot_position(self, robot_num):# определяем позицию робота в Мире и передаем ему локальную карту
        robot_map = [[2, 2, 2], [2, 2, 2], [2, 2, 2]] # шаблон карты робота, где везде препятствия
        global_map = self.field  # запрашиваем глобальную карту
        robot = self.robot_list[robot_num]  # запрашиваем список роботов, откуда возьмем информацию о нужном нам роботе
        r_x = robot[2] # х - вторая координата робота
        r_y = robot[1] # у - первая координата робота
        for y in range(3): # перебираем шаблон локальной карты робота
            for x in range(3):
                g_x = r_x - 1 + x # глобальная х = х координата робота + х координата локальной карты
                g_y = r_y - 1 + y # глобальная у = у координата робота + у координата локальной карты
                if g_x < 0: # проверка не входит ли клетка ща пределы глобальной карты, если выходит, то клетка по умолчанию остается со значением 2
                    continue
                if g_y < 0:
                    continue
                if g_x >= self.width:
                    continue
                if g_y >= self.length:
                    continue
                robot_map[y][x] = global_map[g_y][g_x] # добавляем в локальную карту клетку из глобальной карты
                robot_map[1][1] = 1 # центр локальной карты всегда робот
        return robot_map

