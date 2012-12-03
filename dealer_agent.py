
from agent import Agent
from actions import Actions
"""
Hand for the dealer, which has no choices.

Most casinos play dealer must stand on soft 17 and anything below.
Sometimes the delaer must hit on soft 17. To make this change in the
code change the check to be ... softCount() <= 17 instead of < 17.
"""
class DealerAgent(Agent):
    def getNextAction(self, _, hand):
      if ((hand.getSoftCount() > 21 and hand.getHardCount() < 17)
          or hand.getSoftCount() < 17):
        return Actions.HIT
      else:
        return Actions.STAND

    def __str__(self):
        return "Dealer agent"
