'''
Created on Nov 30, 2012

@author: Kellen
'''
import unittest

from game import Game
from hand import Hand
from card import Card

"""
Test the win/lose game logic.
TODO(kellend): Test game using its public interface.
"""
class GameLogicTest(unittest.TestCase):
    
    def setUp(self):
        dealerAgent = None
        playerAgents = None
        self.game = Game(dealerAgent, playerAgents)
        self.playaHand = Hand()
        self.dealerHand = Hand()
        
    # Ensure that player blackjack beats dealer non-blackjack
    def testPlayaBlackjackBeatsDealerNonBlackJack(self):
        self.playaHand.addCard(Card(1, 0))
        self.playaHand.addCard(Card(1, 10))
        self.dealerHand.addCard(Card(1, 4))
        self.dealerHand.addCard(Card(1, 5))
        self.dealerHand.addCard(Card(1, 10))        
        self.assertGreater(self.game.determineWinner(self.playaHand, self.dealerHand), 0)        
        
    # Ensure that player blackjack beats dealer non-blackjack
    def testPlaya17LosesDealer21(self):
        self.playaHand.addCard(Card(1, 0))
        self.playaHand.addCard(Card(1, 6))
        self.dealerHand.addCard(Card(1, 4))
        self.dealerHand.addCard(Card(1, 5))
        self.dealerHand.addCard(Card(1, 10))        
        self.assertLess(self.game.determineWinner(self.playaHand, self.dealerHand), 0)        
        
    # Ensure that player blackjack beats dealer blackjack
    def testPlayaBlackJackLosesDealerBlackjack(self):
        self.playaHand.addCard(Card(1, 0))
        self.playaHand.addCard(Card(1, 10))
        self.dealerHand.addCard(Card(1, 0))
        self.dealerHand.addCard(Card(1, 10))        
        self.assertGreater(self.game.determineWinner(self.playaHand, self.dealerHand), 0)
        
    # Ensure that player blackjack beats dealer blackjack
    def testPlaya21LosesDealerBlackjack(self):
        self.playaHand.addCard(Card(1, 4))
        self.playaHand.addCard(Card(1, 5))
        self.playaHand.addCard(Card(1, 10))
        self.dealerHand.addCard(Card(1, 0))
        self.dealerHand.addCard(Card(1, 10))        
        self.assertLess(self.game.determineWinner(self.playaHand, self.dealerHand), 0)
        
    # Ensure that player bust loses to dealer bust
    def testPlayaBustLosesDealerBust(self):
        self.playaHand.addCard(Card(1, 5))
        self.playaHand.addCard(Card(1, 6))
        self.playaHand.addCard(Card(1, 10))
        self.dealerHand.addCard(Card(1, 5))
        self.dealerHand.addCard(Card(1, 5))
        self.dealerHand.addCard(Card(1, 10))        
        self.assertLess(self.game.determineWinner(self.playaHand, self.dealerHand), 0)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
