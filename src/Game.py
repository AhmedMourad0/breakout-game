import time

from OpenGL.raw.GLUT import glutWarpPointer

from src.LevelsLoader import load_levels
from src.model.core.Ball import Ball
from src.model.core.Bat import Bat
from src.model.core.Mouse import Mouse
from src.model.core.Player import Player
from src.model.core.Wall import Wall
from src.model.core.Window import Window

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_INSETS = 20


def create_window():
    return Window(WINDOW_WIDTH, WINDOW_HEIGHT, Wall.bottomless(WINDOW_INSETS))


BAT_WIDTH = 100
BAT_HEIGHT = 10
# this doesn't matter because the mouse motion detector is instantly called when the app is launched
BAT_INITIAL_X = 0
BAT_Y = 50


def create_bat():
    return Bat(BAT_INITIAL_X, BAT_Y, BAT_WIDTH, BAT_HEIGHT)


BALL_LENGTH = 16
BALL_INITIAL_X = 100
BALL_INITIAL_Y = 100
BALL_DELTA_X = 5
BALL_DELTA_Y = 5
BALL_INITIAL_IS_GLUED_TO_BAT = 3


def create_ball(window):
    return Ball(
        window,
        BALL_INITIAL_X,
        BALL_INITIAL_Y,
        BALL_LENGTH,
        BALL_DELTA_X,
        BALL_DELTA_Y,
        BALL_INITIAL_IS_GLUED_TO_BAT
    )


PLAYER_INITIAL_SCORE = 0
PLAYER_INITIAL_LIVES = 5


def create_player(is_in_infinite_lives_mode, score=PLAYER_INITIAL_SCORE):
    if is_in_infinite_lives_mode:
        return Player.infinite_lives(score)
    else:
        return Player.limited_lives(score, PLAYER_INITIAL_LIVES)


def create_mouse(window, bat):
    mouse_initial_x = window.inner.horizontal_center()
    mouse_initial_y = window.inner.vertical_center()
    mouse_x_lower_limit = window.inner.left + bat.width() / 2
    mouse_x_upper_limit = window.inner.right - bat.width() / 2

    return Mouse(
        mouse_initial_x,
        mouse_initial_y,
        mouse_x_lower_limit,
        mouse_x_upper_limit,
        glutWarpPointer
    )


class Game:

    def __init__(self):
        self.window = create_window()
        self._is_in_infinite_lives_mode = False
        self.bat = create_bat()
        self.ball = create_ball(self.window)
        self.player = create_player(self._is_in_infinite_lives_mode)
        self.all_levels = load_levels()
        self.current_level = self.all_levels[0]
        self.fleet = self.current_level.create_fleet(self.window)
        self.mouse = create_mouse(self.window, self.bat)
        self.last_slide_down_time = time.time()
        self.time_interval = 1
        self.is_paused = False
        self.time_of_pause = 0

    def set_in_infinite_lives_mode(self, is_in_infinite_lives_mode):
        if self._is_in_infinite_lives_mode != is_in_infinite_lives_mode:
            self._is_in_infinite_lives_mode = is_in_infinite_lives_mode
            self.player = create_player(is_in_infinite_lives_mode, score=self.player.score)

    def is_in_infinite_lives_mode(self):
        return self._is_in_infinite_lives_mode

    def has_won(self):
        return self.fleet.is_destroyed() and self.current_level.is_last_level(self.all_levels)

    def should_move_to_next_level(self):
        return self.fleet.is_destroyed() and not self.current_level.is_last_level(self.all_levels)

    def has_lost(self):
        return not self.player.has_remaining_lives()

    def has_finished(self):
        return self.has_won() or self.has_lost()

    def move_to_next_level(self):
        self._move_to_level(self.current_level.index + 1)

    def move_to_previous_level(self):
        self._move_to_level(self.current_level.index - 1)

    def restart_from_first_level(self):
        self._move_to_level(0)
        self.player = create_player(self._is_in_infinite_lives_mode)

    def _move_to_level(self, level_index):
        self.current_level = self.all_levels[level_index]
        self.fleet = self.current_level.create_fleet(self.window)
        self.last_slide_down_time = time.time()
        self.ball = create_ball(self.window)

    def lose_one_life(self):
        self.ball = create_ball(self.window)
        self.ball.move_one_frame(self.bat)
        self.player.lose_one_life()

    def slide_fleet_down(self):
        if time.time() - self.last_slide_down_time >= self.fleet.slide_down_time_gap:
            self.fleet.slide_down_if_needed()
            self.last_slide_down_time = time.time()

    def pause_or_resume(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.time_of_pause = time.time()
        else:
            elapsed_time_for_slide_down_timer = self.time_of_pause - self.last_slide_down_time
            self.last_slide_down_time = time.time() - elapsed_time_for_slide_down_timer
