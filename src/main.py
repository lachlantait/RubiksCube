""" Starts the game! """

__author__ = "Lachlan Tait"

from src.cube_text_ui_2d import CubeTextUI2D
from src.cube_simulator_3x3 import CubeSimulator3x3
from src.cube_game import CubeGame2D

if __name__ == '__main__':
    game = CubeGame2D(CubeSimulator3x3, CubeTextUI2D)
    game.play_game()
