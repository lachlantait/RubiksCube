import unittest

from cube import Cube, RowMove, ColumnMove, Colour
from cube_simulator_3x3 import CubeSimulator3x3


class PatternTests3x3(unittest.TestCase):
    def test_example(self):
        test_cube = Cube(3)
        test_cube.rotate_x(1, ColumnMove.UP)
        test_cube.rotate_y(2, RowMove.LEFT)
        test_cube.rotate_z(3, ColumnMove.UP)
        test_cube.rotate_x(1, ColumnMove.DOWN)
        test_cube.rotate_y(2, RowMove.RIGHT)
        test_cube.rotate_z(3, ColumnMove.DOWN)

        expected_cube_list = [
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
        expected_cube = Cube(3, cube_list=expected_cube_list)
        self.assertEqual(test_cube, expected_cube, "The cubes don't match!")

        expected_cube_string = "YWWYGOGRGBRRGRGRRRBBWRBWBBBGYOGOGOOWGOROWWOWWYYYBYYOBY"
        expected_cube = Cube(3, string_repr=expected_cube_string)
        self.assertEqual(test_cube, expected_cube, "Creating a cube from a string representation doesn't work")

    def test_checkerboard(self):
        checkerboard_string = ("GBGBGBGBG"
                               "ROROROROR"
                               "BGBGBGBGB"
                               "ORORORORO"
                               "WYWYWYWYW"
                               "YWYWYWYWY")
        expected_cube = Cube(3, string_repr=checkerboard_string)

        test_sim = CubeSimulator3x3()
        test_sim.perform_moves("M2E2S2")
        self.assertEqual(expected_cube, test_sim._cube, "The two cubes are not equal")

        test_sim = CubeSimulator3x3()
        test_sim.perform_moves("MESMES")
        self.assertEqual(expected_cube, test_sim._cube, "The two cubes are not equal")


if __name__ == '__main__':
    unittest.main()
