from PIL import Image
from outils import UNIT_SIZE


with open("ressources/textures/plateau.txt", "r") as file:
    texte = file.readlines()
    rep = []

    for line in texte:
        temp = []
        for char in line[:-1]:
            if char == "M":
                temp += [1]
            else:
                temp += [0]

        rep.append(temp)

size = (len(rep), len(rep[0]))

width = size[1]*UNIT_SIZE
height = size[0]*UNIT_SIZE

img = Image.new(mode="RGB", size=(width, height))


for x in range(size[1]):
    for y in range(size[0]):
        if rep[y][x] == 1:
            for i in range(UNIT_SIZE):
                for j in range(UNIT_SIZE):
                    img.putpixel(
                        (x*UNIT_SIZE + j, y*UNIT_SIZE + i), (0, 0, 255))

img.show()
img.save('ressources/textures/plateau.jpg')
