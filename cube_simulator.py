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

    def __init__(self, cube_subclass: Type[Cube], size: int) -> None:
        """
        Initialises the cube using the Cube subclass and the size given.
        Cube subclasses can each have their own method of displaying the cube.
        """
        if type(self) is CubeSimulator:
            raise TypeError(f"Only {type(self).__name__} subclasses may be instantiated")
        self._cube: Cube = cube_subclass(size)
        self._moves: dict[str, Callable] = {}

    def perform_moves(self, moves_string: str) -> None:
        """
        Reads the string given and performs all moves on the cube.

        :param moves_string: A string representing a sequence of moves to perform.
            e.g. "RUR'U'" means R U R' U'.
        """
        stored_move = None
        for char in moves_string:
            if char == "2":
                if stored_move:
                    self.move_twice(stored_move)
                    stored_move = None
                else:
                    raise ValueError("typed 2 with nothing/invalid value before it")
            elif char == "'":
                if stored_move:
                    stored_move(prime=True)
                    stored_move = None
                else:
                    raise ValueError("typed ' with nothing/invalid value before it")
            else:
                if stored_move:
                    stored_move()
                stored_move = self._moves[char]
        if stored_move:
            stored_move()

    @staticmethod
    def move_twice(move: Callable) -> None:
        move()
        move()

    def display_cube(self) -> None:
        self._cube.display_cube()
