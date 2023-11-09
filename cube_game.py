from typing import Type
from abc import ABC, abstractmethod
import os
import random

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

    UI_WIDTH = 60
    HORIZONTAL_BORDER = "=" * UI_WIDTH

    QUIT_KEY = "Q"
    RESET_KEY = "W"
    SCRAMBLE_KEY = "O"
    UNDO_KEY = "P"
    HISTORY_KEY = "H"
    SHOW_INVERSE_KEY = "G"
    TOGGLE_CASE_KEY = "T"

    MOVES_INSTRUCTION = "Type in a sequence of moves and press ENTER"

    SCRAMBLE_MOVE_COUNT = 22

    def __init__(self, simulator_subclass: Type[CubeSimulator], cube_subclass: Type[Cube]) -> None:
        """
        Initialises the game.
        The Cube subclass provided should be able to display a cube via console text output.
        """
        super().__init__(simulator_subclass, cube_subclass)
        self._message: str = ""
        self._is_case_toggled: bool = False
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

        elif user_input_upper == CubeGame2D.SCRAMBLE_KEY:
            self._scramble()

        elif user_input_upper == CubeGame2D.UNDO_KEY:
            self._undo_sequence()

        elif user_input_upper == CubeGame2D.HISTORY_KEY:
            self._display_history()

        elif user_input_upper == CubeGame2D.TOGGLE_CASE_KEY:
            self._is_case_toggled = not self._is_case_toggled

        elif user_input_upper == CubeGame2D.SHOW_INVERSE_KEY:
            self._show_inverse_sequence()

        else:
            self._perform_moves(user_input)

    def _undo_sequence(self) -> None:
        previous_moves_sequence = self._simulator.get_previous_moves_sequence()
        if previous_moves_sequence is not None:
            previous_moves_sequence = "".join(previous_moves_sequence)
            inverse_sequence = self._simulator.undo_moves_sequence()
            self._message = f"Previous moves sequence {previous_moves_sequence} reverted using {inverse_sequence}"
        else:
            self._message = "No move sequence to undo"

    def _display_history(self) -> None:
        moves_history = self._simulator.get_moves_history()
        self._message = "Moves history:"
        if len(moves_history) > 0:
            for moves_sequence in moves_history:
                self._message += "\n- " + "".join(moves_sequence)
        else:
            self._message += "\n-"

    def _show_inverse_sequence(self) -> None:
        """ Displays the inverse of the most recent sequence. """
        previous_sequence = self._simulator.get_previous_moves_sequence()
        if previous_sequence is not None:
            previous_sequence_string = "".join(previous_sequence)
            inverse_sequence = self._simulator.get_inverse_sequence(previous_sequence)
            self._message = f"Inverse of {previous_sequence_string}: {inverse_sequence}"
        else:
            self._message = "There is no previous sequence to show the inverse of"

    def _perform_moves(self, moves_string: str) -> None:
        if self._is_case_toggled:
            moves_string = moves_string.swapcase()

        try:
            self._simulator.perform_moves(moves_string)
        except ValueError as e:
            self._message = e  # An error message will be printed next time the screen is displayed

    def _scramble(self) -> None:
        scramble_sequence = ""
        for _ in range(self.SCRAMBLE_MOVE_COUNT):
            random_move: str = random.choice(self._simulator.get_moves())
            random_move += random.choice(["", "'", "2"])
            scramble_sequence += random_move
        self._simulator.perform_moves(scramble_sequence, record=False)
        self._message = "Cube scrambled"

    def _display_title(self) -> None:
        size = self._simulator.get_size()
        print(CubeGame2D.HORIZONTAL_BORDER)
        print(f"Rubik's Cube Simulator {size}x{size}")
        print(CubeGame2D.HORIZONTAL_BORDER)

    def _display_options(self) -> None:
        print("OPTIONS:")
        toggle_case_state = "X" if self._is_case_toggled else " "
        option_width = (self.UI_WIDTH // 2) - 3
        print("| " + f"[{self.QUIT_KEY}]: Quit".ljust(option_width)
              + "| " + f"[{self.RESET_KEY}]: Reset cube".ljust(option_width) + "|")
        print("| " + f"[{self.SCRAMBLE_KEY}]: Scramble cube".ljust(option_width)
              + "| " + f"[{self.UNDO_KEY}]: Undo last sequence".ljust(option_width) + "|")
        print("| " + f"[{self.HISTORY_KEY}]: Show moves history".ljust(option_width)
              + "| " + f"[{self.SHOW_INVERSE_KEY}]: Show inverse sequence".ljust(option_width) + "|")
        print("| " + f"[{self.TOGGLE_CASE_KEY}]: Toggle case [{toggle_case_state}]".ljust(option_width) + "|")

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
            most_recent_moves_sequence = self._simulator.get_previous_moves_sequence()
            if most_recent_moves_sequence is not None:
                self._message = "Last move: " + "".join(most_recent_moves_sequence)
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

