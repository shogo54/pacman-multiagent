# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import searchAgents
import sys
from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        minDisToGhost = sys.maxint
        for ghostState in newGhostStates:
            disToGhost = searchAgents.aStarMazeDistance(ghostState.getPosition(), newPos, currentGameState)
            if minDisToGhost > disToGhost:
                minDisToGhost = disToGhost
        if minDisToGhost <= 1:
            return -sys.maxint - 1

        closestFoods = []
        minDisToFood = sys.maxint
        for foodPos in newFood.asList():
            disToFood = searchAgents.aStarMazeDistance(foodPos, newPos, currentGameState)
            if minDisToFood > disToFood:
                minDisToFood = disToFood
                closestFoods = [foodPos]
            elif minDisToFood == disToFood:
                closestFoods.append(foodPos)
        if minDisToFood == sys.maxint:
            return minDisToFood

        return 2 * successorGameState.getScore() - minDisToFood - len(newFood.asList())


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        bestValue = -sys.maxint - 1
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)
            actionValue = self.getMinMaxValue(successorGameState, 0, 0)
            if bestValue <= actionValue:
                bestValue = actionValue
                bestAction = action
        return bestAction

    def getMinMaxValue(self, gameState, currentDepth, agentIndex):
        agentIndex += 1
        if agentIndex == gameState.getNumAgents():
            agentIndex = 0
            currentDepth += 1
        if currentDepth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, currentDepth, agentIndex)
        if agentIndex >= 1:
            return self.minValue(gameState, currentDepth, agentIndex)

    def maxValue(self, gameState, currentDepth, agentIndex):
        val = -sys.maxint - 1
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        for nextAction in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, nextAction)
            val = max(val, self.getMinMaxValue(successorGameState, currentDepth, agentIndex))
        return val

    def minValue(self, gameState, currentDepth, agentIndex):
        val = sys.maxint
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        for nextAction in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, nextAction)
            val = min(val, self.getMinMaxValue(successorGameState, currentDepth, agentIndex))
        return val


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        bestValue = -sys.maxint - 1
        alpha = -sys.maxint - 1
        beta = sys.maxint
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)
            actionValue = self.getMinMaxValue(successorGameState, 0, 0, alpha, beta)
            if bestValue <= actionValue:
                bestValue = actionValue
                bestAction = action
            if actionValue > beta:
                return action
            alpha = max(alpha, actionValue)
        return bestAction

    def getMinMaxValue(self, gameState, currentDepth, agentIndex, alpha, beta):
        agentIndex += 1
        if agentIndex == gameState.getNumAgents():
            agentIndex = 0
            currentDepth += 1
        if currentDepth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.alphaBetaMaxValue(gameState, currentDepth, agentIndex, alpha, beta)
        if agentIndex >= 1:
            return self.alphaBetaMinValue(gameState, currentDepth, agentIndex, alpha, beta)

    def alphaBetaMaxValue(self, gameState, currentDepth, agentIndex, alpha, beta):
        val = -sys.maxint - 1
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        for nextAction in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, nextAction)
            val = max(val, self.getMinMaxValue(successorGameState, currentDepth, agentIndex, alpha, beta))
            if val > beta:
                return val
            alpha = max(alpha, val)
        return val

    def alphaBetaMinValue(self, gameState, currentDepth, agentIndex, alpha, beta):
        val = sys.maxint
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        for nextAction in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, nextAction)
            val = min(val, self.getMinMaxValue(successorGameState, currentDepth, agentIndex, alpha, beta))
            if val < alpha:
                return val
            beta = min(beta, val)
        return val


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        bestValue = -sys.maxint - 1
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)
            actionValue = self.getExpectiMaxValue(successorGameState, 0, 0)
            if bestValue <= actionValue:
                bestValue = actionValue
                bestAction = action
        return bestAction

    def getExpectiMaxValue(self, gameState, currentDepth, agentIndex):
        agentIndex += 1
        if agentIndex == gameState.getNumAgents():
            agentIndex = 0
            currentDepth += 1
        if currentDepth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, currentDepth, agentIndex)
        if agentIndex >= 1:
            return self.expectiValue(gameState, currentDepth, agentIndex)

    def maxValue(self, gameState, currentDepth, agentIndex):
        val = -sys.maxint - 1
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        for nextAction in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, nextAction)
            val = max(val, self.getExpectiMaxValue(successorGameState, currentDepth, agentIndex))
        return val

    def expectiValue(self, gameState, currentDepth, agentIndex):
        val = 0
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        for nextAction in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, nextAction)
            val += self.getExpectiMaxValue(successorGameState, currentDepth, agentIndex)/len(legalActions)
        return val


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      this is apparently same as my evaluation function
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    minDisToGhost = sys.maxint
    for ghostState in newGhostStates:
        disToGhost = searchAgents.aStarMazeDistance(ghostState.getPosition(), newPos, currentGameState)
        if minDisToGhost > disToGhost:
            minDisToGhost = disToGhost
    if minDisToGhost <= 1:
        return -sys.maxint - 1

    closestFoods = []
    minDisToFood = sys.maxint
    for foodPos in newFood.asList():
        disToFood = searchAgents.aStarMazeDistance(foodPos, newPos, currentGameState)
        if minDisToFood > disToFood:
            minDisToFood = disToFood
            closestFoods = [foodPos]
        elif minDisToFood == disToFood:
            closestFoods.append(foodPos)
    if minDisToFood == sys.maxint:
        return minDisToFood

    return 2 * currentGameState.getScore() - minDisToFood - len(newFood.asList())



# Abbreviation
better = betterEvaluationFunction
