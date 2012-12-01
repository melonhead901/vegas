'''
Created on Nov 30, 2012

@author: Kellen
'''

class GameState(object):
    def getPlayerHands(self):
      return self.playerHands

    def setPlayerHands(self, hands):
      self.playerHands = hands

    def getDealerHand(self):
      return self.dealerHand

    def getDealerUpCard(self):
      return self.dealerHand.getUpCard()

    def setDealerHand(self, hand):
      self.dealerHand = hand

    def getDeck(self):
      return self.deck

    def setDeck(self, deck):
      self.deck = deck
