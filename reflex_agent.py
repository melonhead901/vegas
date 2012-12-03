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
        if hand.canSplit():
            return self.usePairTable(gameState, hand)
        elif hand.getHasAce():
            return self.useAceTable(gameState, hand)
        else:
            return self.useNoAceTable(gameState, hand)

    def usePairTable(self, gameState, hand):
        dealerVal = gameState.getDealerHand().getUpCard().getSoftCount()
        cardVal = hand.getCards()[0].getSoftCount()
        if cardVal == 10 or (cardVal == 9 and dealerVal == 7 or dealerVal >= 10):
            return Actions.STAND
        elif cardVal == 5 and dealerVal >= 2 and dealerVal <= 9:
            return Actions.DOUBLE_DOWN if hand.canDoubleDown() else Actions.HIT
        elif (cardVal >= 2 and cardVal <= 7 and dealerVal >= 8) or \
                (cardVal == 4 and (dealerVal <= 4 or dealerVal == 7)) or \
                (cardVal == 6 and dealerVal == 6):
            return Actions.HIT
        else:
            return Actions.SPLIT

    def useAceTable(self, gameState, hand):
        dealerVal = gameState.getDealerHand().getUpCard().getSoftCount()
        if hand.getSoftCount() >= 19:
            return Actions.STAND
        elif hand.getSoftCount() == 18:
            if dealerVal >= 9:
                return Actions.HIT
            elif dealerVal == 2 or dealerVal == 7 or dealerVal == 8 or \
                    not hand.canDoubleDown():
                return Actions.STAND
            else:
                return Actions.DOUBLE_DOWN
        elif (hand.getSoftCount() == 17 and dealerVal >= 3 and dealerVal <= 6) or \
                ((hand.getSoftCount() == 16 or hand.getSoftCount() == 15) and \
                     dealerVal >= 4 and dealerVal <= 6) or \
                ((hand.getSoftCount() == 13 or hand.getSoftCount() == 14) and \
                     dealerVal == 5 or dealerVal == 6):
            return Actions.DOUBLE_DOWN if hand.canDoubleDown() else Actions.HIT
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
        elif (hand.getValidCount() == 11 and dealerVal <= 10) or \
                (hand.getValidCount() == 10 and dealerVal <= 9) or \
                (hand.getValidCount() == 9 and dealerVal >= 3 and dealerVal <= 6):
            return Actions.DOUBLE_DOWN if hand.canDoubleDown() else Actions.HIT
        else:
            return Actions.HIT

    def __str__(self):
        return "Reflex agent"
