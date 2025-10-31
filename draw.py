import matplotlib.pyplot as plt
import matplotlib.animation as animation
import main
from PIL import Image


world1 = main.World(map='map.bmp')
# world1.add_robot(9,3, world1)
# world1.add_robot(7,3, world1)
# world1.add_robot(5,3, world1)




plt.ion() # обновление графика в реальном времени
fig, ax = plt.subplots() # создаем рисунок и координатную плоскость
frames = [] # сюда мобираем каждый кадр

for i in range(45):
    world1.step() # Вызов шага, чтобы изменить положение робота
    img = ax.imshow(world1.draw_map(), cmap='Blues', animated = True) # преобразование матрицы в картинку
    frames.append([img]) # сохраняем кадр
    plt.pause(1)

ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True) # создание гиф файла
ani.save('robot_moving.gif', writer='pillow') # Сохранение гиф файла
