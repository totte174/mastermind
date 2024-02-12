# Mastermind Solver
This project is a [mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) solver algorithm I implemented in python an afternoon. Try it out!

## Usage
```command
$ py mastermind.py
Make a code which consists of 4 numbers between 0 and 5.
My guess: [0, 0, 1, 1]
Result: 0,1
My guess: [3, 3, 2, 0]
Result: 0,2
My guess: [4, 2, 0, 2]
Result: 1,1
My guess: [2, 1, 3, 2]
Result: 1,2
My guess: [1, 2, 3, 4]
Result: 4,0
Wohoo! I won!
```
## How it works
It keeps track of all possible permutations (codes) given previous guesses. To determine next guess it uses a min-max algorithm to find the guess which decreases the number of possible permutations most.

## Performance
The guessing algorithm has complexity O(n<sup>2</sup>) to the number of possible permutations (codes) at this point in the game. This is not a problem however for normal games where it will always find the optimal solution in less than a tenth of a second. However using a higher number of colors or pegs the amount of permutations increases greatly and thus complexity becomes a great issue.
