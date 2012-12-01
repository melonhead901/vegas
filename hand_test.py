'''
Created on Nov 21, 2012

@author: Kellen
'''
import unittest
from hand import Hand
from card import Card

class Test(unittest.TestCase):
    def test_emptyHandHardCount(self):
        hand = Hand()
        self.assertEqual(0, hand.getHardCount(), "hard count wasn't 0 for empty deck")
        
    def test_emptyHandSoftCount(self):
        hand = Hand()
        self.assertEqual(0, hand.getSoftCount(), "soft count wasn't 0 for empty deck")
        
    def test_emptyHandValidCount(self):
        hand = Hand()
        self.assertEqual(0, hand.getValidCount(), "valid count wasn't 0 for empty deck")
        
    def test_emptyHandBlackJack(self):
        hand = Hand()
        self.assertFalse(hand.isBlackJack(), "empty hand isn't blackjack")
        
    def test_emptyHandNotBust(self):
        hand = Hand()
        self.assertFalse(hand.isBust())
        
    # Helper method, creates a hand with 2,3,4,5, valued at 14
    def createFourCard20PointHand(self):
        hand = Hand()
        hand.addCard(Card(1, 1))
        hand.addCard(Card(1, 2))
        hand.addCard(Card(1, 3))
        hand.addCard(Card(1, 4))
        return hand
        
    def test_fiveCardHardCount(self):
        hand = self.createFourCard20PointHand()
        self.assertEqual(14, hand.getHardCount())
        
    def test_fiveCardSoftCount(self):
        hand = self.createFourCard20PointHand()
        self.assertEqual(14, hand.getSoftCount())
        
    def test_fiveCardValidCount(self):
        hand = self.createFourCard20PointHand()
        self.assertEqual(14, hand.getValidCount())
        
    def test_fiveCardNoBlackjack(self):
        hand = self.createFourCard20PointHand()
        self.assertFalse(hand.isBlackJack())
        
    def test_fiveCardNoBust(self):
        hand = self.createFourCard20PointHand()
        self.assertFalse(hand.isBust())
        
    # Helper method, creates a hand with A, 7, valued at 8/18
    def createHandWithAce(self):
        hand = Hand()
        hand.addCard(Card(1, 0))
        hand.addCard(Card(1, 6))
        return hand
   
    def test_handWithAceSoftValue(self):     
        hand = self.createHandWithAce()
        self.assertEqual(18, hand.getSoftCount())
    
    def test_handWithAceHardValue(self):     
        hand = self.createHandWithAce()
        self.assertEqual(8, hand.getHardCount())
        
    def test_handWithAceValidValue(self):     
        hand = self.createHandWithAce()
        self.assertEqual(18, hand.getValidCount())
    
    def test_handWithAceBlackjack(self):
        hand = self.createHandWithAce()
        self.assertFalse(hand.isBlackJack())
        
    def test_handWithAceBust(self):
        hand = self.createHandWithAce()
        self.assertFalse(hand.isBust())
        
    # Helper method, creates a hand with A, 7, 5 valued at 13/23
    def createHandWithAceFive(self):
        hand = Hand()
        hand.addCard(Card(1, 0))
        hand.addCard(Card(1, 6))
        hand.addCard(Card(1, 4))
        return hand    
    
    def test_handWithAceFiveSoftValue(self):     
        hand = self.createHandWithAceFive()
        self.assertEqual(23, hand.getSoftCount())
    
    def test_handWithAceFiveHardValue(self):     
        hand = self.createHandWithAceFive()
        self.assertEqual(13, hand.getHardCount())
        
    def test_handWithAceFiveValidValue(self):     
        hand = self.createHandWithAceFive()
        self.assertEqual(13, hand.getValidCount())
    
    def test_handWithAceFiveBlackjack(self):
        hand = self.createHandWithAceFive()
        self.assertFalse(hand.isBlackJack())
        
    def test_handWithAceFiveBust(self):
        hand = self.createHandWithAceFive()
        self.assertFalse(hand.isBust())        
    
    def test_bustedHandWithAce(self):
        hand = Hand()
        hand.addCard(Card(1, 0))
        hand.addCard(Card(1, 6))
        hand.addCard(Card(1, 6))
        hand.addCard(Card(1, 9))
        self.assertTrue(hand.isBust())
    
    def test_blackJack(self):
        hand = Hand()
        hand.addCard(Card(1, 0))
        hand.addCard(Card(1, 10))
        self.assertTrue(hand.isBlackJack())

    def test_compare(self):
        hand1 = Hand()
        hand1.addCard(Card(0, 6))
        hand1.addCard(Card(0, 7))
        hand2 = Hand()
        hand2.addCard(Card(0, 9))
        hand2.addCard(Card(0, 3))
        self.assertGreater(hand1.compare(hand2), 0)
        self.assertLess(hand2.compare(hand1), 0)
        self.assertEqual(hand1.compare(hand1), 0)

        # BlackJack should beat a normal 21 hand.
        hand1 = Hand()
        hand1.addCard(Card(0, 0))
        hand1.addCard(Card(0, 11))
        self.assertTrue(hand1.isBlackJack())
        hand2 = Hand()
        hand2.addCard(Card(0, 3))
        hand2.addCard(Card(0, 9))
        hand2.addCard(Card(0, 6))
        self.assertEqual(21, hand2.getValidCount())
        self.assertFalse(hand2.isBlackJack())
        self.assertGreater(hand1.compare(hand2), 0)
        self.assertLess(hand2.compare(hand1), 0)
        self.assertEqual(hand1.compare(hand1), 0)

    def test_equality(self):
        hand1 = Hand()
        hand1.addCard(Card(0, 6))
        hand1.addCard(Card(0, 7))
        hand2 = Hand()
        hand2.addCard(Card(0, 9))
        hand2.addCard(Card(0, 3))
        self.assertNotEqual(hand1, hand2)

        hand1 = Hand()
        hand1.addCard(Card(0, 0))
        hand1.addCard(Card(0, 11))
        self.assertTrue(hand1.isBlackJack())
        hand2 = Hand()
        hand2.addCard(Card(0, 3))
        hand2.addCard(Card(0, 9))
        hand2.addCard(Card(0, 6))
        self.assertNotEqual(hand1, hand2)

        hand2 = Hand()
        hand2.addCard(Card(1, 0))
        hand2.addCard(Card(1, 11))
        self.assertNotEqual(hand1, hand2)

        hand2 = Hand()
        hand2.addCard(Card(0, 0))
        hand2.addCard(Card(0, 11))
        self.assertEqual(hand1, hand2)

    def test_str(self):
        hand = Hand()
        hand.addCard(Card(0, 6))
        hand.addCard(Card(2, 4))
        self.assertEqual("[7 of Clubs, 5 of Spades] with soft " \
                             "count 12 and hard count 12", str(hand))

        hand.addCard(Card(3, 10))
        self.assertEqual("[7 of Clubs, 5 of Spades, Jack of " \
                             "Hearts] with soft count 22 and " \
                             "hard count 22 (Bust)", str(hand))

        hand = Hand()
        hand.addCard(Card(0, 0))
        hand.addCard(Card(0, 12))
        self.assertEqual("[Ace of Clubs, King of Clubs] with " \
                             "soft count 21 and hard count 11 " \
                             "(BlackJack)", str(hand))
        
    def hasAceWhenHandDoes(self):
        hand = Hand()
        hand.addCard(1, 2)
        hand.addCard(1, 0)
        hand.addCard(1, 3)
        self.assertTrue(hand.hasAce())        
        
    def hasAceWhenHandDoesNot(self):
        hand = Hand()
        hand.addCard(1, 1)        
        hand.addCard(1, 2)        
        hand.addCard(1, 3)
        self.assertFalse(hand.hasAce())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
