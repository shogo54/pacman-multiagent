import pacman

'''
metarun.py runs things that look like command-line arguments
for Berkeley Python. You can leave the 'python pacman.py' part
at the beginning, or remove it, since we are not really running
from the command line.

You should comment out all lines in the file except one!
'''

# pacman.main('python pacman.py -p ReflexAgent -l testClassic')
pacman.main('python pacman.py --frameTime 0 -p ReflexAgent -k 1')
