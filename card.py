

class Card:    
    # Cards are 0-indexed so the ace's value is 0
    ACE_VALUE = 0    
    
    """
    A card represents a suit, value pair. Card suits
    are 0-based and are ordered as Clubs, Diamonds,
    Spades, Hearts. Card values are also 0-based, and
    a value of 0 corresponds to an ace, while a value
    of 12 corresponds to a king. Suits and values must
    be non-negative integers, but no enforcement on
    them is made aside from that. Face cards, which
    have a count of 10, are considered to be all cards
    from ten onward.
    """
    def __init__(self, suit, value):
        if suit < 0:
            raise ValueError("Suit must be a non-negative integer " \
                                 "but was {0}".format(suit))
        if value < 0:
            raise ValueError("Value must be a non-negative integer " \
                                 "but was {0}".format(value))
        self.suit = suit
        self.value = value

    def getCount(self):
        """
        The count of a card is simply its 1-based value
        for ace through ten and is 10 for the jack and
        higher.
        """
        if self.value < 10:
            return self.value + 1
        else:
            return 10

    def getSoftCount(self):
        """
        The soft count for a card is the same as its
        count except for the ace, in which case the
        soft count is 11.
        """
        if self.value == 0:
            return 11
        else:
            return self.getCount()

    def __eq__(self, other):
        return (self.suit, self.value) == (other.suit, other.value)

    def __hash__(self):
        return hash((self.suit, self.value))

    def __str__(self):
        return "{1} of {0}".format(self.suitString(),
                                   self.valueString())

    def suitString(self):
        if self.suit == 0:
            return "Clubs"
        elif self.suit == 1:
            return "Diamonds"
        elif self.suit == 2:
            return "Spades"
        elif self.suit == 3:
            return "Hearts"
        else:
            return "Suit {0}".format(self.suit)

    def valueString(self):
        if self.value == 0:
            return "Ace"
        elif self.value == 10:
            return "Jack"
        elif self.value == 11:
            return "Queen"
        elif self.value == 12:
            return "King"
        else:
            return "{0}".format(self.value + 1)
