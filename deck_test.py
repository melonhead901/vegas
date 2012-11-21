import random
import unittest

from card import Card
from deck import Deck

class DeckTest(unittest.TestCase):
    def genericDeckTest(self, sets, suits, values):
        """
        Test taking cards from and giving cards to a deck
        with the specified number of sets, suits, and values.
        Does not exercise Deck.shuffle().
        """
        deck = Deck(sets, suits, values)
        self.assertEqual(sets, deck.numSets())
        self.assertEqual(suits, deck.numSuits())
        self.assertEqual(values, deck.numValues())
        self.assertEqual(sets * suits * values, deck.numCards())
        self.assertEqual(suits * values, deck.numUniqueCards())
        self.assertEqual(sets * suits * values, deck.numActiveCards())
        self.assertEqual(0, deck.numInactiveCards())
        deck.verifyFull()
        cardCounts = {}
        for i in range(deck.numCards()):
            self.assertEqual(deck.numCards() - i, deck.numActiveCards())
            self.assertEqual(i, deck.numInactiveCards())
            card = deck.take()
            cardCounts[card] = cardCounts.get(card, 0) + 1
            deck.give(card)
        deck.verifyFull()
        for (_, count) in cardCounts.items():
            self.assertEqual(deck.numSets(), count)

    def test_singleSet(self):
        self.genericDeckTest(1, 1, 1)
        self.genericDeckTest(1, 4, 1)
        self.genericDeckTest(1, 1, 13)
        self.genericDeckTest(1, 4, 13)

    def test_doubleSet(self):
        self.genericDeckTest(2, 1, 1)
        self.genericDeckTest(2, 4, 1)
        self.genericDeckTest(2, 1, 13)
        self.genericDeckTest(2, 4, 13)

    def test_shuffle(self):
        deck = Deck(1, 1, 2)
        card1 = deck.take()
        card2 = deck.take()
        self.assertNotEqual(card1, card2)
        deck.give(card1)
        deck.give(card2)
        deck.verifyFull()

        # The deck should be shuffled on this call.
        card3 = deck.take()
        self.assertTrue(card3 == card1 or card3 == card2)
        card4 = deck.take()
        self.assertTrue(card4 == card1 or card4 == card2)
        self.assertNotEqual(card3, card4)

        # Try shuffling with various numbers of cards.
        deck.shuffle()
        deck.give(card3)
        deck.shuffle()
        deck.give(card4)
        deck.verifyFull()
        deck.shuffle()
        deck.verifyFull()
        card3 = deck.take()
        self.assertTrue(card3 == card1 or card3 == card2)
        card4 = deck.take()
        self.assertTrue(card4 == card1 or card4 == card2)
        self.assertNotEqual(card3, card4)

    def test_errorCases(self):
        self.assertRaises(ValueError, Deck, 0, 1, 1)
        self.assertRaises(ValueError, Deck, 1, 0, 1)
        self.assertRaises(ValueError, Deck, 1, 1, 0)

        # Try taking from an empty deck.
        deck = Deck(1, 1, 1)
        deck.take()
        self.assertRaises(ValueError, deck.take)

        # Try verifying that the deck is full when it is not.
        deck = Deck(1, 1, 2)
        card = deck.take()
        deck.give(card)
        deck.verifyFull()
        card = deck.take()
        self.assertRaises(ValueError, deck.verifyFull)

        # Try verifying that the deck is full when an invalid
        # card has been added.
        deck = Deck(1, 1, 1)
        deck.give(Card(5, 10))
        self.assertRaises(ValueError, deck.verifyFull)

if __name__ == '__main__':
    random.seed(287984925002)
    unittest.main()
