from PIL import Image


class Parse:

    def __init__(self, image):
        self.map_image = Image.open(image)
        self.pixels = self.map_image.load()
        self.width, self.length = self.map_image.size

    def parse_image(self):
        field = []
        for y in range(self.length):
            row = [0] * self.width
            print()
            for x in range(self.width):
                px = self.pixels[y, x]
                if px == (0, 0, 0):
                    row[x] = 2
                elif px == (255, 255, 255):
                    row[x] = 0
                else:
                    row[x] = 1
            field.append(row)
        return field

# разберись как оно работает. Написать комментарии
