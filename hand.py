from card import Card

"""
Hand represents a collection of Cards a player may have in a particular round.
"""
class Hand:    
    # Valid hand can have at most 21
    HAND_MAX = 21    
    
    """
    Create a new empty hand
    """
    def __init__(self):
        # list of cards in the hand
        self.cards = []
        
        # the hard count of the hand
        self.count = 0
        
        # whether this hand has an ace
        self.hasAce = False
        
    # Add the given card to the hand
    def addCard(self, card):
        self.cards.append(card)
        self.count += card.getCount()
        if card.value is Card.ACE_VALUE:
            self.hasAce = True
        
    # The count of the hand -- treating first ace as 11 if necessary
    def getSoftCount(self):
        return self.count + (10 if self.hasAce else 0)
        
    # The count of the hand -- treating first ace as 1 if necessary
    def getHardCount(self):
        return self.count
        
    # True if the count is always over 21, false otherwise
    def isBust(self):
        return self.getSoftCount() > Hand.HAND_MAX and self.getHardCount() > Hand.HAND_MAX
    
    # highest valid count if any, else 0
    def getValidCount(self):
        # Soft count will be higher if it's valid
        if self.getSoftCount() <= Hand.HAND_MAX:
            return self.getSoftCount()
        if self.getHardCount() <= Hand.HAND_MAX:
            return self.getHardCount()
        else:
            return 0
      
    # A blackjack is when the total is 21 after just 2 cards  
    def isBlackJack(self):
        return self.getValidCount() is 21 and len(self.cards) is 2
            