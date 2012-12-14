'''
Created on Dec 13, 2012

@author: Kellen
'''

from q_learning_agent import QLearningAgent

"""
Q-Learning agent that also takes into account counting:

Table from:
http://en.wikipedia.org/wiki/Card_counting#Systems

Card Strategy    2    3    4    5    6    7    8    9    10, J, Q, K    A
Zen Count       +1    +1  +2    +2  +2   +1    0    0    -2            -1
"""
class CountLearningAgent(QLearningAgent):    
    def __init__(self, alpha=0.2, discount=0.8, epsilon=0.1):
        QLearningAgent.__init__(self, alpha=alpha, discount=discount, epsilon=epsilon)
        self.count = 0
    
    def gameOver(self, gameState, hand, reward):
        QLearningAgent.gameOver(self, gameState, hand, reward)
        for hand in gameState.playerHands:
            for card in hand:
                val = card.getValue()
                # The following is very order dependent.
                # If you want to change it be sure you know what you're doing.
                if val == 0: # A
                    self.count -= 1
                elif val >= 9: # 10 or higher
                    self.count -= 2
                elif val == 6 or val <= 2 : # 7, 2, or 3
                    self.count += 1
                elif val >= 3 and val <= 5: # 4, 5, 6
                    self.count += 2
                # else 8 or 9, no change to count
                
    def stateToFeatures(self, gameState, playerHand):
        return QLearningAgent.stateToFeatures(self, gameState, playerHand) + (self.count,)
    
    
    def __str__(self):
        return "Count learning agent"