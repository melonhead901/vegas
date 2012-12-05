from actions import Actions
from agent import Agent

class StandingAgent(Agent):
    def getNextAction(self, gameState, hand):
        return Actions.STAND

    def __str__(self):
        return "Standing agent"
