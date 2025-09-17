import time


class Robot:


    def __init__(self):
        pass

    def moving(self, p_x, p_y, local_map):
        d_x = 0
        d_y = 1
        return d_x, d_y

# Роботу на основании полученных данных прнимать решение, куда идти


class World:

    def __init__(self, width, lenght):
        self.map = [[0] * width for _ in range(lenght)]
        self.robot_list = []

    def add_robot(self, x,y):
         robot = [Robot(),x,y]
         self.robot_list.append(robot)

    def draw_map(self):
        for row in self.map:
            print(*row)

    def get_robot_list(self):
        print(self.robot_list)

    def step(self):
        for r in self.robot_list:
            x = r[1]
            y = r[2]
            d_x, d_y = r[0].moving(x, y, None)
            r[1] += d_x
            r[2] += d_y

# реализовать, чтобы он не убегал за края карты, в рамках step
# И чтобы робот не втыкался в препятсвия
# Передавать роботу локальную карту (маленький кусочек)

world1 = World(10, 10)
world1.add_robot(5,5)
world1.draw_map()
world1.get_robot_list()
for i in range(3):
    world1.step()
    world1.get_robot_list()


