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
    
    # Value      0  1  2  3  4  5  6  7  8  9  10   11  12
    # Card       A  2  3  4  5  6  7  8  9  0   J    Q  K
    ValueArr = [-1, 1, 1, 1, 1, 1, 0, 0, 0, -1, -1, -1, -1]  # Simple
    
    #ValueArr = [-1, 1, 1, 2, 2, 2, 1, 0, 0, -2, -2, -2, -2]  #Complicated
    
    def __init__(self, alpha=0.2, discount=0.8, epsilon=0.1):
        QLearningAgent.__init__(self, alpha=alpha, discount=discount, epsilon=epsilon)
        self.count = 0
    
    def gameOver(self, gameState, hand, reward):
        QLearningAgent.gameOver(self, gameState, hand, reward)
        #print gameState.playerHands
        for hand in gameState.playerHands.keys():
            self.updateCount(hand)
        self.updateCount(gameState.dealerHand)
    
    def updateCount(self, hand):        
            for card in hand.getCards():
                self.count += CountLearningAgent.ValueArr[card.value]
                
    def stateToFeatures(self, gameState, playerHand):
        reportedCount = gameState.getDeck().count
        # Constrain the count to be in the range [-10, 10]
        reportedCount = min(reportedCount, 10)
        reportedCount = max(reportedCount, -10)
        # print reportedCount
        return (QLearningAgent.stateToFeatures(self, gameState, playerHand) + (reportedCount,))
    
    def __str__(self):
        return "Count learning agent"