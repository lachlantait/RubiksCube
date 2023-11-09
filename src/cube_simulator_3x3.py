from typing import Callable, Type

from .cube import Cube, RowMove, ColumnMove
from .cube_simulator import CubeSimulator

__author__ = "Lachlan Tait"


class CubeSimulator3x3(CubeSimulator):
    """
    Provides an interface for performing moves on a 3x3 Cube using 3x3 Rubik's Cube move notation
    (sourced here: https://solvethecube.com/notation).
    """

    def __init__(self, cube_subclass: Type[Cube]) -> None:
        """
        Initialises the cube using the Cube subclass given.
        Cube subclasses can each have their own method of displaying the cube.
        """
        super().__init__(cube_subclass, 3, scramble_move_count=22)
        self._moves: dict[str, Callable] = {
            "U": self.move_U,
            "D": self.move_D,
            "L": self.move_L,
            "R": self.move_R,
            "F": self.move_F,
            "B": self.move_B,
            "M": self.move_M,
            "E": self.move_E,
            "S": self.move_S,
            "u": self.move_u,
            "d": self.move_d,
            "l": self.move_l,
            "r": self.move_r,
            "f": self.move_f,
            "b": self.move_b,
            "x": self.move_x,
            "y": self.move_y,
            "z": self.move_z
        }

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
        self._cube.rotate_z(1, direction)

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
        self.move_b(prime=not prime)
