from actions import Actions
from agent import Agent

class StandingAgent(Agent):
    def getNextAction(self, gameState):
        return Actions.STAND
