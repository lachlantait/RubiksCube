from typing import Callable

from cube import Cube, RowMove, ColumnMove


class CubeSimulator3x3:
    """
    Provides an interface for performing moves on a 3x3 Cube using 3x3 Rubik's Cube move notation
    (sourced here: https://solvethecube.com/notation).
    """

    def __init__(self) -> None:
        self._cube = Cube(3)

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
                stored_move = self._get_move_from_char(char)
        if stored_move:
            stored_move()

    def _get_move_from_char(self, move_char: str) -> Callable:
        """
        Returns the move_* function that corresponds to the single-character string given.

        :raises ValueError: If move_char is not a single-character string that corresponds to a move_* function.
        """
        match move_char:
            case "U":
                move = self.move_U
            case "D":
                move = self.move_D
            case "L":
                move = self.move_L
            case "R":
                move = self.move_R
            case "F":
                move = self.move_F
            case "B":
                move = self.move_B
            case "M":
                move = self.move_M
            case "E":
                move = self.move_E
            case "S":
                move = self.move_S
            case "u":
                move = self.move_u
            case "d":
                move = self.move_d
            case "l":
                move = self.move_l
            case "r":
                move = self.move_r
            case "f":
                move = self.move_f
            case "b":
                move = self.move_b
            case "x":
                move = self.move_x
            case "y":
                move = self.move_y
            case "z":
                move = self.move_z
            case _:
                raise ValueError("Invalid character")
        return move

    def move_U(self, *, prime: bool = False) -> None:
        direction = RowMove.LEFT if not prime else RowMove.RIGHT
        self._cube.rotate_y(1, direction)

    def move_D(self, *, prime: bool = False) -> None:
        direction = RowMove.RIGHT if not prime else RowMove.LEFT
        self._cube.rotate_y(3, direction)

    def move_L(self, *, prime: bool = False) -> None:
        direction = ColumnMove.DOWN if not prime else ColumnMove.UP
        self._cube.rotate_x(1, direction)

    def move_R(self, *, prime: bool = False) -> None:
        direction = ColumnMove.UP if not prime else ColumnMove.DOWN
        self._cube.rotate_x(3, direction)

    def move_F(self, *, prime: bool = False) -> None:
        direction = ColumnMove.DOWN if not prime else ColumnMove.UP
        self._cube.rotate_z(3, direction)

    def move_B(self, *, prime: bool = False) -> None:
        direction = ColumnMove.UP if not prime else ColumnMove.DOWN
        self._cube.rotate_z(3, direction)

    def move_M(self, *, prime: bool = False) -> None:
        direction = ColumnMove.DOWN if not prime else ColumnMove.UP
        self._cube.rotate_x(2, direction)

    def move_E(self, *, prime: bool = False) -> None:
        direction = RowMove.RIGHT if not prime else RowMove.LEFT
        self._cube.rotate_y(2, direction)

    def move_S(self, *, prime: bool = False) -> None:
        direction = ColumnMove.DOWN if not prime else ColumnMove.UP
        self._cube.rotate_z(2, direction)

    def move_u(self, *, prime: bool = False) -> None:
        self.move_U(prime=prime)
        self.move_E(prime=not prime)

    def move_d(self, *, prime: bool = False) -> None:
        self.move_D(prime=prime)
        self.move_E(prime=prime)

    def move_l(self, *, prime: bool = False) -> None:
        self.move_L(prime=prime)
        self.move_M(prime=prime)

    def move_r(self, *, prime: bool = False) -> None:
        self.move_R(prime=prime)
        self.move_M(prime=not prime)

    def move_f(self, *, prime: bool = False) -> None:
        self.move_F(prime=prime)
        self.move_S(prime=prime)

    def move_b(self, *, prime: bool = False) -> None:
        self.move_B(prime=prime)
        self.move_S(prime=not prime)

    def move_x(self, *, prime: bool = False) -> None:
        self.move_R(prime=prime)
        self.move_l(prime=not prime)

    def move_y(self, *, prime: bool = False) -> None:
        self.move_U(prime=prime)
        self.move_d(prime=not prime)

    def move_z(self, *, prime: bool = False) -> None:
        self.move_F(prime=prime)
        self.move_d(prime=not prime)

    @staticmethod
    def move_twice(move: Callable) -> None:
        move()
        move()

    def display_cube(self) -> None:
        self._cube.display_cube()


if __name__ == '__main__':
    test_sim = CubeSimulator3x3()
    test_sim.perform_moves("M2E2S2")
    test_sim.display_cube()
