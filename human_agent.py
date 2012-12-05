
from actions import Actions
from agent import Agent

class HumanAgent(Agent):
    # Keep a count of how many human players there
    # are for the purpose of identifying them.
    playerCount = 0

    def __init__(self):
        self.playerIndex = HumanAgent.playerCount
        HumanAgent.playerCount += 1

    def getNextAction(self, gameState, hand):
        print "Player {0} has hand {1}".format(
            self.playerIndex, hand)
        otherHands = [h
                      for h
                      in gameState.getPlayerHands().keys()
                      if h is not hand]
        if otherHands:
          print "Other hands visible: {0}".format(otherHands)
        print "Dealer showing: {0}".format(
            gameState.getDealerHand().getUpCard())
        while True:
            response = raw_input("== What will player {0} do {1}? ".format(
                    self.playerIndex,
                    "(H)it/(S)tand/S(p)lit/(D)ouble down")).lower()
            if response.lower() == "h":
                return Actions.HIT
            elif response.lower() == "s":
                return Actions.STAND
            elif response.lower() == "p":
                return Actions.SPLIT
            elif response.lower() == "d":
                return Actions.DOUBLE_DOWN

    def lose(self, gameState, hand):
        print "Player {0}'s hand of {1} lost to the dealer's " \
            "hand of {2}".format(self.playerIndex, hand, gameState.getDealerHand())

    def win(self, gameState, hand):
        print "Player {0}'s hand of {1} won to the dealer's " \
            "hand of {2}".format(self.playerIndex, hand, gameState.getDealerHand())

    def tie(self, gameState, hand):
        print "Player {0}'s hand of {1} tied with the dealer's " \
            "hand of {2}".format(self.playerIndex, hand, gameState.getDealerHand())

    def __str__(self):
        return "Human agent"
