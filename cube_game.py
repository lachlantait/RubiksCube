from typing import Type
from abc import ABC, abstractmethod
import os

from cube_simulator import CubeSimulator
from cube import Cube


class CubeGame(ABC):
    """ Abstract interface for a Rubik's Cube simulator game. """

    def __init__(self, simulator_subclass: Type[CubeSimulator], cube_subclass: Type[Cube]) -> None:
        self._simulator: CubeSimulator = simulator_subclass(cube_subclass)

    @abstractmethod
    def play_game(self) -> None:
        raise NotImplementedError


class CubeGame2D(CubeGame):
    """ Rubik's Cube simulator game with a text-based, console user-interface. """

    HORIZONTAL_BORDER = "=" * 55

    QUIT_KEY = "Q"
    RESET_KEY = "W"
    TOGGLE_CASE_KEY = "T"

    def __init__(self, simulator_subclass: Type[CubeSimulator], cube_subclass: Type[Cube]) -> None:
        """
        Initialises the game.
        The Cube subclass provided should be able to display a cube via console text output.
        """
        super().__init__(simulator_subclass, cube_subclass)
        self._is_case_toggled: bool = False
        self._message: str = ""

    def play_game(self) -> None:
        has_quit = False
        while not has_quit:
            self._clear_screen()
            self._display_title()
            self._simulator.display_cube()
            print(CubeGame2D.HORIZONTAL_BORDER)
            self._display_options()
            print(CubeGame2D.HORIZONTAL_BORDER)
            self._display_moves()
            print(CubeGame2D.HORIZONTAL_BORDER)
            print(self._message)
            self._message = ""
            user_input = input("> ")
            if user_input.upper() == CubeGame2D.QUIT_KEY:
                has_quit = True
                print()
            elif user_input.upper() == CubeGame2D.RESET_KEY:
                self._simulator.get_cube().reset()
                self._message = "Cube reset"
            elif user_input.upper() == CubeGame2D.TOGGLE_CASE_KEY:
                self._is_case_toggled = not self._is_case_toggled
            else:
                self._perform_moves(user_input)

    def _perform_moves(self, moves_string: str) -> None:
        if self._is_case_toggled:
            moves_string = moves_string.swapcase()

        try:
            self._simulator.perform_moves(moves_string)
        except ValueError as e:
            self._message = e  # An error message will be printed next time the screen is displayed

    def _display_title(self) -> None:
        size = self._simulator.get_size()
        print(CubeGame2D.HORIZONTAL_BORDER)
        print(f"Rubik's Cube Simulator {size}x{size}")
        print(CubeGame2D.HORIZONTAL_BORDER)

    def _display_options(self) -> None:
        print("OPTIONS:")
        toggle_case_state = "X" if self._is_case_toggled else " "
        print(f"| [{CubeGame2D.QUIT_KEY}]: Quit | [{CubeGame2D.RESET_KEY}]: Reset cube |")
        print(f"| [{CubeGame2D.TOGGLE_CASE_KEY}]: Toggle case [{toggle_case_state}] |")

    def _display_moves(self) -> None:
        print("Type in a sequence of moves and press ENTER")

        print("\nMoves:")
        for modifier in [" ", "'", "2"]:
            output = ""
            for move in self._simulator.get_moves():
                output += move + modifier + " "
            print(output)

    @staticmethod
    def _clear_screen() -> None:
        os.system("cls" if os.name == "nt" else "clear")


if __name__ == '__main__':
    from cube_simulator_3x3 import CubeSimulator3x3
    from cube_text_ui_2d import CubeTextUI2D

    game = CubeGame2D(CubeSimulator3x3, CubeTextUI2D)
    game.play_game()

