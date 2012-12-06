from agent import Agent

class ValueIterationAgent(Agent):

    def __init__(self, iterations):
        self.mdp = BlackjackMDP()
        self.values = {}

        for iteration in range(0, iterations):
            next_values = {}
            states = mdp.getStates()
            for state in states:
                next_values[state] = max(
                    map(lambda action:
                        self.getQValue(state, action),
                        mdp.getPossibleActions(state)))
            self.values = next_values
            
    def getNextAction(self, gameState, hand):
        actions = hand.getPossibleActions()
        if len(actions) == 0:
            return None
        else:
            maxValue, maxActions = None, None
            for action in actions:
                value = self.getQValue(gameState, action)
                if value == maxValue:
                    maxActions.append(action)
                elif value > maxValue:
                    maxValue, maxActions = value, [action]
        return random.choice(maxActions)
