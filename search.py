# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from util import Stack, Queue
from util import PriorityQueue as PQ


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    # set up
    to_visit = Stack()  # stack or Queue of nodes to visit
    visited = set()  # set of nodes visited
    paths = {}  # dict from dot to paths
    goal = ()  # tuple of goal state

    # put first node
    start = problem.getStartState()
    to_visit.push(start)
    paths[start] = []

    # process for each
    while not to_visit.isEmpty():
        current = to_visit.pop()
        if problem.isGoalState(current):
            goal = current
            break
        for (nextloc, dir, cost) in problem.getSuccessors(current):
            if not nextloc in visited:
                to_visit.push(nextloc)
                paths[nextloc] = paths[current] + [dir]
        visited.add(current)

    return paths[goal]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # set up
    to_visit = Queue()  # stack or Queue of nodes to visit
    visited = set()  # set of nodes visited
    paths = {}  # dict from dot to paths
    goal = ()  # tuple of goal state

    # put first node
    start = problem.getStartState()
    to_visit.push(start)
    paths[start] = []

    # process for each
    while not to_visit.isEmpty():
        current = to_visit.pop()
        if problem.isGoalState(current):
            goal = current
            break
        if current in visited:
            continue
        for (nextloc, dir, cost) in problem.getSuccessors(current):
            if not nextloc in visited:
                to_visit.push(nextloc)
                if not nextloc in paths:
                    paths[nextloc] = paths[current] + [dir]
        visited.add(current)

    return paths[goal]


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # set up
    to_visit = PQ()  # PQ of nodes to visit
    visited = set()  # set of nodes visited
    paths = {}  # dict from dot to paths
    goal = ()  # tuple of goal state

    # put first node
    start = problem.getStartState()
    to_visit.push(start,0)
    paths[start] = ([],0)

    # process for each node
    while not to_visit.isEmpty():
        current, way = to_visit.popPrioNItem()
        if problem.isGoalState(current):
            goal = current
            break
        if current in visited:
            continue
        for (nextloc, dir, cost) in problem.getSuccessors(current):
            if not nextloc in visited:
                to_visit.push(nextloc, way+cost)
                if not nextloc in paths or (nextloc in paths and way+cost < paths[nextloc][1]):
                    paths[nextloc] = (paths[current][0] + [dir], paths[current][1] + cost)
        visited.add(current)

    return paths[goal][0]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # set up
    to_visit = PQ()  # PQ of nodes to visit
    visited = set()  # set of nodes visited
    paths = {}  # dict from dot to paths
    goal = ()  # tuple of goal state

    # put first node
    start = problem.getStartState()
    to_visit.push(start, 0 + heuristic(start, problem))     # put first node and cost (0) + heuristic
    paths[start] = ([], 0)       # path does not contain heuristic

    # process for each node
    while not to_visit.isEmpty():
        current, way = to_visit.popPrioNItem()
        way -= heuristic(current, problem)       # way from PQ includes heuristic so reduce it
        if problem.isGoalState(current):
            goal = current
            break
        if current in visited:
            continue
        for (nextloc, dir, cost) in problem.getSuccessors(current):
            if not nextloc in visited:
                to_visit.push(nextloc,  way + cost + heuristic(nextloc, problem))
                if not nextloc in paths or (nextloc in paths and way + cost < paths[nextloc][1]):
                    paths[nextloc] = (paths[current][0] + [dir], paths[current][1] + cost)
        visited.add(current)

    return paths[goal][0]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
