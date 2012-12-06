import random

from agent import Agent
from blackjack_markov_decision_process import BlackjackMarkovDecisionProcess

class ValueIterationAgent(Agent):
  def __init__(self, iterations):
    self.mdp = BlackjackMarkovDecisionProcess()
    self.values = {}
    self.discount = 0.9
    for iteration in range(0, iterations):
      nextValues = {}
      states = self.mdp.getStates()
      for state in states:
        if self.mdp.isTerminal(state):
          nextValues[state] = 0
        else:
          nextValues[state] = max(
            map(lambda action: self.getQValue(state, action),
                self.mdp.getPossibleActions(state)))
      self.values = nextValues

  def getNextAction(self, gameState, hand):
    state = (False, hand.getHasAce(), hand.getHardCount(),
             gameState.getDealerUpCard().getSoftCount())
    actions = self.mdp.getPossibleActions(state)
    if not actions:
      return None
    else:
      maxValue, maxActions = None, None
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
    # Q_{n+1}(s, a) = \sum_{s' \in S} Pr(s'|s,a)[U(s, a, s') + gamma * V_n(s')]
    qValue = 0
    for transitionState, prob in statesAndProbs:
      reward = self.mdp.getReward(state, action, transitionState)
      qValue += prob * (self.mdp.getReward(state, action, transitionState) +
                        self.discount * self.values.get(transitionState, 0))
    return qValue

  def __str__(self):
    return "Value iteration agent"
