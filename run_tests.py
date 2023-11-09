"""
Tests for all the classes in this project. Not very comprehensive.

Strategy for testing 'patterns':
- Sourced pattern algorithms from https://ruwix.com/the-rubiks-cube/rubiks-cube-patterns-algorithms/
- Line up my IRL cube so that the colours are in the same position as the default cube layout in this program
- Perform the algorithm on my cube
- Write down a string representation of the resulting cube layout
- The tests in this file perform the algorithm on a cube, and see if the resulting layout matches a cube created from
    the string representation I gave.
"""

import unittest

from cube import RowMove, ColumnMove, Colour
from cube_text_ui_2d import CubeTextUI2D
from cube_simulator_3x3 import CubeSimulator3x3
from cube_game import CubeGame2D

__author__ = "Lachlan Tait"


# TODO: Ideally need to make sure every move (and its variants) is tested
# A list of (<pattern name>, <algorithm>, <expected cube layout>) tuples:
patterns: list[tuple[str, str, str]] = [
    ("Checkerboard 1",
     "M2E2S2",
     ("GBGBGBGBG"
      "ROROROROR"
      "BGBGBGBGB"
      "ORORORORO"
      "WYWYWYWYW"
      "YWYWYWYWY")
     ),
    ("Checkerboard 2",
     "MESMES",
     ("GBGBGBGBG"
      "ROROROROR"
      "BGBGBGBGB"
      "ORORORORO"
      "WYWYWYWYW"
      "YWYWYWYWY")
     ),
    ("Cube in the cube",
     "F L F U' R U F2 L2 U' L' B D' B' L2 U",
     ("YYYGGYGGY"
      "BRRBRRBBB"
      "BBWBBWWWW"
      "GGGGOOGOO"
      "RRRRWWRWW"
      "OOOYYOYYO")
     ),
    ("Cube in a cube in a cube",
     "U' L' U' F' R2 B' R F U B2 U B' L U' F U R F'",
     ("OOOGGOYGO"
      "WRBWRRWWW"
      "WBRBBRRRR"
      "YYYYOOYOG"
      "BBBBWWBWR"
      "GGGYYGOYG")
     )
]


class TestCube(unittest.TestCase):
    def test_example(self):
        test_cube = CubeTextUI2D(3)
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
        expected_cube = CubeTextUI2D(3, cube_list=expected_cube_list)
        self.assertEqual(test_cube, expected_cube, "The cubes don't match!")

        expected_cube_string = "YWWYGOGRGBRRGRGRRRBBWRBWBBBGYOGOGOOWGOROWWOWWYYYBYYOBY"
        expected_cube = CubeTextUI2D(3, string_repr=expected_cube_string)
        self.assertEqual(test_cube, expected_cube, "Creating a cube from a string representation doesn't work")

        test_cube.reset()
        expected_cube = CubeTextUI2D(3)
        self.assertEqual(test_cube, expected_cube, "Resetting the cube doesn't work")


class TestCubeSimulator3x3(unittest.TestCase):
    def test_reset(self):
        test_cube = CubeTextUI2D(3, string_repr=patterns[0][2])  # Creating a cube with some arbitrary layout
        test_cube.reset()
        expected_cube = CubeTextUI2D(3)
        self.assertEqual(test_cube, expected_cube, "Resetting the cube doesn't work")

    def test_patterns(self):
        for pattern_name, algorithm, expected_string in patterns:
            test_sim = CubeSimulator3x3(CubeTextUI2D)
            test_sim.perform_moves(algorithm)
            expected_cube = CubeTextUI2D(3, string_repr=expected_string)
            self.assertEqual(test_sim.get_cube(), expected_cube,
                             f"The cubes do not match for pattern \"{pattern_name}\"")
            test_sim.undo_moves_sequence()
            expected_cube.reset()
            self.assertEqual(test_sim.get_cube(), expected_cube,
                             f"Undoing pattern \"{pattern_name}\" did not reset the cube back to solved")


class TestCubeGame(unittest.TestCase):
    def test_patterns(self):
        for pattern_name, algorithm, expected_string in patterns:
            test_game = CubeGame2D(CubeSimulator3x3, CubeTextUI2D)
            test_game._perform_moves(algorithm)
            expected_cube = CubeTextUI2D(3, string_repr=expected_string)
            self.assertEqual(test_game._simulator.get_cube(), expected_cube,
                             f"The cubes do not match for pattern \"{pattern_name}\"")
            test_game._undo_sequence()
            expected_cube.reset()
            self.assertEqual(test_game._simulator.get_cube(), expected_cube,
                             f"Undoing pattern \"{pattern_name}\" did not reset the cube back to solved")


if __name__ == '__main__':
    unittest.main()
