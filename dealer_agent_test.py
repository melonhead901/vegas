'''
Created on Nov 30, 2012

@author: Kellen
'''
import unittest
from hand import Hand
from card import Card
from dealer_agent import DealerAgent
from actions import Actions


class DealerAgentTest(unittest.TestCase):

    # Hand where the dealer should hit based on hard count
    def test_4CardHand(self):
        hand = Hand()
        hand.addCard(Card(1, 6))
        hand.addCard(Card(1, 4))
        hand.addCard(Card(1, 2))
        hand.addCard(Card(1, 0))
        dealer = DealerAgent()
        dealer.receiveHand(hand)
        self.assertEqual(Actions.HIT, dealer.getNextAction(None))

    # Hand where the dealer should stand based on soft count
    def test_Soft17(self):
        hand = Hand()
        hand.addCard(Card(1, 6))
        hand.addCard(Card(1, 0))
        dealer = DealerAgent()
        dealer.receiveHand(hand)
        self.assertEqual(Actions.STAND, dealer.getNextAction(None))


if __name__ == "__main__":
    unittest.main()