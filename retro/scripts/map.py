import pyray
import random

import os

random.seed(0)

def load_image(path) -> pyray.Texture:
    image = pyray.load_image(path)
    pyray.image_resize_nn(image, image.width * 4, image.height * 4)

    return pyray.load_texture_from_image(image)

class Map():
    def __init__(self, screen_size, base_path) -> None:
        self.grid_size = 64

        self.screen_size = screen_size

        self.assets = {
            "grass" : load_image(os.path.join(base_path, "assets/tilesets/grass.png")),
            "decor_grass" : load_image(os.path.join(base_path, "assets/tilesets/decor_16x16 Kopie.png"))
        }

        #  grid_pos : {"type" : "grass", "decor" : False}
        self.map = {}

        for x in range(100):
            for y in range(100):
                self.map.update({(x, y) : {"type" : "grass", "decor" : False}})

                if random.random() > 0.8:
                    self.map[(x, y)].update({"decor" : True})

    def render(self, offset, player) -> None:
        off_x, off_y = offset

        for pos in self.map:
            pix_size = (pos[0] * self.grid_size - off_x, pos[1] * self.grid_size - off_y)

            if pix_size[0] > self.screen_size[0] + self.grid_size * 2 or pix_size[0] < -self.grid_size:
                continue
                pass

            if pix_size[1] > self.screen_size[1] + self.grid_size * 2 or pix_size[1] < -self.grid_size:
                continue
                pass

            tile = self.map[pos]
            pyray.draw_texture(self.assets[tile["type"]], pix_size[0], pix_size[1], pyray.WHITE)

            if tile["decor"]:
                decor_name = "decor_" + tile["type"]
                pyray.draw_texture(self.assets[decor_name], pix_size[0], pix_size[1], pyray.WHITE)
