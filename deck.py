import random

class Deck:
    """
    A Deck represents some number of sets of (suit, value)
    cards. It supports the take() function, which removes
    a card from the active pile of cards and transfers
    ownership of it to the caller, and the give() function,
    which transfers ownership of a card back to the deck.
    Once a card has been give()n to the deck, it becomes
    inactive and will not be returned by take().

    Inactive cards will be shuffled and made active
    automatically when there are no more cards in the
    active pile. Alternatively, the shuffle() function
    will merge all inactive cards with the active cards
    and randomize their positions.
    """
    def __init__(self, sets, suits, values):
        """
        Create a new deck with the given number of sets
        of cards of the given number of suits and values.
        The deck is shuffled after initialization.
        """
        if sets < 1:
            raise ValueError(
                "The number of sets must be at least " \
                    "{0}".format(sets))
        if suits < 1:
            raise ValueError(
                "The number of suits must be at least " \
                    "{0}".format(suits))
        if values < 1:
            raise ValueError(
                "The number of sets must be at least " \
                    "{0}".format(values))
        self.sets = sets
        self.suits = suits
        self.values = values
        self.activePile = []
        for suit in range(self.suits):
            for value in range(self.values):
                for i in range(self.sets):
                    self.activePile.append((suit, value))
        self.inactivePile = []
        self.shuffle()

    def numSets(self):
        """
        The number of sets of cards in this deck,
        as in how many copies of each value of each
        suit there are.
        """
        return self.sets

    def numSuits(self):
        """
        The number of suits in this deck.
        """
        return self.suits

    def numValues(self):
        """
        The number of values in this deck.
        """
        return self.values

    def numCards(self):
        """
        The total number of cards in this deck. This
        is independent of whether any cards have been
        take()n.
        """
        return self.numUniqueCards() * self.numSets()

    def numUniqueCards(self):
        """
        The number of unique cards in this deck. With
        4 suits and 13 values, for instance, there are
        52 unique cards. This is independent of whether
        or not any cards have been take()n.
        """
        return self.numSuits() * self.numValues()

    def numActiveCards(self):
        """
        The number of active cards in the deck. Active
        cards are those ready to be returned by an
        invocation of take().
        """
        return len(self.activePile)

    def numInactiveCards(self):
        """
        The number of inactive cards in the deck.
        Inactive cards are those that have been take()n
        and then give()n back to the deck.
        """
        return len(self.inactivePile)

    def take(self):
        """
        Get the next card from the deck. The caller
        takes ownership of the returned (suit, value)
        card and must later return it with take(). If
        the deck contains any active cards, the top
        card is returned, and otherwise the pile of
        inactive cards is shuffled and made active
        before returning the top card from that pile.

        It is an error to invoke take() when there are
        no active or inactive cards in the deck.
        """
        if not self.activePile:
            if not self.inactivePile:
                raise ValueError("No cards remain in the deck")
            self.shuffle()
        return self.activePile.pop()

    def give(self, card):
        """
        Return the given card to the pile of inactive
        cards.
        """
        self.inactivePile.append(card)

    def shuffle(self):
        """
        Combine the active and inactive decks and
        randomize their order.
        """
        self.activePile.extend(self.inactivePile)
        self.inactivePile = []
        random.shuffle(self.activePile)

    def verifyFull(self):
        """
        Verify that all cards are present in the deck.
        """
        combinedPile = self.activePile + self.inactivePile
        expectedCount = self.numUniqueCards() * self.numSets()
        if len(combinedPile) != expectedCount:
            raise ValueError(
                "Expected deck to contain {0} cards but it actually " \
                    "contains {1}".format(expectedCount, len(combinedPile)))
        cardCounts = {}
        for card in combinedPile:
            newCount = cardCounts.get(card, 0) + 1
            cardCounts[card] = newCount
            if newCount > self.numSets():
                raise ValueError(
                    "Expected at most {0} instances of card {1} but " \
                        "there are at least {2}".format(
                            self.numSets(), card, newCount))
