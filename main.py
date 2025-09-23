import time
import random


class Robot:

    def __init__(self):
        self.local_map = []

    def moving(self, s_x, p_y):
        local_map = self.look_around()
        delta_x = -1
        delta_y = 0
        d_x = 0
        d_y = 0
        return d_x + delta_x, d_y + delta_y

    def look_around(self):
        self.local_map = []
        global_map = world1.map
        robot = world1.get_robot_list()
        for y in range(len(global_map)):
            row = []
            row_c = []
            for x in range(len(global_map[y])):
                if y in range(robot[0][1] - 1, robot[0][1] + 2) and x in range(robot[0][2] - 1, robot[0][2] + 2):
                    if y == robot[0][1] and x == robot[0][2]:
                        row.append(1)
                        row_c.append([x, y])
                    else:
                        row.append(global_map[y][x])
                        row_c.append([x, y])
            if len(row) != 0:
                self.local_map.append(row)
                self.local_map.append(row_c)
        return self.local_map


# Робот на основании полученных данных прнимает решение, куда идти


class World:

    def __init__(self, width, length):
        self.map = [[0] * width for _ in range(length)]
        self.robot_list = []
        self.obstacle = []

    def add_robot(self, x, y):
        robot = [Robot(), x, y]
        self.robot_list.append(robot)

    def draw_map(self):
        c_y = self.robot_list[0][1]
        c_x = self.robot_list[0][2]
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if x == c_x and y == c_y:
                    print(1, end=' ')
                else:
                    print(self.map[y][x], end=' ')
            print()

    def get_robot_list(self):
        return self.robot_list

    def step(self):
        for r in self.robot_list:
            print(*r[0].look_around())
            y = r[1]
            x = r[2]
            d_x, d_y = r[0].moving(x, y)
            if 1 <= y <= len(self.map)-2 and 1 <= x <= len(self.map[0])-2:  # Сравниваем координаты робота и размеры Мира, чтобы не выйти за его пределы
                r[1] += d_y
                r[2] += d_x
            else:
                print(x)
                exit()



# реализовать, чтобы он не убегал за края карты, в рамках step (done)
# И чтобы робот не втыкался в препятсвия
# Передавать роботу локальную карту (маленький кусочек) (done)

world1 = World(10, 10)
world1.add_robot(5, 5)
world1.get_robot_list()
print()
for i in range(7):
    print(world1.get_robot_list())
    world1.draw_map()
    world1.step()
    world1.get_robot_list()
    print()
    time.sleep(1)
