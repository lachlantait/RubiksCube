"""
Rubik's Cube simulator.
"""

__author__ = "Lachlan Tait"

from enum import Enum, auto

from termcolor import colored


class Colour(Enum):
    """ Colours for the faces of the cube. """
    RED = auto()
    WHITE = auto()
    ORANGE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLUE = auto()


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
    LEFT = 1
    RIGHT = 2


class Cube:
    """
    A Rubik's Cube.

    Represented internally as a 3-dimensional array of Colour values.

    Faces are indexed like so:
    ╔===╗
    ╟ 4 ╢
    ╠===╬===╦===╦===╗
    ╟ 0 ╟ 1 ╢ 2 ╢ 3 ╢
    ╠===╬===╩===╩===╝
    ╟ 5 ╢
    ╚===╝
    When a new cube is created, the faces are given colours by going through each face index in order and giving
    that face the corresponding colour in the Colour enum class. So reorder the enum values if you want a different
    order of colours.

    x, y, and z for the rotate methods are defined like so:
        ╔===╗
        ╟   ╢/> z
    y ^ ╠===/===╦===╦===╗
      | ╟ 0 ╟   ╢   ╢   ╢
      | ╠===╬===╩===╩===╝
       ----> x
        ╚===╝
    where rotate_x means rotate around the x-axis, etc.
    """
    
    FACES_IN_A_CUBE = 6

    def __init__(self, size: int) -> None:
        """
        Initialises the cube in the completed state.
        :param size: The cube created will have faces that are <size>x<size> (e.g. (3x3)).
                     Must be >= 1.
        """
        if size <= 0:
            raise ValueError("Invalid size")
        self.size: int = size
        self._cube: list[list[list[Colour]]] = self.initialise_cube()

    def __getitem__(self, face: int) -> list[list[Colour]]:
        return self._cube[face]

    def __len__(self):
        return self.FACES_IN_A_CUBE * self.size * self.size

    def initialise_cube(self) -> list[list[list[Colour]]]:
        """ Returns a completed cube. """
        return [[[colour] * self.size for _ in range(self.size)] for colour in Colour]

    def rotate_x(self, column: int, direction: ColumnMove) -> None:
        """
        Rotates the column specified, in the given direction, 90 degrees around the x-axis.

        :param column: The column to rotate, 1-indexed.
        :param direction: Whether to rotate the column up or down.
        """
        if not 1 <= column <= self.size:
            raise ValueError("Invalid column")
        column -= 1  # Change column to 0-indexed.

        # Rotate the column
        face0_column = self.get_column(0, column)
        face4_column = self.get_column(4, column)
        face2_column = self.get_column(2, self.size - 1 - column)  # Get the opposite column
        face5_column = self.get_column(5, column)
        if direction == ColumnMove.UP:
            self._set_column(0, column, face5_column)
            self._set_column(4, column, face0_column)
            # Set the opposite column, in reverse order:
            self._set_column(2, self.size - 1 - column, face4_column, reverse=True)
            self._set_column(5, column, face2_column)
        else:  # direction == ColumnMove.DOWN
            self._set_column(0, column, face4_column)
            self._set_column(4, column, face2_column, reverse=True)
            # Set the opposite column, in reverse order:
            self._set_column(2, self.size - 1 - column, face5_column, reverse=True)
            self._set_column(5, column, face0_column)

        # Leftmost column was rotated, so face 3 was rotated
        if column == 0:
            rotate_face_direction = RotateMove.LEFT if direction == ColumnMove.UP else RotateMove.RIGHT
            self._rotate_face(3, rotate_face_direction)
        # Rightmost column was rotated, so face 1 was rotated
        elif column == self.size - 1:
            rotate_face_direction = RotateMove.RIGHT if direction == ColumnMove.UP else RotateMove.LEFT
            self._rotate_face(1, rotate_face_direction)

    def rotate_y(self, row: int, direction: RowMove) -> None:
        """
        Rotates the row specified, in the given direction, 90 degrees around the y-axis.

        :param row: The row to rotate, 1-indexed.
        :param direction: Whether to rotate the row left or right.
        """
        if not 1 <= row <= self.size:
            raise ValueError("Invalid row")
        row -= 1  # Change row to 0-indexed.

        # Rotate the row
        face0_row = self._cube[0][row]
        face1_row = self._cube[1][row]
        face2_row = self._cube[2][row]
        face3_row = self._cube[3][row]
        if direction == RowMove.LEFT:
            self._cube[0][row] = face1_row
            self._cube[1][row] = face2_row
            self._cube[2][row] = face3_row
            self._cube[3][row] = face0_row
        else:  # direction == rowMove.RIGHT
            self._cube[0][row] = face3_row
            self._cube[1][row] = face0_row
            self._cube[2][row] = face1_row
            self._cube[3][row] = face2_row

        # Top row was rotated, so top face was rotated
        if row == 0:
            rotate_face_direction = RotateMove.RIGHT if direction == RowMove.LEFT else RotateMove.LEFT
            self._rotate_face(4, rotate_face_direction)
        # Bottom row was rotated, so bottom face was rotated
        elif row == self.size - 1:
            rotate_face_direction = RotateMove.LEFT if direction == RowMove.LEFT else RotateMove.RIGHT
            self._rotate_face(5, rotate_face_direction)

    def rotate_z(self, column: int, direction: ColumnMove) -> None:
        """
        Rotates the column specified, in the given direction, 90 degrees around the z-axis.

        :param column: The column to rotate, 1-indexed.
        :param direction: Whether to rotate the column up or down.
        """
        if not 1 <= column <= self.size:
            raise ValueError("Invalid column")
        column -= 1  # Change column to 0-indexed.

        # Rotate the column
        # Some 'columns' here are actually stored as rows
        face1_column = self.get_column(1, column)
        face4_column = self._cube[4][0]
        face3_column = self.get_column(3, self.size - 1 - column)  # Get opposite column
        face5_column = self._cube[5][self.size - 1]
        if direction == ColumnMove.UP:
            self._set_column(1, column, face5_column, reverse=True)
            self._cube[4][0] = face1_column
            # Set the opposite column, in reverse order:
            self._set_column(3, self.size - 1 - column, face4_column, reverse=True)
            self._cube[5][self.size - 1] = face3_column
        else:  # direction == ColumnMove.DOWN
            self._set_column(1, column, face4_column)
            self._set_row(4, 0, face3_column, reverse=True)
            self._set_column(3, self.size - 1 - column, face5_column)  # Set the opposite column
            self._set_row(5, self.size - 1, face1_column, reverse=True)

        # Leftmost column was rotated, so face 0 was rotated
        if column == 0:
            rotate_face_direction = RotateMove.LEFT if direction == ColumnMove.UP else RotateMove.RIGHT
            self._rotate_face(0, rotate_face_direction)
        # Rightmost column was rotated, so face 2 was rotated
        elif column == self.size - 1:
            rotate_face_direction = RotateMove.RIGHT if direction == ColumnMove.UP else RotateMove.LEFT
            self._rotate_face(2, rotate_face_direction)

    def _rotate_face(self, face: int, direction: RotateMove) -> None:
        """
        Rotates a face of the cube 90 degrees in the given direction.

        This method only writes the given face, it does not affect other adjacent faces.
        It is intended as a private helper method for the other rotate methods, not as a public method.

        :param face: The face of the cube, 0-indexed.
        :param direction: Whether to rotate the face left or right.
        """
        # Store each column in the face
        columns = [None] * self.size
        for i in range(self.size):
            columns[i] = self.get_column(face, i)

        # Write the stored columns to the rows
        if direction == RotateMove.LEFT:
            for row in range(self.size):
                # Assign to rows by iterating through columns list in reverse order
                self._cube[face][row] = columns[self.size - 1 - row]
        else:  # direction == RotateMove.Right
            for row in range(self.size):
                # Assign each row each list in columns in order, but reverse each column list
                for column in range(self.size):
                    self._cube[face][row][column] = columns[row][self.size - 1 - column]

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
            for i in range(self.size):
                self._cube[face][row][i] = new_row_list[self.size - 1 - i]

    def get_column(self, face: int, column: int) -> list:
        """
        Given a face and a column number, returns a list representing that column.

        The column list will be from top to bottom.

        :param face: The face of the cube, 0-indexed.
        :param column: The column within the face, 0-indexed.
        """
        column_list = [None] * self.size
        for row in range(self.size):
            column_list[row] = self._cube[face][row][column]
        return column_list

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
            for row in range(self.size):
                self._cube[face][row][column] = new_column_list[row]
        else:
            for row in range(self.size):
                self._cube[face][row][column] = new_column_list[self.size - 1 - row]

    def display_cube(self) -> None:
        """
        Display a text interface representing the cube.

        Example:
        ╔=======╗
        ╟ ■ ■ ■ ╢
        ╟ ■ ■ ■ ╢
        ╟ ■ ■ ■ ╢
        ╠=======╬=======╦=======╦=======╗
        ╟ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╢
        ╟ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╢
        ╟ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╢
        ╠=======╬=======╩=======╩=======╝
        ╟ ■ ■ ■ ╢
        ╟ ■ ■ ■ ╢
        ╟ ■ ■ ■ ╢
        ╚=======╝
        """
        horizontal_line = "=" * (self.size * 2 + 1)

        # Face 4 (top)
        print("╔" + horizontal_line + "╗")
        for row in range(self.size):
            row_output = "╟ "
            for column in range(self.size):
                row_output += self.get_square(4, row, column) + " "
            row_output += "╢"
            print(row_output)

        # Faces 0-3
        print("╠" + horizontal_line + "╬" + horizontal_line + "╦" + horizontal_line + "╦" + horizontal_line + "╗")
        for row in range(self.size):
            row_output = "╟ "
            for face in range(4):  # Do faces 0, 1, 2, 3
                for column in range(self.size):
                    row_output += self.get_square(face, row, column) + " "
                row_output += "╫ "
            row_output = row_output[:-2] + "╢"
            print(row_output)
        print("╠" + horizontal_line + "╬" + horizontal_line + "╩" + horizontal_line + "╩" + horizontal_line + "╝")

        # Face 5 (bottom)
        for row in range(self.size):
            row_output = "╟ "
            for column in range(self.size):
                row_output += self.get_square(5, row, column) + " "
            row_output += "╢"
            print(row_output)
        print("╚" + horizontal_line + "╝")

    def get_square(self, face: int, row: int, column: int) -> str:
        """
        Returns a coloured string, displaying the colour of the given square.
        :param face: The face of the cube, 0-indexed.
        :param row: The row within the face, 0-indexed.
        :param column: The column within the row, 0-indexed.
        """
        if not 0 <= face <= 5:
            raise ValueError("Invalid face")
        if not 0 <= row < self.size:
            raise ValueError("Invalid row")
        if not 0 <= column < self.size:
            raise ValueError("Invalid column")

        match self._cube[face][row][column]:
            case Colour.RED:
                colour = "red"
            case Colour.WHITE:
                colour = "white"
            case Colour.ORANGE:
                colour = "yellow"  # No orange in termcolor :(
            case Colour.YELLOW:
                colour = "light_yellow"
            case Colour.GREEN:
                colour = "green"
            case Colour.BLUE:
                colour = "blue"
            case _:
                colour = "black"
        return colored("■", colour)

    def __str__(self) -> str:
        """ Pretty-print self.cube """
        output = ""
        for face in range(self.FACES_IN_A_CUBE):
            output += f"Face {face + 1}:"
            for row in range(self.size):
                row_string = "\n\t"
                for column in range(self.size):
                    row_string += f"[{self._cube[face][row][column].name}] "
                row_string = row_string[:-1]  # Exclude final space
                output += row_string
            output += "\n"
        return output[:-1]  # Exclude final newline character


if __name__ == '__main__':
    test_cube = Cube(3)
    # test_cube[3][0][1] = Colour.BLUE

    test_cube.rotate_x(1, ColumnMove.UP)
    test_cube.rotate_y(2, RowMove.LEFT)
    test_cube.rotate_z(3, ColumnMove.UP)
    test_cube.rotate_x(1, ColumnMove.DOWN)
    test_cube.rotate_y(2, RowMove.RIGHT)
    test_cube.rotate_z(3, ColumnMove.DOWN)

    test_cube.display_cube()
