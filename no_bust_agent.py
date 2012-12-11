from actions import Actions
from agent import Agent

class NoBustAgent(Agent):
    def getNextAction(self, _, hand):
        if hand.getHardCount() <= 11:
            return Actions.HIT
        else:
            return Actions.STAND

    def __str__(self):
        return "Standing agent"
