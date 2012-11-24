
from actions import Actions
from deck import Deck
from hand import Hand
from human_agent import HumanAgent

class Game:
    def __init__(self, dealerAgent, playerAgents):
        self.dealerAgent = dealerAgent
        self.playerAgents = playerAgents
        self.dealerHand = None
        # A map of hands to the players who control them.
        self.handPlayerMap = {}
        self.inactiveHandPlayerMap = {}
        self.deck = Deck(1, 4, 13)

    def executeGame(self, numRounds):
        for i in range(numRounds):
            print "Round {0}".format(i)
            self.executeRound()

    def executeRound(self):
        self.handPlayerMap = {}
        self.inactiveHandPlayerMap = {}
        self.deck.verifyFull()
        # Deal a hand to the dealer and to each player.
        self.dealerHand = Hand()
        # TODO(snowden): Should one of these cards be
        # visible to the player agents?
        self.dealerHand.addCard(self.deck.take())
        self.dealerHand.addCard(self.deck.take())
        self.dealerAgent.receiveHand(self.dealerHand)
        for playerAgent in self.playerAgents:
            playerHand = Hand()
            playerHand.addCard(self.deck.take())
            playerHand.addCard(self.deck.take())
            playerAgent.receiveHand(playerHand)
            self.handPlayerMap[playerHand] = playerAgent

        # While there are still hands in play, ask the
        # agent controlling the hand for the next action.
        while self.handPlayerMap:
            # It isn't possible to modify the keys of the existing
            # map, so we have to create a new one each iteration.
            newHandPlayerMap = {}
            for (hand, playerAgent) in self.handPlayerMap.items():
                # TODO(snowden): Build a list that includes hands
                # updated during previous iterations of this loop.
                handList = (self.handPlayerMap.keys() +
                            self.inactiveHandPlayerMap.keys())
                action = playerAgent.getNextAction(
                    hand, handList)
                if action == Actions.STAND:
                    # If the action is to stand, remove the hand from
                    # the map of active hands and add it to the map
                    # of inactive hands.
                    self.inactiveHandPlayerMap[hand] = playerAgent
                elif action == Actions.HIT:
                    card = self.deck.take()
                    hand.addCard(card)
                    playerAgent.receiveCard(hand, card)
                    if hand.isBust():
                        self.inactiveHandPlayerMap[hand] = playerAgent
                    else:
                        newHandPlayerMap[hand] = playerAgent
                else:
                    raise ValueError("Not yet implemented.")
            self.handPlayerMap = newHandPlayerMap

        # All agents have either indicated that they want to
        # stand or else have busted, so it is the dealer's
        # turn to act.
        while True:
            # The dealer is not permitted to act on the cards
            # that players have been dealt.
            dealerAction = self.dealerAgent.getNextAction(
                self.dealerHand, [])
            if dealerAction == Actions.STAND:
                break
            elif dealerAction == Actions.HIT:
                card = self.deck.take()
                self.dealerHand.addCard(card)
                self.dealerAgent.receiveCard(self.dealerHand, card)
                if self.dealerHand.isBust():
                    break

        # The dealer has finished executing its actions. Compare
        # the dealer's hands with those of the players to determine
        # winners and losers.
        for (hand, playerAgent) in self.inactiveHandPlayerMap.items():
            # The dealer wins in the case of ties.
            if hand.compare(self.dealerHand) <= 0:
                playerAgent.lose(hand, self.dealerHand)
            else:
                playerAgent.win(hand, self.dealerHand)
            # Return the cards in the hand to the deck.
            for card in hand.getCards():
                self.deck.give(card)
        # Return the dealer's cards to the deck.
        for card in self.dealerHand.getCards():
            self.deck.give(card)
        # The deck should have all of the cards back.
        self.deck.verifyFull()

if __name__ == '__main__':
    # TODO(snowden): Make it possible to specify agents
    # via command-line arguments.
    dealerAgent = HumanAgent()
    playerAgents = [HumanAgent()]
    game = Game(dealerAgent, playerAgents)
    game.executeGame(2)
