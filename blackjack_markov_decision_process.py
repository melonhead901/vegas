from actions import Actions
from card import Card
from hand import Hand
from markov_decision_process import MarkovDecisionProcess

class BlackjackMarkovDecisionProcess(MarkovDecisionProcess):
  """
  For the blackjack Markov decision process,
  states are taken to be of the form
  (isDone, hasAce, hardCount, dealerSoftCount).
  isDone signals whether the agent can no longer
  act upon the hand (i.e. after doubling down or
  standing) and the other values are self-explanatory.
  This results in a (relatively) small state space,
  making value iteration possible.
  """
  def getStates(self):
    """
    Return a list of all states in the MDP. This is
    an enumeration of all possible configurations of
    (isDone, hasAce, hardCount, dealerSoftCount).
    """
    # This enumerates all states regardless of whether
    # they are actually feasible.
    states = []
    for isDone in [True, False]:
      for hasAce in [True, False]:
        for hardCount in range(2, 32):
          for dealerSoftCount in range(2, 11):
            states.append((isDone, hasAce, hardCount, dealerSoftCount))
    return states

  def getPossibleActions(self, state):
    """
    Return list of possible actions from the
    given state.
    """
    isDone, hasAce, hardCount, dealerSoftCount = state
    if isDone:
      return []
    # TODO(snowden): Splitting and MDPs don't play nicely
    # together, but DOUBLE_DOWN should be reasonable.
    return [Actions.HIT, Actions.STAND]

  def getTransitionStatesAndProbs(self, state, action):
    """
    Returns list of (nextState, prob) pairs
    representing the states reachable from
    the given state using the given action
    along with their transition probabilities.
    """
    if self.isTerminal(state):
      return []

    isDone, hasAce, hardCount, dealerSoftCount = state
    if action == Actions.STAND:
      return [((True, hasAce, hardCount, dealerSoftCount), 1)]
    elif action == Actions.HIT or action == Actions.DOUBLE_DOWN:
      if action == Actions.DOUBLE_DOWN:
        isDone = True
      statesAndProbs = []
      for cardValue in range(1, 11):
        # Compute probabilities without regard for card-counting.
        prob = 1.0 / 13.0 if cardValue < 10 else 4.0 / 13.0
        statesAndProbs.append(((isDone, hasAce or cardValue == 1,
                               hardCount + cardValue, dealerSoftCount),
                              prob))
        return statesAndProbs
    else:
      raise ValueError("Action {0} is not supported in the " \
                         "blackjack MDP".format(action))

  def getReward(self, state, action, transitionState):
    isDone, hasAce, hardCount, dealerSoftCount = transitionState
    if hardCount > 21:
      return -1

    # TODO(snowden): Make this less terrible.
    # I didn't have a way of associating win/lose/tie
    # and reward, so I made the poor choice of just
    # picking some reward value anyway. I'll need to
    # figure out how this is actually going to work.
    softCount = hardCount + 10 if hasAce and hardCount <= 11 else hardCount
    if isDone:
      return max((softCount - 16) / 5, 0)
    else:
      return 0

  def isTerminal(self, state):
    """
    Returns whether the given state is a terminal state.
    """
    isDone, hasAce, hardCount, dealerSoftCount = state
    return isDone or hardCount >= 22
