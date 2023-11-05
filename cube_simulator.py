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

    def get_cube(self) -> Cube:
        return self._cube

    def get_size(self) -> int:
        return self._size

    def get_moves(self) -> list[str]:
        return list(self._moves.keys())

    def perform_moves(self, moves_string: str) -> None:
        """
        Reads the string given and performs all moves on the cube.

        :param moves_string: A string representing a sequence of moves to perform.
            e.g. "RUR'U'" means R U R' U'.
        :raises ValueError: If a modifier is given with no move before it to perform it on,
            or if an invalid character is given.
        """
        stored_move = None
        for char in self._remove_whitespace(moves_string):
            if char == "2":
                if stored_move:
                    self.move_twice(stored_move)
                    stored_move = None
                else:
                    raise ValueError("Typed 2 with nothing/invalid value before it")
            elif char == "'":
                if stored_move:
                    stored_move(prime=True)
                    stored_move = None
                else:
                    raise ValueError("Typed ' with nothing/invalid value before it")
            else:
                if stored_move:
                    stored_move()
                try:
                    stored_move = self._moves[char]
                except KeyError:
                    raise ValueError(f"Invalid character: \"{char}\"")
        if stored_move:
            stored_move()

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

    def display_cube(self) -> None:
        self._cube.display_cube()
