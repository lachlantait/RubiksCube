# RubiksCube

## Overview
A Rubik's Cube simulator that runs in the terminal, written in Python.

## Current Features
- Perform any possible move on a 3x3 cube
- See history of algorithms performed on the cube
- Reset the cube back to solved (also clears history)
- Undo the most recent algorithm
  (currently this will set the history back to how it was before this algorithm was performed)
- Show the inverse of the most recently performed algorithm
- Scramble the cube (Just does random moves a set amount of times, currently 22)
- Toggle case will toggle between your input being treated as normal/swapped case (this was added
  in case you want to perform moves that require upper-case letters often and for some reason using caps lock
  is inconvenient)

### Interface
<img src="/cover.webp">

### Inputting Moves
You input moves by inputting a string of as many moves as you want, using standard Rubik's Cube notation:

e.g. "U' L' U' F' R2 B' R F U B2 U B' L U' F U R F'"

These moves will then all be performed in sequence on the cube.
Spaces don't matter, since all whitespace characters are removed from the string.
Input for moves are case-sensitive, but the characters for options are not.

## Getting Started
Navigate to the project directory in your terminal

Set up a virtual environment if you wish

Install dependencies:
```
pip install -r requirements.txt
```
Launch the program with:
```
python -m src.main
```

### Dependencies
- Uses [termcolor](https://github.com/termcolor/termcolor) for coloured terminal output

## Project Backstory

This was just made for fun. I started this as I was only just getting into Rubik's Cubes for the first time,
so I learnt about the notation and other things as I was working on this. I intend to add to it over time.

It's probably a fairly naive implementation? I still have a lot to learn. But I tried my best to make it
extensible for future.

## Implementation

Here are some details on the main classes in the project:

### Cube (in cube.py)
The cube is represented as a 3-dimensional list, with the outermost list being the 6 faces of the cube,
and each face is a 2-dimensional list that represents each individual tile in that face.

The cube is thus manipulated through methods that manipulate this 3-dimensional list. I created methods that can
manipulate any part of a cube of any size by specifying the x/y/z axis a row/column is rotated around, a number to
specify what row/column to rotate, and a direction to rotate in.

Each position in the cube just contains an enum value representing one of 6 colours. The program then reads these
values and prints output of the corresponding colour.

Support is there for cubes of different sizes like 2x2, 4x4, etc., but I haven't tested this much, or added
an interface for the user to interact with cubes of these sizes.

### CubeSimulator (in cube_simulator.py)
This class adds an interface for performing moves with standard Rubik's Cube notation. These methods call the
rotate_(x/y/z) methods in the Cube class. All other functionality in the program for working with the cube is
provided in this class.

### CubeGame (in cube_game.py)
This class provides the user interface, and calls the appropriate methods on the CubeSimulator class.

## To-do / Ideas / Future Features
- 3D interface?
- Solver?
- Other cube sizes?
- Interface for inputting a cube layout into the program?
- In-program help screen
- More rigorous testing
- Better method for checking if two cubes are the same (currently they have to be rotated in exactly the same way)
- Option to show/hide undo moves in the history
  (i.e. keep the move that was undone, and add the inverse algorithm to the history)
