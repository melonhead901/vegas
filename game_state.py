'''
Created on Nov 30, 2012

@author: Kellen
'''

class GameState(object):
    def __init__(self, playerHands, dealerHand, deck):
        self.playerHands = playerHands
        self.dealerHand = dealerHand
        self.deck = deck

    def getPlayerHands(self):
      return self.playerHands

    def getDealerHand(self):
      return self.dealerHand

    def getDealerUpCard(self):
      return self.dealerHand.getUpCard()

    def getDeck(self):
      return self.deck
