import random

class MarkovDecisionProcess:
    
  def getStates(self):
    """
    Return a list of all states in the MDP.
    Not generally possible for large MDPs.
    """
    abstract
        
  def getStartState(self):
    """
    Return the start state of the MDP.
    """
    abstract
    
  def getPossibleActions(self, state):
    """
    Return list of possible actions from 'state'.
    """
    abstract
        
  def getTransitionStatesAndProbs(self, state, action):
    """
    Returns list of (nextState, prob) pairs
    representing the states reachable
    from 'state' by taking 'action' along
    with their transition probabilities.  
    """
    abstract
        
  def isTerminal(self, state):
    """
    Returns true if the current state is a terminal state.  By convention,
    a terminal state has zero future rewards.  Sometimes the terminal state(s)
    may have no possible actions.  It is also common to think of the terminal
    state as having a self-loop action 'pass' with zero reward; the formulations
    are equivalent.
    """
    abstract
