from actions import Actions
from card import Card
from dealer_agent import DealerAgent
from deck import Deck
from hand import Hand
from markov_decision_process import MarkovDecisionProcess

class BlackjackMarkovDecisionProcess(MarkovDecisionProcess):
  """
  For the blackjack Markov decision process,
  states are taken to be of the form
  (isDone, isFirst, isDoubleDown, hasAce, hardCount, dealerSoftCount).
  isDone signals whether the agent can no longer
  act upon the hand (i.e. after doubling down or
  standing), isFirst signals whether this is the
  agent's first action (i.e. the agent has two cards)
  and the other values are self-explanatory.
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
      for isFirst in [True, False]:
        for isDoubleDown in [True, False]:
          for hasAce in [True, False]:
            for hardCount in range(2, 32):
              for dealerSoftCount in range(2, 11):
                states.append((isDone, isFirst, isDoubleDown, hasAce, hardCount, dealerSoftCount))
    return states

  def getPossibleActions(self, state):
    """
    Return list of possible actions from the
    given state.
    """
    isDone, isFirst, isDoubleDown, hasAce, hardCount, dealerSoftCount = state
    if isDone:
      return []
    elif isFirst:
      return [Actions.HIT, Actions.STAND, Actions.DOUBLE_DOWN]
    else:
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

    isDone, isFirst, isDoubleDown, hasAce, hardCount, dealerSoftCount = state
    if action == Actions.STAND:
      return [((True, isFirst, isDoubleDown, hasAce, hardCount, dealerSoftCount), 1)]
    elif action == Actions.HIT or action == Actions.DOUBLE_DOWN:
      if action == Actions.DOUBLE_DOWN:
        isDone = True
        isDoubleDown = True
      statesAndProbs = []
      for cardValue in range(1, 11):
        # Compute probabilities without regard for card-counting.
        prob = 1.0 / 13.0 if cardValue < 10 else 4.0 / 13.0
        statesAndProbs.append(((isDone, False, isDoubleDown,
                                hasAce or cardValue == 1,
                                hardCount + cardValue, dealerSoftCount),
                               prob))
      return statesAndProbs
    else:
      raise ValueError("Action {0} is not supported in the " \
                         "blackjack MDP".format(action))

  def getReward(self, state, action, transitionState):
    isDone, isFirst, isDoubleDown, hasAce, hardCount, dealerSoftCount = transitionState
    multiplier = 2 if isDoubleDown else 1
    if hardCount > 21:
      return -2 * multiplier

    softCount = hardCount + 10 if hasAce and hardCount <= 11 else hardCount
    if isDone:
      if isFirst and softCount == 21:
        return multiplier
      # Simulate the dealer's actions
      dealerAgent = DealerAgent()
      dealerCardValue = dealerSoftCount - 1 if dealerSoftCount != 11 else 0
      card = Card(0, dealerCardValue)
      dealerHand = Hand(1)
      dealerHand.addCard(card)
      deck = Deck(1, 4, 13)
      dealerHand.addCard(deck.take())
      while dealerAgent.getNextAction(None, dealerHand) == Actions.HIT:
        dealerHand.addCard(deck.take())
      return multiplier if softCount > dealerHand.getSoftCount() else (
        0 if softCount == dealerHand.getSoftCount() else -multiplier)
    else:
      return 0

  def isTerminal(self, state):
    """
    Returns whether the given state is a terminal state.
    """
    isDone, isFirst, isDoubleDown, hasAce, hardCount, dealerSoftCount = state
    return isDone or hardCount >= 22
