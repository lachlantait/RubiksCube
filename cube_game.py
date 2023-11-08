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

    HORIZONTAL_BORDER = "=" * 60

    QUIT_KEY = "Q"
    RESET_KEY = "W"
    UNDO_KEY = "P"
    HISTORY_KEY = "H"
    TOGGLE_CASE_KEY = "T"

    MOVES_INSTRUCTION = "Type in a sequence of moves and press ENTER"

    def __init__(self, simulator_subclass: Type[CubeSimulator], cube_subclass: Type[Cube]) -> None:
        """
        Initialises the game.
        The Cube subclass provided should be able to display a cube via console text output.
        """
        super().__init__(simulator_subclass, cube_subclass)
        self._is_case_toggled: bool = False
        self._message: str = ""
        self._has_quit: bool = False

    def play_game(self) -> None:
        while not self._has_quit:
            self._clear_screen()
            self._display_title()
            self._simulator.display_cube()
            print(CubeGame2D.HORIZONTAL_BORDER)
            self._display_options()
            print(CubeGame2D.HORIZONTAL_BORDER)
            self._display_moves()
            print(CubeGame2D.HORIZONTAL_BORDER)
            self._display_message()
            self._take_action()

    def _take_action(self) -> None:
        """ Get user input and take the appropriate action. """
        user_input = input("\n> ")
        user_input_upper = user_input.upper()

        if user_input_upper == CubeGame2D.QUIT_KEY:
            self._has_quit = True
            print()

        elif user_input_upper == CubeGame2D.RESET_KEY:
            self._simulator.reset_cube()
            self._message = "Cube reset"

        elif user_input_upper == CubeGame2D.UNDO_KEY:
            previous_moves_sequence = self._simulator.get_most_recent_moves_sequence()
            self._simulator.undo_moves_sequence()
            self._message = "Previous moves sequence reverted: " + previous_moves_sequence

        elif user_input_upper == CubeGame2D.HISTORY_KEY:
            moves_history = self._simulator.get_moves_history()
            self._message = "Moves history:"
            if len(moves_history) > 0:
                for moves_sequence in moves_history:
                    self._message += "\n- " + moves_sequence
            else:
                self._message += "\n-"

        elif user_input_upper == CubeGame2D.TOGGLE_CASE_KEY:
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
        # TODO: Have options lined up
        print(f"| [{CubeGame2D.QUIT_KEY}]: Quit "
              f"| [{CubeGame2D.RESET_KEY}]: Reset cube |")
        print(f"| [{CubeGame2D.UNDO_KEY}]: Undo last sequence "
              f"| [{CubeGame2D.HISTORY_KEY}]: Show moves history |")
        print(f"| [{CubeGame2D.TOGGLE_CASE_KEY}]: Toggle case [{toggle_case_state}] |")

    def _display_moves(self) -> None:
        print("MOVES:")
        for modifier in [" ", "'", "2"]:
            output = ""
            for move in self._simulator.get_moves():
                output += move + modifier + " "
            print(output)

    def _display_message(self) -> None:
        """ Displays the message that is currently set, then clears it. """
        if self._message == "":
            most_recent_moves_sequence = self._simulator.get_most_recent_moves_sequence()
            if most_recent_moves_sequence is not None:
                self._message = "Last move: " + most_recent_moves_sequence
            else:
                self._message = CubeGame2D.MOVES_INSTRUCTION
        print(self._message)
        self._message = ""

    @staticmethod
    def _clear_screen() -> None:
        os.system("cls" if os.name == "nt" else "clear")


if __name__ == '__main__':
    from cube_simulator_3x3 import CubeSimulator3x3
    from cube_text_ui_2d import CubeTextUI2D

    game = CubeGame2D(CubeSimulator3x3, CubeTextUI2D)
    game.play_game()

