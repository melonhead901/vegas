
class MarkovDecisionProcess:
  def getStates(self):
    """
    Return a list of all states in the MDP.
    """
    return NotImplemented

  def getPossibleActions(self, state):
    """
    Return a list of possible actions from the
    given state.
    """
    return NotImplemented

  def getTransitionStatesAndProbs(self, state, action):
    """
    Return a list of (nextState, prob) pairs
    representing the states reachable from
    the given state using the given action
    along with their transition probabilities.
    """
    return NotImplemented

  def getReward(self, state, action, transitionState):
    """
    Return the reward associated with the
    given transition.
    """
    return NotImplemented

  def isTerminal(self, state):
    """
    Return whether the given state is a
    terminal state.
    """
    return NotImplemented
