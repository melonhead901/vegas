import random

from actions import Actions
from agent import Agent
from card import Card

class QLearningAgent(Agent):

    #TODO: discount?
    def __init__(self, alpha=0.2, discount=0.8, epsilon=0.1):
        self.alpha = alpha
        self.discount = discount
        self.epsilon = epsilon
    
        self.q_values = {}
        self.last_action = None
        self.last_features = None
  
    def getQValue(self, features, action):
        return self.q_values.get((features, action), 0.0)
  
    def getValue(self, features, hand):
        actions = hand.getPossibleActions()
        if not actions:
          return 0.0
        else:
          return max(map(lambda action: self.getQValue(features, action), actions))
  
    def getPolicy(self, features, hand):
        if features[0][0][0] <= 11:
          return Actions.HIT

        actions = hand.getPossibleActions()
        if not actions:
          return None
        else:
          max_value = None
          best_actions = []
          for action in actions:
            value = self.getQValue(features, action)
            if value > max_value:
              max_value = value
              best_actions = [action]
            elif value == max_value:
              best_actions.append(action)
          return random.choice(best_actions)
  
    def stateToFeatures(self, gameState):
        hands = map(lambda hand: (hand.getSoftCount(), hand.getHardCount()), gameState.getPlayerHands().keys())
        features = (
            tuple(hands), # TODO: can see everyone's hand atm - fine w/ just one agent
            gameState.getDealerUpCard().getSoftCount())
        return features

    def update(self, features, hand, reward):
#        if self.last_features == (((20, 20),), 7) and self.last_action == Actions.STAND:
#          print 'here %f (reward: %f) (last_action: %s) (q_values: %f, %f)' % \
#              (self.q_values.get((self.last_features, self.last_action), 0.0), \
#               reward, \
#               self.last_action,
#               self.q_values.get((self.last_features, Actions.HIT), 0.0), \
#               self.q_values.get((self.last_features, Actions.STAND), 0.0))

        value = self.getValue(features, hand)
#        if self.last_features == (((20, 20),), 7) and self.last_action == Actions.STAND:
#            print '\tvalue %f' % value
        q_value = self.q_values.get((self.last_features, self.last_action), 0.0)
#        if self.last_features == (((20, 20),), 7) and self.last_action == Actions.STAND:
#            print '\tq_value %f' % q_value
        self.q_values[(self.last_features, self.last_action)] = \
            (1.0 - self.alpha) * q_value + self.alpha * (reward + self.discount * value)

#        if self.last_features == (((20, 20),), 7) and self.last_action == Actions.STAND:
#            print '\tthere %f' % self.q_values.get((self.last_features, self.last_action), 0.0)

    def getNextAction(self, gameState, hand):
        features = self.stateToFeatures(gameState)
        if self.last_features and self.last_action:
            self.update(features, hand, 0.0)

        actions = hand.getPossibleActions()
        
        if not actions:
            action = None
        elif random.random() < self.epsilon:
            action = random.choice(actions)
        else:
            action = self.getPolicy(features, hand)

        self.last_action = action
        self.last_features = features

        return action

    def gameOver(self, gameState, hand, reward):
        features = self.stateToFeatures(gameState)
        self.update(features, hand, reward)

        self.last_action = None
        self.last_features = None

    def lose(self, gameState, hand):
        self.gameOver(gameState, hand, -hand.getBet())

    def win(self, gameState, hand):
        self.gameOver(gameState, hand, hand.getBet())

    def tie(self, gameState, hand):
        self.gameOver(gameState, hand, 0)

    def __str__(self):
        return "Q learning agent"
