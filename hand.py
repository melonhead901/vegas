from card import Card

class Hand:
    """
    Hand represents a collection of Cards a player
    may have in a particular round.
    """
    # Valid hand can have at most 21
    HAND_MAX = 21    

    def __init__(self):
        """
        Create a new empty hand.
        """
        # List of cards in the hand
        self.cards = []
        # The hard count of the hand
        self.count = 0
        # Whether this hand has an ace
        self.hasAce = False

    def addCard(self, card):
        """
        Add the given card to the hand.
        """
        self.cards.append(card)
        self.count += card.getCount()
        if card.value is Card.ACE_VALUE:
            self.hasAce = True

    def getCards(self):
        """
        Get a list of the cards in this hand.
        """
        return self.cards

    def getSoftCount(self):
        """
        The count of the hand, treating first ace
        as 11 if necessary.
        """
        return self.count + (10 if self.hasAce else 0)

    def getHardCount(self):
        """
        The count of the hand, treating first ace
        as 1 if necessary.
        """
        return self.count

    def isBust(self):
        """
        True if the count is always over 21, false otherwise.
        """
        return (self.getSoftCount() > Hand.HAND_MAX and
                self.getHardCount() > Hand.HAND_MAX)

    def getValidCount(self):
        """
        Highest valid count, if any, else 0.
        """
        # Soft count will be higher if it's valid
        if self.getSoftCount() <= Hand.HAND_MAX:
            return self.getSoftCount()
        if self.getHardCount() <= Hand.HAND_MAX:
            return self.getHardCount()
        else:
            return 0

    def isBlackJack(self):
        """
        A hand is a blackjack if the total is 21 after just 2 cards.
        """
        return self.getValidCount() == 21 and len(self.cards) == 2

    def compare(self, other):
        """
        Compare this hand to the given other hand. Returns
        < 0 if this hand is less than the given hand, > 0
        if greater, and 0 if they have the same value.
        """
        difference = self.getValidCount() - other.getValidCount()
        if difference != 0:
            return difference
        if self.isBlackJack() != other.isBlackJack():
            return 1 if self.isBlackJack() else -1
        return 0

    def __eq__(self, other):
        """
        Equality of hands is tricky. Currently this is
        defined as one hand equaling another iff they
        contain the same cards received in the same order,
        although it should maybe be order-insensitive.
        """
        return self.cards == other.cards

    def __hash__(self):
        return hash((len(self.cards), self.count, self.hasAce))

    def __str__(self):
        return "{0} with soft count {1} and hard count {2}{3}".format(
            self.cards, self.getSoftCount(), self.getHardCount(),
            " (BlackJack)" if self.isBlackJack() else (
                " (Bust)" if self.isBust() else ""))

    __repr__ = __str__
