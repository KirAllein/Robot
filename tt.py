world = [['x' for _ in range(3)] for _ in range(3)]
world[1][1] = 'L'
world[1][0] = 'L'
world[2][1] = 'L'
print(world)
coord = []

for i in world:
    for j in i:
        if j == 'L':
            coord.append([world.index(i),i.index(j)])
print(coord)