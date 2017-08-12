# Sudoku Helper

#### Author(s): Christopher Jens Johnson
#### Credit: Base code and outline by Michal Young and Dr. Joe Sventek, University of Oregon. Open source TKinter graphics interface by John Zelle. Naked and Hidden single tactics available at [Sad Man Software](http://www.sadmansoftware.com/sudoku/solvingtechniques.php "Sad Man Software")

This Sudoku helper is a program that can be run in either a python shell or the command line. It uses two tactics, the "naked single" and the "hidden single" to attempt to solve all possible tiles on a given sudoku board. The program parses "boards" using .txt files of the format:

```
1..5..2..
2.3.1....
.5..9..3.
..7.6....
...8..4.1
9..2...9.
65.3..8..
...7.....
......1..
```

This program uses the TKinter module for python to provide a graphics interface for the helper, visualizing the possible numbers for each grid element as it narrows down the choices and solves the board.

*Note: This solver is written for the classic 9x9 soduku board, but can also be modified for other grid size variations*
