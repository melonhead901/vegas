import random

from agent import Agent
from blackjack_markov_decision_process import BlackjackMarkovDecisionProcess

class ValueIterationAgent(Agent):
  def __init__(self, iterations):
    self.mdp = BlackjackMarkovDecisionProcess()
    self.values = {}
    self.discount = 0.9
    states = self.mdp.getStates()
    for _ in range(0, iterations):
      nextValues = {}
      for state in states:
        if self.mdp.isTerminal(state):
          nextValues[state] = self.values.get(state, 0)
        else:
          nextValues[state] = max(
            map(lambda action: self.getQValue(state, action),
                self.mdp.getPossibleActions(state)))
      self.values = nextValues

  def getNextAction(self, gameState, hand):
    state = (False, len(hand.getCards()) == 2, hand.isDoubleDown(),
             hand.getHasAce(), hand.getHardCount(),
             gameState.getDealerUpCard().getSoftCount())
    return self.getActionForState(state)

  def getActionForState(self, state):
    actions = self.mdp.getPossibleActions(state)
    if not actions:
      return None
    else:
      maxValue, maxActions = None, []
      for action in actions:
        value = self.getQValue(state, action)
        if value == maxValue:
          maxActions.append(action)
        elif value > maxValue:
          maxValue, maxActions = value, [action]
      return random.choice(maxActions)

  def getQValue(self, state, action):
    """
    The q-value of the state-action pair.
    """
    statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
    qValue = 0
    for transitionState, prob in statesAndProbs:
      reward = self.mdp.getReward(state, action, transitionState)
      qValue += prob * (reward + self.discount * self.values.get(transitionState, 0))
    return qValue

  def printPolicies(self):
    for hasAce in [False, True]:
      if not hasAce:
        labelString = "sc"
      else:
        labelString = "aces"
      for dealerSoftCount in range(2, 12):
        labelString = "{0}\t{1}".format(labelString, dealerSoftCount)
      print labelString
      for hardCount in range(2, 22):
        formatString = "{0}".format(hardCount)
        for dealerSoftCount in range(2, 12):
          state = (False, True, False, hasAce, hardCount, dealerSoftCount)
          action = self.getActionForState(state)
          formatString += "\t{0}".format(action[0])
        print formatString

  def __str__(self):
    return "Value iteration agent"
