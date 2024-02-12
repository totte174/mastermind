import argparse

class MasterMindSolver:
    def __init__(self, n_colors=6, pegs=4):
        self.n_colors = n_colors
        self.pegs = pegs
        self.possible_perms = self._all_perms()
        self.firstguess = True

    def guess(self, debug=False):
        if self.firstguess:
            self.firstguess = False
            return self._trivial_guess()
        
        # We use min-max to find the guess which gives the least amount of possible
        # permutations if we get the worst result
        best_guess = None
        min_max_entropy = len(self.possible_perms) + 1
        if debug:
            print("Number of possible permutations:", len(self.possible_perms))
        for guess in self.possible_perms:
            result_tracker = [0]*(self.pegs**2 + 1)
            for perm in self.possible_perms:
                w,b = self._result(guess, perm)
                result_tracker[w*self.pegs + b] += 1
            max_entropy = max(result_tracker)
            if max_entropy < min_max_entropy:
                best_guess = guess
                min_max_entropy = max_entropy
        if debug:
            print("Worst number of possible permutations after guess:", min_max_entropy)
        return best_guess

        
    def add_result(self, guess, result):
        self.possible_perms = self._possible_perms(guess, result)
        if len(self.possible_perms) == 0:
            raise Exception("Invalid guesses and results. No permutation possible for guesses and results.")

    def _possible_perms(self, guess, result):
        return [perm for perm in self.possible_perms if result == self._result(guess, perm)]
        
    def _result(self, guess, perm):
        white = 0
        brown = 0
        guess_tally = [0] * self.n_colors
        perm_tally = [0] * self.n_colors
        for peg in range(self.pegs):
            if guess[peg] == perm[peg]:
                white += 1
            else:
                guess_tally[guess[peg]] += 1
                perm_tally[perm[peg]] += 1
        for c in range(self.n_colors):
            brown += min(guess_tally[c], perm_tally[c])
        return white,brown
        
    def _trivial_guess(self):
        guess = []
        for c in range(self.n_colors):
            if len(guess) < self.pegs:
                guess.append(c)
            if len(guess) < self.pegs:
                guess.append(c)
        if len(guess) < self.pegs:
            guess.extend([0 for _ in range(self.pegs-len(guess))])
        return guess

    def _all_perms(self):
        return [[(x//(self.n_colors**peg))%self.n_colors for peg in range(self.pegs)] for x in range(self.n_colors**self.pegs)]
    
    def _all_results(self):
        results = []
        for w in range(self.pegs):
            for b in range(self.pegs-w+1):
                results.append((w,b))
        return results
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
'''Play a game of MasterMind (Cows and Bulls) againt the computer.
Computer guesses a list of colors for each peg. You answer the number of pegs correct in both color and position, as well as the number of pegs correct in color but not in position

    Example:
Your real list of pegs is [0,1,1,3,3,3]
Computer guesses [2,0,1,3,4,5]
You should answer 2,1 since 2 and 3 are correct in both position and color whilst 0 is only correct in color.''',
                                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--colors', '-c', action='store', type=int, default=6,
                        help='number of colors available for each peg (default: 6)')
    parser.add_argument('--pegs', '-p', action='store', type=int, default=4,
                        help='number of pegs (default: 4)')
    parser.add_argument('--debug', action='store_true',
                        help='shows debug information')
    args = parser.parse_args()

    solver = MasterMindSolver(n_colors=args.colors,pegs=args.pegs)
    print(f"Make a code which consists of {args.pegs} numbers between 0 and {args.colors - 1}.")
    for i in range(1000):
        guess = solver.guess(debug=args.debug)
        print("My guess:", guess)
        result = input("Result: ")
        result = tuple(int(x) for x in result.split(","))
        solver.add_result(guess, result)
        if result == (args.pegs,0):
            print("Wohoo! I won!")
            break