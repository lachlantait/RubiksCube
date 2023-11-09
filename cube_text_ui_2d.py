from termcolor import colored

from cube import Cube, Colour

__author__ = "Lachlan Tait"


class CubeTextUI2D(Cube):
    """
    This cube subclass provides a text-based, coloured representation of a cube.
    The cube is represented as a 2D net.
    """
    def display_cube(self) -> None:
        """
        Display a text interface representing the cube as a 2D net.

        Example:
                ╔=======╗
                ╟ ■ ■ ■ ╢
                ╟ ■ ■ ■ ╢
                ╟ ■ ■ ■ ╢
        ╔=======╬=======╬=======╦=======╗
        ╟ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╢
        ╟ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╢
        ╟ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╫ ■ ■ ■ ╢
        ╚=======╬=======╬=======╩=======╝
                ╟ ■ ■ ■ ╢
                ╟ ■ ■ ■ ╢
                ╟ ■ ■ ■ ╢
                ╚=======╝
        """
        horizontal_line = "=" * (self._size * 2 + 1)
        space_before = " " * (2 + self._size * 2)

        # Face 4 (top)
        print(space_before + "╔" + horizontal_line + "╗")
        for row in range(self._size):
            row_output = space_before + "╟ "
            for column in range(self._size):
                row_output += self._get_coloured_square(4, row, column) + " "
            row_output += "╢"
            print(row_output)

        # Faces 0-3
        print("╔" + horizontal_line + "╬" + horizontal_line + "╬" + horizontal_line + "╦" + horizontal_line + "╗")
        for row in range(self._size):
            row_output = "╟ "
            for face in range(4):  # Do faces 0, 1, 2, 3
                for column in range(self._size):
                    row_output += self._get_coloured_square(face, row, column) + " "
                row_output += "╫ "
            row_output = row_output[:-2] + "╢"
            print(row_output)
        print("╚" + horizontal_line + "╬" + horizontal_line + "╬" + horizontal_line + "╩" + horizontal_line + "╝")

        # Face 5 (bottom)
        for row in range(self._size):
            row_output = space_before + "╟ "
            for column in range(self._size):
                row_output += self._get_coloured_square(5, row, column) + " "
            row_output += "╢"
            print(row_output)
        print(space_before + "╚" + horizontal_line + "╝")

    def _get_coloured_square(self, face: int, row: int, column: int) -> str:
        """
        Returns a coloured string, displaying the colour of the given square in the cube.

        :param face: The face of the cube, 0-indexed.
        :param row: The row within the face, 0-indexed.
        :param column: The column within the row, 0-indexed.
        :raises ValueError: If an invalid face, row, or column is given.
        """
        if not 0 <= face < Cube.FACES_IN_A_CUBE:
            raise ValueError("Invalid face")
        if not 0 <= row < self._size:
            raise ValueError("Invalid row")
        if not 0 <= column < self._size:
            raise ValueError("Invalid column")

        match self.get_square(face, row, column):
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


if __name__ == '__main__':
    test_cube = CubeTextUI2D(3)
    test_cube.display_cube()
