import unittest

from cube import *


class PatternTests(unittest.TestCase):
    def test_1(self):
        test_cube = Cube(3)
        test_cube.rotate_x(1, ColumnMove.UP)
        test_cube.rotate_y(2, RowMove.LEFT)
        test_cube.rotate_z(3, ColumnMove.UP)
        test_cube.rotate_x(1, ColumnMove.DOWN)
        test_cube.rotate_y(2, RowMove.RIGHT)
        test_cube.rotate_z(3, ColumnMove.DOWN)

        result = test_cube.get_cube()

        expected = [
            [
                [Colour.WHITE, Colour.RED, Colour.RED],
                [Colour.YELLOW, Colour.RED, Colour.YELLOW],
                [Colour.RED, Colour.RED, Colour.RED]
            ],
            [
                [Colour.WHITE, Colour.WHITE, Colour.GREEN],
                [Colour.RED, Colour.WHITE, Colour.GREEN],
                [Colour.WHITE, Colour.WHITE, Colour.WHITE]
            ],
            [
                [Colour.YELLOW, Colour.BLUE, Colour.ORANGE],
                [Colour.YELLOW, Colour.ORANGE, Colour.YELLOW],
                [Colour.ORANGE, Colour.ORANGE, Colour.GREEN]
            ],
            [
                [Colour.BLUE, Colour.GREEN, Colour.GREEN],
                [Colour.BLUE, Colour.YELLOW, Colour.ORANGE],
                [Colour.YELLOW, Colour.RED, Colour.YELLOW]
            ],
            [
                [Colour.YELLOW, Colour.ORANGE, Colour.RED],
                [Colour.ORANGE, Colour.GREEN, Colour.GREEN],
                [Colour.ORANGE, Colour.GREEN, Colour.GREEN]
            ],
            [
                [Colour.BLUE, Colour.BLUE, Colour.BLUE],
                [Colour.WHITE, Colour.BLUE, Colour.BLUE],
                [Colour.ORANGE, Colour.WHITE, Colour.BLUE]
            ]
        ]

        self.assertEqual(result, expected, "The cubes don't match!")


if __name__ == '__main__':
    unittest.main()
