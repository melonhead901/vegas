'''
Created on Dec 13, 2012

@author: Kellen
'''
import unittest

from card import Card
from deck import Deck
from game_state import GameState
from hand import Hand

from count_learning_agent import CountLearningAgent

class CountLearningAgentTest(unittest.TestCase):


    def setUp(self):
        # An agent every test can use
        self.agent = CountLearningAgent()

    def testNoCardNoCount(self):
        self.assertEqual(0, self.agent.count)        
        
    def testNoValCardsNoCount(self):
        hand = Hand(1)
        hand.addCard(Card(1, 6))        
        hand.addCard(Card(1, 6))
        self.agent.updateCount(hand)
        self.assertEqual(0, self.agent.count)
        
    def testOffsettingCardsNoCount(self):
        hand = Hand(1)
        hand.addCard(Card(1, 0))        
        hand.addCard(Card(1, 2))
        self.agent.updateCount(hand)
        self.assertEqual(0, self.agent.count)        
        
    def testEntireDeckNoCount(self):
        # The entire deck should be neutral
        deck = Deck(1, 4, 13)
        dealerHand = Hand(1)
        for _ in range(13):
            dealerHand.addCard(deck.take())
        playerHandMap = {}
        for i in range(3):
            hand = Hand(1)
            for _ in range(13):
                hand.addCard(deck.take())
            playerHandMap[hand] = i
                
        self.assertEqual(0, deck.numActiveCards())    
        gameState = GameState(playerHandMap, dealerHand, deck)
        self.agent.gameOver(gameState, playerHandMap.keys()[0], 1)
        self.assertEqual(0, self.agent.count)
        
    def testEntireDeckNoCountMultiRound(self):
        # The entire deck should be neutral
        deck = Deck(1, 4, 13)
        dealerHand = Hand(1)
        for _ in range(6):
            dealerHand.addCard(deck.take())
        playerHandMap = {}
        for i in range(3):
            hand = Hand(1)
            for _ in range(6):
                hand.addCard(deck.take())
            playerHandMap[hand] = i
                
        self.assertEqual(52-6*4, deck.numActiveCards())    
        gameState = GameState(playerHandMap, dealerHand, deck)
        self.agent.gameOver(gameState, playerHandMap.keys()[0], 1)
        
        dealerHand = Hand(1)
        for _ in range(7):
            dealerHand.addCard(deck.take())
        playerHandMap = {}
        for i in range(3):
            hand = Hand(1)
            for _ in range(7):
                hand.addCard(deck.take())
            playerHandMap[hand] = i
            
        self.assertEqual(0, deck.numActiveCards())   
        gameState = GameState(playerHandMap, dealerHand, deck)
        self.agent.gameOver(gameState, playerHandMap.keys()[0], 1)
        self.assertEqual(0, self.agent.count)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()