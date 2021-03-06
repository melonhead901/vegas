import random
from actions import Actions
from agent import Agent

class QLearningAgent(Agent):

    def __init__(self, alpha, discount, epsilon):
        self.alpha = alpha
        self.discount = discount
        self.epsilon = epsilon

        self.q_values = {}
        self.last_action = None
        self.last_features = None

        self.states_seen = {}
        self.no_policy_moves_made = 0

    def getQValue(self, features, action):
        return self.q_values.get((features, action), 0.0)

    def getValue(self, features, hand):
        actions = hand.getPossibleActions()
        if not actions:
          return 0.0
        else:
          return max(map(lambda action: self.getQValue(features, action), actions))

    def getPolicy(self, features, hand):
        # Cheating
        if features[0] <= 8:
          return Actions.HIT

        actions = hand.getPossibleActions()
        if not actions:
          return None
        else:
          no_policy = True

          max_value = None
          best_actions = []
          for action in actions:
            if self.q_values.has_key((features, action)):
              no_policy = False

            value = self.getQValue(features, action)
            if value > max_value:
              max_value = value
              best_actions = [action]
            elif value == max_value:
              best_actions.append(action)

          if no_policy:
            self.no_policy_moves_made += 1
          return random.choice(best_actions)

    def stateToFeatures(self, gameState, playerHand):
        hands = map(lambda hand: (hand.getHardCount(), hand.getHasAce()), gameState.getPlayerHands().keys())
        features = (
            playerHand.getHardCount(),
            playerHand.getHasAce(),
            # tuple(hands), # ignore other hands
            gameState.getDealerUpCard().getSoftCount())
        return features

    def update(self, features, hand, reward):
        key = (self.last_features, self.last_action)
        self.states_seen[key] = self.states_seen.get(key, 0) + 1

        value = self.getValue(features, hand)
        q_value = self.q_values.get((self.last_features, self.last_action), 0.0)
        self.q_values[(self.last_features, self.last_action)] = \
            (1.0 - self.alpha) * q_value + self.alpha * (reward + self.discount * value)

    def getNextAction(self, gameState, hand):
        features = self.stateToFeatures(gameState, hand)
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
        features = self.stateToFeatures(gameState, hand)
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

    def needsTraining(self):
      return True

    def trainingOver(self):
      self.epsilon = 0.0
      self.alpha = 0.0
      self.no_policy_moves_made = 0
