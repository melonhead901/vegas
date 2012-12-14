from actions import Actions
from card import Card

class Hand:
    """
    Hand represents a collection of Cards a player
    may have in a particular round.
    """
    # Valid hand can have at most 21
    HAND_MAX = 21    

    def __init__(self, bet, isSplit=False):
        """
        Create a new empty hand.
        """
        if bet < 0:
            raise ValueError("Bet must be >= 0 but was {0}".format(bet))
        # The bet associated with the hand.
        self._bet = bet
        # Whether this hand is the result of a split.
        self._isSplit = isSplit
        # Whether an agent has doubled down on this hand.
        self._isDoubleDown = False
        # List of cards in the hand.
        self._cards = []
        # The hard count of the hand.
        self._count = 0
        # Whether this hand has an ace.
        self._hasAce = False        

    def addCard(self, card):
        """
        Add the given card to the hand.
        """
        self._cards.append(card)
        self._count += card.getCount()
        if card.value is Card.ACE_VALUE:
            self._hasAce = True

    def getCards(self):
        """
        Get a list of the cards in this hand.
        """
        return self._cards

    def getSoftCount(self):
        """
        The count of the hand, treating first ace
        as 11 if necessary.
        """
        return self._count + (10 if self._hasAce else 0)

    def getHardCount(self):
        """
        The count of the hand, treating first ace
        as 1 if necessary.
        """
        return self._count

    def getBet(self):
        """
        The bet associated with this hand.
        """
        return self._bet

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
        return self.getValidCount() == 21 and len(self._cards) == 2

    def getUpCard(self):
        """
        The card that would show if this is the dealer's hand.
        """
        if not self._cards:
            raise ValueError("There are no cards in this hand")
        return self._cards[0]

    def getPossibleActions(self):
        """
        Return a list of possible actions for this hand.
        """
        actions = []
        if self.canHit():
            actions.append(Actions.HIT)
        if self.canStand():
            actions.append(Actions.STAND)
        if self.canSplit():
            actions.append(Actions.SPLIT)
        if self.canDoubleDown():
            actions.append(Actions.DOUBLE_DOWN)
        return actions
        
    def isSplit(self):
        """
        Whether this hand is the result of a split.
        """
        return self._isSplit

    def isDoubleDown(self):
        """
        Whether an agent has doubled down on this hand.
        """
        return self._isDoubleDown

    def canHit(self):
        """
        Whether it is possible for an agent to hit on
        this hand. Hitting is allowed at any point up
        until the agent stays or doubles down, which
        is handled by the game logic.
        """
        return True

    def canStand(self):
        """
        Whether it is possible for an agent to stand
        on this hand. It is always possible to stand.
        """
        return True

    def canSplit(self):
        """
        Whether it is possible to split this hand. Splits are
        allowed if the hand is not itself a split, if it
        contains only two cards, if the counts of the cards
        match.
        """
        return not self._isSplit and len(self._cards) == 2 and \
            self._cards[0].getCount() == self._cards[1].getCount()

    def canDoubleDown(self):
        """
        Whether it is possible to double down on this hand.
        Doubling down is allowed only if the hand contains
        two cards. Doubling down after splitting is permitted.
        """
        return len(self._cards) == 2

    def hit(self, deck):
        """
        Hit on this hand, taking a card from the given deck.
        Prefer invoking hit over addCard, where appropriate,
        as this function checks that hitting is permitted first.
        """
        if not self.canHit():
            raise ValueError("Hitting on this hand is not allowed: {0}".format(self))
        self.addCard(deck.take())

    def stand(self, _):
        """
        Stand on this hand, committing to taking no further action.
        """
        if not self.canStand():
            raise ValueError("Standing on this hand is not allowed: {0}".format(self))

    def split(self, deck):
        """
        Split this hand into two distinct hands. This hand
        object is invalidated, and the two split hands are
        returned as a pair.
        """
        if not self.canSplit():
            raise ValueError("This hand cannot be split: {0}".format(self))
        splitHands = (Hand(self._bet, True), Hand(self._bet, True))
        splitHands[0].addCard(self._cards[0])
        splitHands[0].addCard(deck.take())
        splitHands[1].addCard(self._cards[1])
        splitHands[1].addCard(deck.take())
        return splitHands

    def doubleDown(self, deck):
        """
        Double down on this hand. After doubling down, the
        agent in control of the hand receives one additional
        card and then may take no further action.
        """
        if not self.canDoubleDown():
            raise ValueError("This hand cannot be doubled down: {0}".format(self))
        self._bet *= 2
        self.hit(deck)
        self._isDoubleDown = True

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

    def getHasAce(self):
        return self._hasAce

    def __hash__(self):
        return hash((len(self._cards), self._count, self._hasAce))

    def __str__(self):
        return "{0} with soft count {1} and hard count {2}{3}".format(
            self._cards, self.getSoftCount(), self.getHardCount(),
            " (BlackJack)" if self.isBlackJack() else (
                " (Bust)" if self.isBust() else ""))

    __repr__ = __str__
