import pacman

'''
metarun.py runs things that look like command-line arguments
for Berkeley Python. You can leave the 'python pacman.py' part
at the beginning, or remove it, since we are not really running
from the command line.

You should comment out all lines in the file except one!
'''

# question 1 - evaluation function
#pacman.main('python pacman.py -p ReflexAgent -l testClassic')
#pacman.main('python pacman.py --frameTime 0 -p ReflexAgent -k 1')
#pacman.main('python pacman.py --frameTime 0 -p ReflexAgent -k 2')

# question 2 - minmax algorithm
#pacman.main('python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4')
#pacman.main('python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3')

# question 3 - alpha-beta pruning
#pacman.main('python pacman.py -p MinimaxAgent -l smallClassic -a depth=2')
#pacman.main('python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic')

# question 4 - expectimax
#pacman.main('python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3')
#pacman.main('python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10')
#pacman.main('python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10')

# question 5 - better evaluation function
pacman.main('python pacman.py -p AlphaBetaAgent -l mediumClassic -a depth=3')