from typing import Type, Callable

from cube import Cube


class CubeSimulator:
    """
    Abstract class for a Rubik's Cube simulator.
    Provides an interface for performing moves on a cube.

    Subclasses should each have their own cube size and list of moves that can be performed on the cube.
    Moves should be implemented by having the subclass overwrite self._moves to contain keys that are a single-character
    string representing the move, and a function that performs that move. e.g. "U": self.move_U
    All such functions should have a keyword argument named "prime" to perform the 'prime' version of that move.

    This class itself cannot be instantiated, only its subclasses. This is enforced manually in __init__.
    """

    def __init__(self, cube_subclass: Type[Cube], size: int = 0) -> None:
        """
        Initialises the cube using the Cube subclass and the size given.
        Cube subclasses can each have their own method of displaying the cube.

        :raises TypeError: If called on CubeSimulator and not from a subclass.
        """
        if type(self) is CubeSimulator:
            raise TypeError(f"Only {type(self).__name__} subclasses may be instantiated")
        self._cube: Cube = cube_subclass(size)
        self._size: int = size
        self._moves: dict[str, Callable] = {}
        self._moves_history: list[list[str]] = []

    def get_cube(self) -> Cube:
        return self._cube

    def get_size(self) -> int:
        return self._size

    def get_moves(self) -> list[str]:
        """ Returns the list of moves that can be performed (without modified versions e.g. U' and U2). """
        return list(self._moves.keys())

    def get_moves_history(self) -> list[list[str]]:
        return self._moves_history

    def get_previous_moves_sequence(self) -> list[str] | None:
        if len(self._moves_history) > 0:
            return self._moves_history[-1]
        return None

    def perform_moves(self, moves_string: str, *, record: bool = True) -> None:
        """
        Reads the string given and performs all moves on the cube.

        :param moves_string: A string representing a sequence of moves to perform.
            e.g. "RUR'U'" means R U R' U'.
        :param record: An optional keyword argument. If True, records the sequence in the history. Defaults to True.
        :raises ValueError: If a modifier is given with no move before it to perform it on,
            or if an invalid character is given.
        """
        stored_move = None
        stored_char: str | None = None
        moves_list: list[str] = []
        for char in self._remove_whitespace(moves_string):
            if char == "2":
                if stored_move:
                    self.move_twice(stored_move)
                    moves_list.append(stored_char + char)
                    stored_move = None
                    stored_char = None
                else:
                    raise ValueError("Typed 2 with nothing/invalid value before it")
            elif char == "'":
                if stored_move:
                    stored_move(prime=True)
                    moves_list.append(stored_char + char)
                    stored_move = None
                    stored_char = None
                else:
                    raise ValueError("Typed ' with nothing/invalid value before it")
            else:
                if stored_move:
                    stored_move()
                    moves_list.append(stored_char)
                try:
                    stored_move = self._moves[char]
                    stored_char = char
                except KeyError:
                    raise ValueError(f"Invalid character: \"{char}\"")
        if stored_move:
            stored_move()
            moves_list.append(stored_char)
        if record and len(moves_list) > 0:
            self._moves_history.append(moves_list)

    @staticmethod
    def _remove_whitespace(input_str: str) -> str:
        whitespace_chars = [" ", "\t"]
        output_str = ""
        for char in input_str:
            if char not in whitespace_chars:
                output_str += char
        return output_str

    @staticmethod
    def move_twice(move: Callable) -> None:
        move()
        move()

    def undo_moves_sequence(self) -> str:
        """
        Undoes the most recent sequence of moves.

        :return: The sequence of moves used to undo the most recent sequence, as a string.
        :raises ValueError: If there is no moves sequence left to undo.
        """
        if len(self._moves_history) == 0:
            raise ValueError("No moves sequence to undo.")
        previous_moves_sequence: list[str] = self._moves_history.pop()
        inverse_sequence = self.get_inverse_sequence(previous_moves_sequence)
        self.perform_moves(inverse_sequence, record=False)
        return inverse_sequence

    @staticmethod
    def get_inverse_sequence(moves_sequence: list[str]) -> str:
        """
        Reads the moves sequence given and returns the sequence needed to undo that sequence.

        :param moves_sequence: A list of strings representing individual moves
        :return: A string of moves, in the same format that could be passed to self.perform_moves
        """
        inverse_sequence = ""
        for i in range(len(moves_sequence) - 1, -1, -1):
            move: str = moves_sequence[i]
            if len(move) == 1:
                inverse_sequence += move + "'"
            elif move[1] == "'":
                inverse_sequence += move[0]
            elif move[1] == "2":
                inverse_sequence += move
        return inverse_sequence

    def display_cube(self) -> None:
        self._cube.display_cube()

    def reset_cube(self) -> None:
        self._cube.reset()
        self._moves_history.clear()
