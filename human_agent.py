
from actions import Actions
from agent import Agent

class HumanAgent(Agent):
    # Keep a count of how many human players there
    # are for the purpose of identifying them.
    playerCount = 0

    def __init__(self):
        self.playerIndex = HumanAgent.playerCount
        HumanAgent.playerCount += 1

    def receiveHand(self, hand):
        print "Player {0} was dealt {1}".format(
            self.playerIndex, hand)

    def receiveCard(self, hand, card):
        print "Player {0} received card {1}".format(
            self.playerIndex, card)

    def getNextAction(self, hand, handList):
        print "Player {0} has hand {1}".format(
            self.playerIndex, hand)
        print "Other hands visible: {0}".format(handList)
        while True:
            response = raw_input("What will player {0} do {1}? ".format(
                    self.playerIndex,
                    "(H)it/(S)tand")).lower()
            if response == "h":
                return Actions.HIT
            elif response == "s":
                return Actions.STAND

    def lose(self, hand, dealerHand):
        print "Player {0}'s hand of {1} lost to the dealer's " \
            "hand of {2}".format(self.playerIndex, hand, dealerHand)

    def win(self, hand, dealerHand):
        print "Player {0}'s hand of {1} won to the dealer's " \
            "hand of {2}".format(self.playerIndex, hand, dealerHand)
