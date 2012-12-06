import mdp

class BlackjackMDP(mdp.MarkovDecisionProcess):

  def getStates(self):
    """
    Return a list of all states in the MDP.
    Not generally possible for large MDPs.
    """
    raise NotImplemented
        
  def getStartState(self):
    """
    Return the start state of the MDP.
    """
    raise NotImplemented
    
  def getPossibleActions(self, state):
    """
    Return list of possible actions from 'state'.
    """
    return hand.getPossibleActions()
        
  def getTransitionStatesAndProbs(self, state, action):
    """
    Returns list of (nextState, prob) pairs
    representing the states reachable
    from 'state' by taking 'action' along
    with their transition probabilities.  
    """
    raise NotImplemented

  def getReward(self, state, action, nextState):
    """
    Get the reward for the state, action, nextState transition.
    
    Not available in reinforcement learning.
    """
    raise NotImplemented

  def isTerminal(self, state):
    """
    Returns true if the current state is a terminal state.  By convention,
    a terminal state has zero future rewards.  Sometimes the terminal state(s)
    may have no possible actions.  It is also common to think of the terminal
    state as having a self-loop action 'pass' with zero reward; the formulations
    are equivalent.
    """
    return hand.isBust() || ...
