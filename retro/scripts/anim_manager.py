from scripts.sprite import Sprite
from scripts.animation import Animation

class AnimManager():
    def __init__(self, sprite, img_durs=None, ofsets=None, no_loop=[]) -> None:
        self.anims = sprite.anims

        if img_durs == None:
            img_durs = [10 for _ in range(len(self.anims))]

        if ofsets == None:
            ofsets = [[0, 0] for _ in range(len(self.anims))]

        self.class_anims = {}
        for index, anim in enumerate(self.anims):
            do_loop = True
            if anim in no_loop:
                do_loop = False

            self.class_anims.update({anim : Animation(sprite, anim, img_durs[index], ofsets[index], do_loop)})
