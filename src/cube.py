"""
Classes for simulating a Rubik's Cube.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto

__author__ = "Lachlan Tait"


class Cube(ABC):
    """
    A Rubik's Cube.

    Represented internally as a 3-dimensional list of Colour values.
    This class is abstract so that subclasses can provide their own method of displaying the cube.

    Faces are indexed like so:
        ╔===╗
        ╟ 4 ╢
    ╔===╬===╬===╦===╗
    ╟ 0 ╟ 1 ╢ 2 ╢ 3 ╢
    ╚===╬===╬===╩===╝
        ╟ 5 ╢
        ╚===╝
    When a new cube is created, the faces are given colours by going through each face index in order and giving
    that face the corresponding colour in the Colour enum class.

    x, y, and z for the rotate methods are defined like so:
        ╔===╗
       Y╟   ╢
    ╔==^╬===/>Z=╦===╗
    ╟  |╟ 1 ╢   ╢   ╢
    ╚==|/===╬===╩===╝
       .-----> X
        ╚===╝
    where rotate_x means rotate around the x-axis, etc.
    """

    FACES_IN_A_CUBE = 6

    def __init__(self, size: int, *,
                 cube_list: list[list[list[Colour]]] | None = None,
                 string_repr: str | None = None
                 ) -> None:
        """
        Initialises the cube.

        If neither <cube_list> nor <string_repr> are provided, the cube initialised is solved.
        Warning: <cube_list> and <string_repr> are not checked to see if they are valid/solvable cubes.

        :param size: The cube created will have faces that are <size>x<size> (e.g. (3x3)).
            Must be >= 1.
        :param cube_list: If provided, the cube is initialised to this 3-dimensional list.
        :param string_repr: If provided (and <cube> is not),
            the cube is initialised using this string representation of a cube.
        :raises ValueError: If a non-positive size is given.
        """
        if size <= 0:
            raise ValueError("Invalid size")
        self._size: int = size

        self._cube: list[list[list[Colour]]] | None = None
        if cube_list:
            self._cube = cube_list
        elif string_repr:
            self._cube = Cube.create_cube_from_string_representation(self._size, string_repr)
        else:
            self.reset()  # Sets the cube to the initial, solved state

    def __len__(self):
        """ Returns the amount of squares in the cube. """
        return Cube.FACES_IN_A_CUBE * self._size * self._size

    def __eq__(self, other: Cube) -> bool:
        return self._size == other._size and self._cube == other._cube

    def __iter__(self):
        return CubeIterator(self)

    def get_size(self) -> int:
        return self._size

    def get_cube(self) -> list[list[list[Colour]]]:
        return self._cube

    def get_row(self, face: int, row: int) -> list[Colour]:
        """
        Given a face and a row number, returns a list representing that row.

        :param face: The face of the cube, 0-indexed.
        :param row: The row within the face, 0-indexed.
        """
        return self._cube[face][row]

    def get_column(self, face: int, column: int) -> list[Colour]:
        """
        Given a face and a column number, returns a list representing that column.

        The column list will be from top to bottom.

        :param face: The face of the cube, 0-indexed.
        :param column: The column within the face, 0-indexed.
        """
        column_list = []
        for row in range(self._size):
            column_list.append(self._cube[face][row][column])
        return column_list

    def get_square(self, face: int, row: int, column: int) -> Colour:
        return self._cube[face][row][column]

    def get_string_representation(self) -> str:
        """
        Returns a string representing the cube.
        e.g. "GGGGGGGGGRRRRRRRRRBBBBBBBBBOOOOOOOOOWWWWWWYYYYYY" is a solved cube.
        """
        output = ""
        for square in self:
            output += Cube.get_string_from_colour(square)
        return output

    def set_cube(self, cube: list[list[list[Colour]]]):
        """
        Sets the cube to the 3-dimensional list given.
        Warning: cube is not checked to see if it is a valid/solvable cube.
        """
        self._cube = cube

    def _set_row(self, face: int, row: int, new_row_list: list[Colour], reverse: bool = False) -> None:
        """
        Given a face and row number, sets that row using the new_row_list provided.

        :param face: The face of the cube, 0-indexed.
        :param row: The row within the face, 0-indexed.
        :param new_row_list: A list representing a row, the row will be set using this list.
        :param reverse: If true, sets the row in reverse order.
        """
        if not reverse:
            self._cube[face][row] = new_row_list
        else:
            for i in range(self._size):
                self._cube[face][row][i] = new_row_list[self._size - 1 - i]

    def _set_column(self, face: int, column: int, new_column_list: list[Colour], reverse: bool = False) -> None:
        """
        Given a face and column number, sets that column using the new_column_list provided.

        :param face: The face of the cube, 0-indexed.
        :param column: The column within the face, 0-indexed.
        :param new_column_list: A list representing a column, the column will be set using this list.
            This list should have the top-most square first.
        :param reverse: If true, sets the column in reverse order.
        """
        if not reverse:
            for row in range(self._size):
                self._cube[face][row][column] = new_column_list[row]
        else:
            for row in range(self._size):
                self._cube[face][row][column] = new_column_list[self._size - 1 - row]

    def reset(self) -> None:
        """ Resets the cube back to the solved state. """
        self._cube = Cube.create_solved_cube(self._size)

    def rotate_x(self, column: int, direction: ColumnMove) -> None:
        """
        Rotates the column specified, in the given direction, 90 degrees around the x-axis.

        :param column: The column to rotate, 1-indexed.
        :param direction: Whether to rotate the column up or down.
        :raises ValueError: If an invalid column number is given.
        """
        if not 1 <= column <= self._size:
            raise ValueError("Invalid column")
        column -= 1  # Change column to 0-indexed.

        # Rotate the column
        face1_column = self.get_column(1, column)
        face4_column = self.get_column(4, column)
        face3_column = self.get_column(3, self._size - 1 - column)  # Get the opposite column
        face5_column = self.get_column(5, column)
        if direction == ColumnMove.UP:
            self._set_column(1, column, face5_column)
            self._set_column(4, column, face1_column)
            self._set_column(3, self._size - 1 - column, face4_column, reverse=True)  # Set the opposite column
            self._set_column(5, column, face3_column, reverse=True)
        else:  # direction == ColumnMove.DOWN
            self._set_column(1, column, face4_column)
            self._set_column(4, column, face3_column, reverse=True)
            self._set_column(3, self._size - 1 - column, face5_column, reverse=True)  # Set the opposite column
            self._set_column(5, column, face1_column)

        # Leftmost column was rotated, so face 0 was rotated
        if column == 0:
            rotate_face_direction = RotateMove.ANTICLOCKWISE if direction == ColumnMove.UP else RotateMove.CLOCKWISE
            self._rotate_face(0, rotate_face_direction)
        # Rightmost column was rotated, so face 2 was rotated
        elif column == self._size - 1:
            rotate_face_direction = RotateMove.CLOCKWISE if direction == ColumnMove.UP else RotateMove.ANTICLOCKWISE
            self._rotate_face(2, rotate_face_direction)

    def rotate_y(self, row: int, direction: RowMove) -> None:
        """
        Rotates the row specified, in the given direction, 90 degrees around the y-axis.

        :param row: The row to rotate, 1-indexed.
        :param direction: Whether to rotate the row left or right.
        :raises ValueError: If an invalid row number is given.
        """
        if not 1 <= row <= self._size:
            raise ValueError("Invalid row")
        row -= 1  # Change row to 0-indexed.

        # Rotate the row
        face0_row = self.get_row(0, row)
        face1_row = self.get_row(1, row)
        face2_row = self.get_row(2, row)
        face3_row = self.get_row(3, row)
        if direction == RowMove.LEFT:
            self._set_row(0, row, face1_row)
            self._set_row(1, row, face2_row)
            self._set_row(2, row, face3_row)
            self._set_row(3, row, face0_row)
        else:  # direction == RowMove.RIGHT
            self._set_row(0, row, face3_row)
            self._set_row(1, row, face0_row)
            self._set_row(2, row, face1_row)
            self._set_row(3, row, face2_row)

        # Top row was rotated, so top face was rotated
        if row == 0:
            rotate_face_direction = RotateMove.CLOCKWISE if direction == RowMove.LEFT else RotateMove.ANTICLOCKWISE
            self._rotate_face(4, rotate_face_direction)
        # Bottom row was rotated, so bottom face was rotated
        elif row == self._size - 1:
            rotate_face_direction = RotateMove.ANTICLOCKWISE if direction == RowMove.LEFT else RotateMove.CLOCKWISE
            self._rotate_face(5, rotate_face_direction)

    def rotate_z(self, column: int, direction: ColumnMove) -> None:
        """
        Rotates the column specified, in the given direction, 90 degrees around the z-axis.

        :param column: The column to rotate, 1-indexed.
        :param direction: Whether to rotate the column up or down.
        :raises ValueError: If an invalid column number is given.
        """
        if not 1 <= column <= self._size:
            raise ValueError("Invalid column")
        column -= 1  # Change column to 0-indexed.

        # Rotate the column
        # Some 'columns' here are actually stored as rows
        face2_column = self.get_column(2, column)
        face4_column = self.get_row(4, self._size - 1 - column)  # Get opposite column
        face0_column = self.get_column(0, self._size - 1 - column)  # Get opposite column
        face5_column = self.get_row(5, column)
        if direction == ColumnMove.UP:
            self._set_column(2, column, face5_column, reverse=True)
            self._set_row(4, self._size - 1 - column, face2_column)  # Set opposite column
            self._set_column(0, self._size - 1 - column, face4_column, reverse=True)  # Set opposite column
            self._set_row(5, column, face0_column)
        else:  # direction == ColumnMove.DOWN
            self._set_column(2, column, face4_column)
            self._set_row(4, self._size - 1 - column, face0_column, reverse=True)  # Set opposite column
            self._set_column(0, self._size - 1 - column, face5_column)  # Set opposite column
            self._set_row(5, column, face2_column, reverse=True)

        # Leftmost column was rotated, so face 1 was rotated
        if column == 0:
            rotate_face_direction = RotateMove.ANTICLOCKWISE if direction == ColumnMove.UP else RotateMove.CLOCKWISE
            self._rotate_face(1, rotate_face_direction)
        # Rightmost column was rotated, so face 3 was rotated
        elif column == self._size - 1:
            rotate_face_direction = RotateMove.CLOCKWISE if direction == ColumnMove.UP else RotateMove.ANTICLOCKWISE
            self._rotate_face(3, rotate_face_direction)

    def _rotate_face(self, face: int, direction: RotateMove) -> None:
        """
        Rotates a face of the cube 90 degrees in the given direction.

        This method only writes the given face, it does not affect other adjacent faces.
        It is intended as a private helper method for the other rotate methods, not as a public method.

        :param face: The face of the cube, 0-indexed.
        :param direction: Whether to rotate the face left or right.
        """
        # Store each column in the face
        columns = []
        for i in range(self._size):
            columns.append(self.get_column(face, i))

        # Write the stored columns to the rows
        if direction == RotateMove.ANTICLOCKWISE:
            for row in range(self._size):
                # Assign to rows by iterating through columns list in reverse order
                self._cube[face][row] = columns[self._size - 1 - row]
        else:  # direction == RotateMove.CLOCKWISE
            for row in range(self._size):
                # Assign each row each list in columns in order, but reverse each column list
                for column in range(self._size):
                    self._cube[face][row][column] = columns[row][self._size - 1 - column]

    def __str__(self) -> str:
        """ Pretty-print self._cube """
        output = ""
        for face in range(Cube.FACES_IN_A_CUBE):
            output += f"Face {face + 1}:"
            for row in range(self._size):
                row_string = "\n\t"
                for column in range(self._size):
                    row_string += f"[{self.get_square(face, row, column).name}] "
                row_string = row_string[:-1]  # Exclude final space
                output += row_string
            output += "\n"
        return output[:-1]  # Exclude final newline character

    @staticmethod
    def create_solved_cube(size: int) -> list[list[list[Colour]]]:
        """
        Returns a solved cube.

        :param size: The cube created will have faces that are <size>x<size> (e.g. (3x3)).
            Must be >= 1.
        :raises ValueError: If a non-positive size is given.
        """
        if size <= 0:
            raise ValueError("Invalid size")
        return [[[colour] * size for _ in range(size)] for colour in Colour]

    @staticmethod
    def create_cube_from_string_representation(size: int, string_representation: str) -> list[list[list[Colour]]]:
        """
        Returns a cube created from a string representing how the colours should be assigned to each square.

        Warning: This method doesn't check that the cube created is solvable.

        :param size: The cube created will have faces that are <size>x<size> (e.g. (3x3)).
            Must be >= 1.
        :param string_representation: A string representing the colours in the cube.
            e.g. "GGGGGGGGGRRRRRRRRRBBBBBBBBBOOOOOOOOOWWWWWWYYYYYY" is a solved cube.
        :return: A 3-dimensional list of colours representing a cube.
        :raises ValueError: If a non-positive size is given.
        """
        if size <= 0:
            raise ValueError("Invalid size")

        cube_list = []
        i = 0
        for face in range(Cube.FACES_IN_A_CUBE):
            face_list = []
            for row in range(size):
                row_list = []
                for square in range(size):
                    row_list.append(Cube.get_colour_from_string(string_representation[i]))
                    i += 1
                face_list.append(row_list)
            cube_list.append(face_list)
        return cube_list

    @staticmethod
    def get_colour_from_string(colour_string: str) -> Colour:
        """
        Returns a Colour that is represented by the single-character string given.

        :raises ValueError: If an invalid string is given.
        """
        match colour_string:
            case "G":
                colour = Colour.GREEN
            case "R":
                colour = Colour.RED
            case "B":
                colour = Colour.BLUE
            case "O":
                colour = Colour.ORANGE
            case "W":
                colour = Colour.WHITE
            case "Y":
                colour = Colour.YELLOW
            case _:
                raise ValueError("Invalid string")
        return colour

    @staticmethod
    def get_string_from_colour(colour: Colour) -> str:
        """
        Returns a single-character string representing the colour given.

        :raises ValueError: If an invalid Colour is given.
        """
        match colour:
            case Colour.GREEN:
                colour_string = "G"
            case Colour.RED:
                colour_string = "R"
            case Colour.BLUE:
                colour_string = "B"
            case Colour.ORANGE:
                colour_string = "O"
            case Colour.WHITE:
                colour_string = "W"
            case Colour.YELLOW:
                colour_string = "Y"
            case _:
                raise ValueError("Invalid Colour")
        return colour_string

    @abstractmethod
    def display_cube(self) -> None:
        raise NotImplementedError


class CubeIterator:
    """ Iterates through every square in the cube in order. """
    def __init__(self, cube: Cube) -> None:
        self._cube: Cube = cube
        self._current_face: int = 0
        self._current_row: int = 0
        self._current_square: int = 0

    def __iter__(self):
        return self

    def __next__(self) -> Colour:
        if self._current_face >= self._cube.FACES_IN_A_CUBE:
            raise StopIteration

        cube_list = self._cube.get_cube()
        square: Colour = cube_list[self._current_face][self._current_row][self._current_square]

        self._current_square += 1
        if self._current_square >= self._cube.get_size():
            self._current_square = 0
            self._current_row += 1
            if self._current_row >= self._cube.get_size():
                self._current_row = 0
                self._current_face += 1

        return square


class Colour(Enum):
    """
    Colours for the faces of the cube.
    Note: The ordering here determines the order that colours are assigned to faces.
    """
    GREEN = auto()
    RED = auto()
    BLUE = auto()
    ORANGE = auto()
    WHITE = auto()
    YELLOW = auto()


class RowMove(Enum):
    """ Moves to be performed on a row of the cube. """
    LEFT = 1
    RIGHT = 2


class ColumnMove(Enum):
    """ Moves to be performed on a column of the cube. """
    UP = 1
    DOWN = 2


class RotateMove(Enum):
    """ Directions a face of the cube can be rotated in. """
    ANTICLOCKWISE = 1
    CLOCKWISE = 2
