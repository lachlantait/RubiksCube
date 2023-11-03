import unittest

from cube import *


class PatternTests(unittest.TestCase):
    def test_example(self):
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
                [Colour.YELLOW, Colour.WHITE, Colour.WHITE],
                [Colour.YELLOW, Colour.GREEN, Colour.ORANGE],
                [Colour.GREEN, Colour.RED, Colour.GREEN]
            ],
            [
                [Colour.BLUE, Colour.RED, Colour.RED],
                [Colour.GREEN, Colour.RED, Colour.GREEN],
                [Colour.RED, Colour.RED, Colour.RED]
            ],
            [
                [Colour.BLUE, Colour.BLUE, Colour.WHITE],
                [Colour.RED, Colour.BLUE, Colour.WHITE],
                [Colour.BLUE, Colour.BLUE, Colour.BLUE]
            ],
            [
                [Colour.GREEN, Colour.YELLOW, Colour.ORANGE],
                [Colour.GREEN, Colour.ORANGE, Colour.GREEN],
                [Colour.ORANGE, Colour.ORANGE, Colour.WHITE]
            ],
            [
                [Colour.GREEN, Colour.ORANGE, Colour.RED],
                [Colour.ORANGE, Colour.WHITE, Colour.WHITE],
                [Colour.ORANGE, Colour.WHITE, Colour.WHITE]
            ],
            [
                [Colour.YELLOW, Colour.YELLOW, Colour.YELLOW],
                [Colour.BLUE, Colour.YELLOW, Colour.YELLOW],
                [Colour.ORANGE, Colour.BLUE, Colour.YELLOW]
            ]
        ]

        self.assertEqual(result, expected, "The cubes don't match!")


if __name__ == '__main__':
    unittest.main()
