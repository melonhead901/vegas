import random

from actions import Actions
from agent import Agent

class QLearningAgent(Agent):

    def __init__(self, alpha=0.5, discount=1.0, epsilon=0.1):
        self.alpha = alpha
        self.discount = discount
        self.epsilon = epsilon
    
        self.q_values = {}
        self.last_action = None
        self.last_features = None
  
    def getQValue(self, features, action):
        return self.q_values.get((features, action), 0)
  
    def getValue(self, features):
        actions = [Actions.HIT, Actions.STAND]
        if len(actions) == 0:
          return 0.0
        else:
          return max(map(lambda action: self.getQValue(features, action), actions))
  
    def getPolicy(self, features):
        actions = [Actions.HIT, Actions.STAND]
        if len(actions) == 0:
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
        features = (
            tuple(gameState.getPlayerHands().keys()), # can see everyone's hand atm
            gameState.getDealerUpCard())
    
        return features
  
    def update(self, features, reward):
        value = self.getValue(features)
        q_value = self.q_values.get((self.last_features, self.last_action), 0)
        self.q_values[(self.last_features, self.last_action)] = (1.0 - self.alpha) * q_value
        self.q_values[(self.last_features, self.last_action)] += self.alpha * (reward + self.discount * value)
      

    def getNextAction(self, gameState):
        features = self.stateToFeatures(gameState)
        if self.last_features and self.last_action:
            self.update(features, 0.0)

        actions = [Actions.HIT, Actions.STAND]
        
        if len(actions) == 0:
            result = None
        elif random.random() < self.epsilon:
            result = random.choice(actions)
        else:
            result = self.getPolicy(gameState)

        self.last_action = result
        self.last_features = features

        return result

    def gameOver(self, gameState, reward):
        features = self.stateToFeatures(gameState)
        self.update(features, reward)

        self.last_action = None
        self.last_features = None

    def lose(self, gameState):
        print "losed"
        self.gameOver(gameState, -1.0)

    def win(self, gameState):
        print "winned"
        self.gameOver(gameState, 1.0)

    def tie(self, gameState):
        print "tied"
        self.gameOver(gameState, 0.0)
