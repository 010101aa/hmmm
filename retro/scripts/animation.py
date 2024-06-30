import pyray

class Animation():
    def __init__(self, sprite, anim_name, img_dur=5, offset=[0, 0], do_loop=True) -> None:
        self.images = sprite.anims[anim_name]
        self.textures = {}
        self.textures_rev = {}

        self.do_loop = do_loop

        for frame in self.images:
            self.textures.update({frame : pyray.load_texture_from_image(self.images[frame])})

            pyray.image_flip_horizontal(self.images[frame])
            self.textures_rev.update({frame : pyray.load_texture_from_image(self.images[frame])})

            pyray.unload_image(self.images[frame])

        self.img_dur = img_dur
        self.offset = offset

        self.anim_index = 0
        self.frame = 0

    def update(self, delta_time) -> bool:
        if not self.do_loop and self.anim_index == len(self.images) - 1:
            return True

        self.frame += delta_time

        self.anim_index = (self.frame // self.img_dur) % len(self.images)

        return False

    def render(self, pos, reversed, offset) -> None:
        off_x, off_y = offset

        if not reversed:
            pyray.draw_texture(self.textures[self.anim_index], pos[0] - off_x, pos[1] - off_y, pyray.WHITE)

        if reversed:
            pyray.draw_texture(self.textures_rev[self.anim_index], pos[0] - off_x, pos[1] - off_y, pyray.WHITE)
