
class Agent:
    """
    An agent is a player in the game of Blackjack
    such as a human player, a dealer (who follows
    a set of hard-coded rules), or an AI-based player.
    """
    def receiveHand(self, hand):
        """
        Receive a new hand, such as at the start of
        a round. The agent should not modify this hand.
        """

    def receiveCard(self, hand, card):
        """
        Receive a card for a particular hand held
        by this agent. The agent should not modify
        the hand or the card.
        """

    def getNextAction(self, gameState):
        """
        Get the next action for the given gameState. The
        provided gameState contains all of the hands
        of players participating in the round. The
        returned action must be one of those defined
        in the Actions class (see actions.py) and must
        be valid for the agent's hand.
        """
        return NotImplemented

    def lose(self, hand, dealerHand):
        """
        Notify this agent of a loss for the purpose
        of record-keeping.
        """

    def win(self, hand, dealerHand):
        """
        Notify this agent of a win for the purpose
        of record-keeping.
        """

    def tie(self, hand, dealerHand):
        """
        Notify this agent of a tie for the purpose
        of record-keeping.
        """
