import autograder

'''
metagrade.py runs grading test cases. 

Call with -h to get the options

Call with an empty string to run all test cases.

Call with for example -q q1 for particular question.

Call with for example -t test_cases/q2/0-small-tree for one particular test case
'''

# autograder.main('')
# autograder.main('-q q1 --no-graphics')
# autograder.main('-q q2')
# autograder.main('-q q2 --no-graphics')
# autograder.main('-q q3')
# autograder.main('-q q3 --no-graphics')
# autograder.main('-q q4')
# autograder.main('-q q4 --no-graphics')
autograder.main('-q q5 --no-graphics')

# How to run one specific test case:
# autograder.main('-t test_cases/q2/0-small-tree')