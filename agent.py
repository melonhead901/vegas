
class Agent:
    """
    An agent is a player in the game of Blackjack
    such as a human player, a dealer (who follows
    a set of hard-coded rules), or an AI-based player.
    """
    def getNextAction(self, gameState, hand):
        """
        Get the next action for the given gameState
        and hand. The provided gameState contains all
        of the hands of players participating in the
        round. The returned action must be one of those
        defined in the Actions class (see actions.py)
        and must be valid for the agent's hand.
        """
        return NotImplemented

    def lose(self, gameState, hand):
        """
        Notify this agent of a loss for the purpose
        of record-keeping.
        """

    def win(self, gameState, hand):
        """
        Notify this agent of a win for the purpose
        of record-keeping.
        """

    def tie(self, gameState, hand):
        """
        Notify this agent of a tie for the purpose
        of record-keeping.
        """
