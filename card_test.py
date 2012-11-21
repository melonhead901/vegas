import unittest

from card import Card

class CardTest(unittest.TestCase):
    def test_count(self):
        for value in range(10):
            self.assertEqual(value + 1, Card(0, value).getCount())
        for value in range(10, 13):
            self.assertEqual(10, Card(0, value).getCount())

    def test_softCount(self):
        # All soft counts should be the same except
        # for the ace, which has a soft value of 11.
        self.assertEqual(11, Card(0, 0).getSoftCount())
        for value in range(1, 13):
            self.assertEqual(Card(0, value).getCount(),
                             Card(0, value).getSoftCount())

    def test_equalityAndHash(self):
        for suit in range(3):
            for value in range(12):
                card1 = Card(suit, value)
                card2 = Card(suit, value)
                card3 = Card(suit + 1, value)
                card4 = Card(suit, value + 1)
                self.assertEqual(card1, card2)
                self.assertEqual(hash(card1), hash(card2))
                self.assertNotEqual(card1, card3)
                self.assertNotEqual(card1, card4)
                self.assertNotEqual(hash(card1), hash(card3))
                self.assertNotEqual(hash(card1), hash(card4))

    def test_stringRepresentations(self):
        aceOfClubs = Card(0, 0)
        self.assertEqual("Clubs", aceOfClubs.suitString())
        self.assertEqual("Ace", aceOfClubs.valueString())
        self.assertEqual("Ace of Clubs", str(aceOfClubs))
        nineOfDiamonds = Card(1, 8)
        self.assertEqual("Diamonds", nineOfDiamonds.suitString())
        self.assertEqual("9", nineOfDiamonds.valueString())
        self.assertEqual("9 of Diamonds", str(nineOfDiamonds))
        queenOfSpades = Card(2, 11)
        self.assertEqual("Spades", queenOfSpades.suitString())
        self.assertEqual("Queen", queenOfSpades.valueString())
        self.assertEqual("Queen of Spades", str(queenOfSpades))
        jackOfHearts = Card(3, 10)
        self.assertEqual("Hearts", jackOfHearts.suitString())
        self.assertEqual("Jack", jackOfHearts.valueString())
        self.assertEqual("Jack of Hearts", str(jackOfHearts))
        kingOfSuit4 = Card(4, 12)
        self.assertEqual("Suit 4", kingOfSuit4.suitString())
        self.assertEqual("King", kingOfSuit4.valueString())
        self.assertEqual("King of Suit 4", str(kingOfSuit4))

    def test_errorCases(self):
        self.assertRaises(ValueError, Card, -1, 0)
        self.assertRaises(ValueError, Card, 0, -1)

if __name__ == '__main__':
    unittest.main()
