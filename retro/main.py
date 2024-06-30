import pyray
from pyray import *

import math
import os

from scripts.sprite import Sprite
from scripts.animation import Animation
from scripts.anim_manager import AnimManager
from scripts.map import Map

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
print(BASE_PATH)

#  window init
pyray.init_window(0, 0, "Game")
#  pyray.set_target_fps(60)
pyray.set_exit_key(0)

width, height = pyray.get_screen_width(), pyray.get_screen_height()

pyray.toggle_fullscreen()

#  player
player_sp = Sprite("assets/characters", "player.png", BASE_PATH)
player_anim_manager = AnimManager(player_sp, (10, 10, 10, 10, 10, 10, 10, 10, 10, 20), no_loop=["death"])

player_action = "idle_right"
player_last_idle = "down"

player_pos = [width // 2, height // 2]
player_vel = [0, 0]
player_speed = 3.7

rev = False

cam_offset = [0, 0]
image_center = [25, 32]

player_cool_down = 0

#  map
game_map = Map((width, height), BASE_PATH)

# music / sfx
pyray.init_audio_device()

bg_music = pyray.load_sound(os.path.join(BASE_PATH, "assets/bg_music.wav"))
pyray.set_sound_volume(bg_music, 0.5)

while not pyray.window_should_close():
    #  music loop
    if not pyray.is_sound_playing(bg_music):
        pyray.play_sound(bg_music)

    #  delta time
    delta_time = pyray.get_frame_time() * 60

    #  player update
    player_cool_down -= delta_time

    player_vel[0] = 0
    player_vel[1] = 0
    if pyray.is_key_down(KeyboardKey.KEY_D):
        player_vel[0] += 1

    if pyray.is_key_down(KeyboardKey.KEY_A):
        player_vel[0] -= 1

    if pyray.is_key_down(KeyboardKey.KEY_S):
        player_vel[1] += 1

    if pyray.is_key_down(KeyboardKey.KEY_W):
        player_vel[1] -= 1

    if player_vel[0] != 0 or player_vel[1] != 0:
        lenth = math.sqrt(player_vel[0] ** 2 + player_vel[1] ** 2)

        player_vel[0] = player_vel[0] / lenth * player_speed
        player_vel[1] = player_vel[1] / lenth * player_speed

    if pyray.is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and player_cool_down <= 0:
        player_action = "attack_" + player_last_idle
        player_cool_down = 29
        player_anim_manager.class_anims[player_action].frame = 0

    if player_cool_down <= 0:
        player_pos[0] += player_vel[0] * delta_time
        player_pos[1] += player_vel[1] * delta_time

    if player_vel[0] > 0:
        if player_cool_down <= 0:
            player_action = "walk_right"
            player_last_idle = "right"

        rev = False

    elif player_vel[0] < 0:
        if player_cool_down <= 0:
            player_action = "walk_right"
            player_last_idle = "right"

        rev = True

    if player_vel[0] == 0 and player_vel[1] > 0 and player_cool_down <= 0:
        player_action = "walk_down"
        player_last_idle = "down"

    elif player_vel[0] == 0 and player_vel[1] < 0 and player_cool_down <= 0:
        player_action = "walk_up"
        player_last_idle = "up"

    if player_vel[0] == 0 and player_vel[1] == 0 and player_cool_down <= 0:
        player_action = "idle_" + player_last_idle

    if pyray.is_key_pressed(KeyboardKey.KEY_ESCAPE):
        player_cool_down = 60
        player_action = "death"
        player_anim_manager.class_anims[player_action].frame = 0
        player_anim_manager.class_anims[player_action].anim_index = 0

    player_anim_manager.class_anims[player_action].update(delta_time)

    #  cam update
    cam_offset[0] += (player_pos[0] - cam_offset[0] + image_center[0] - width / 2) / 300 * delta_time
    cam_offset[1] += (player_pos[1] - cam_offset[1] + image_center[1] - height / 2) / 150 * delta_time

    pyray.begin_drawing()
    pyray.clear_background(BLACK)
    int_offset = (int(cam_offset[0]), int(cam_offset[1]))

    game_map.render(int_offset, None)

    player_anim_manager.class_anims[player_action].render((int(player_pos[0]), int(player_pos[1])), rev, int_offset)

    pyray.draw_fps(5, 5)

    pyray.end_drawing()

pyray.close_window()
