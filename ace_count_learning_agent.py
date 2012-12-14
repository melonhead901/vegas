'''
Created on Dec 13, 2012

@author: Kellen
'''

from count_learning_agent import CountLearningAgent

"""
Aces baby
"""
class AceCountLearningAgent(CountLearningAgent):
                
    def stateToFeatures(self, gameState, playerHand):
        aceCount = gameState.getDeck().aceCount
        return (CountLearningAgent.stateToFeatures(self, gameState, playerHand) + (aceCount,))
    
    def __str__(self):
        return "Ace Count learning agent"