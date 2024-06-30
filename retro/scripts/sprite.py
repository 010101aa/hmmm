import pyray
import os

class Sprite():
    def __init__(self, dir, file, base_bath) -> None:
        self.dir = dir
        self.file = file

        #  load config file
        self.dir_config = None
        with open(os.path.join(base_bath, self.dir, "sp_config.txt"), "r") as file:
            self.dir_config = eval(file.read())

        self.config = self.dir_config[self.file]

        # load images
        self.sprite_image = pyray.load_image(os.path.join(base_bath, self.dir, self.file))

        self.anims = {}
        for anim in self.config["anims"]:
            self.anims.update({anim : {}})

            frames = self.config["anims"][anim][1] - self.config["anims"][anim][0]
            for f_index, frame in enumerate(range(frames)):
                frame_image = pyray.image_copy(self.sprite_image)
                pyray.image_crop(frame_image, (f_index * self.config["grid"][0],
                                               self.config["anims"][anim][2] * self.config["grid"][1],
                                               self.config["grid"][0],
                                               self.config["grid"][1]))
                
                pyray.image_resize_nn(frame_image, 
                                      self.config["grid"][0] * 4,
                                      self.config["grid"][1] * 4)

                self.anims[anim].update({f_index : frame_image})
