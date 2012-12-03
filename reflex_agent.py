'''
Created on Nov 30, 2012

@author: Kellen
'''

from actions import Actions
from agent import Agent

"""
Pretty intelligent agent build from tables on Wikipedia
http://en.wikipedia.org/wiki/Blackjack#Blackjack_strategy
TODO(kellend): Expand when we add in Split, Double, etc.
"""
class ReflexAgent(Agent):
        def getNextAction(self, gameState, hand):
            if hand.getHasAce():
                return self.useAceTable(gameState, hand)
            else:
                return self.useNoAceTable(gameState, hand)
            
        def useAceTable(self, gameState, hand):
            if hand.getSoftCount() >= 19:
                return Actions.STAND
            elif hand.getSoftCount() == 18:
                if gameState.getDealerHand().getUpCard().getSoftCount() >= 9:
                    return Actions.HIT
                else:
                    return Actions.STAND
            else:
                return Actions.HIT
            
        def useNoAceTable(self, gameState, hand):
            dealerVal = gameState.getDealerHand().getUpCard().getSoftCount()
            if hand.getValidCount() >= 17:
                return Actions.STAND
            elif hand.getValidCount() >= 13:
                if dealerVal >= 7:
                    return Actions.HIT
                else:
                    return Actions.STAND
            elif hand.getValidCount() == 12:
                if dealerVal >= 7 or dealerVal <= 3:
                    return Actions.HIT
                else:
                    return Actions.STAND
            else:
                return Actions.HIT

        def __str__(self):
            return "Reflex agent"
