#!/usr/bin/python
 
from actions import Actions
from deck import Deck
from hand import Hand
from human_agent import HumanAgent
from dealer_agent import DealerAgent
from game_state import GameState
from q_learning_agent import QLearningAgent
from reflex_agent import ReflexAgent
from standing_agent import StandingAgent

class Game:
    def __init__(self, dealerAgent, playerAgents):
        self.dealerAgent = dealerAgent
        self.playerAgents = playerAgents

        # maps of Agent => int
        self.loses = {}
        self.wins = {}
        self.ties = {}
        for playerAgent in playerAgents:
          self.loses[playerAgent] = self.wins[playerAgent] = self.ties[playerAgent] = 0

        self.dealerHand = None
        # A map of hands to the players who control them.
        self.handPlayerMap = {}
        self.inactiveHandPlayerMap = {}
        self.deck = Deck(1, 4, 13)
        # Initialize GameState
        self.gameState = GameState()
        self.gameState.setDeck(self.deck)
        self.gameState.setPlayerHands(self.handPlayerMap)

    def executeGame(self, numRounds):
        for i in range(numRounds):
            # print "Round {0}".format(i)
            self.executeRound()

    def executeRound(self):
        self.handPlayerMap = {}
        self.gameState.setPlayerHands(self.handPlayerMap)
        self.inactiveHandPlayerMap = {}
        self.deck.verifyFull()

        # Deal cards to the dealer
        self.dealerHand = Hand()
        self.gameState.setDealerHand(self.dealerHand)
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
                action = playerAgent.getNextAction(self.gameState)
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
            dealerAction = self.dealerAgent.getNextAction(self.gameState)
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
            result = self.determineWinner(hand, self.dealerHand)
            if result < 0:
                playerAgent.lose(self.gameState)
                self.loses[playerAgent] += 1
            elif result > 0:
                playerAgent.win(self.gameState)
                self.wins[playerAgent] += 1
            else: # result == 0
                playerAgent.tie(self.gameState)
                self.ties[playerAgent] += 1
            # Return the cards in the hand to the deck.
            for card in hand.getCards():
                self.deck.give(card)
        # Return the dealer's cards to the deck.
        for card in self.dealerHand.getCards():
            self.deck.give(card)
        # The deck should have all of the cards back.
        self.deck.verifyFull()
        
    # Returns less than 0 if the player loses, greater than 0 if he wins, and 0 for a push
    def determineWinner(self, playerHand, dealerHand):
        # Player loses if both player and dealer bust
        if playerHand.isBust():
            return -1
        # Player wins if both get black jack
        elif playerHand.isBlackJack():
            return 1
        else:
            return playerHand.compare(dealerHand)

    def resultString(self):
        playerStrings = ["%s: %u-%u-%u" % (playerAgent, self.wins[playerAgent], self.loses[playerAgent], self.ties[playerAgent]) for playerAgent in self.playerAgents]
        return '\n'.join(playerStrings)
    
    
def printPolicy(agent):
    str = "sc\t"
    for i in range(2,12):
        str += "{0}\t".format(i)
    print str
        
    for playerSoftCount in range(20,1,-1):    
        str = "{0}\t".format(playerSoftCount)    
        for dealerSoftCard in range(2,12):
            # Construct features for this cell
            feature = (((playerSoftCount, playerSoftCount),), dealerSoftCard)
            # print the action for that feature
            for action in [Actions.STAND]:
              key = (feature, action)
              action = agent.getPolicy(feature)[0]
              if action == 'S':
                  color = "\033[31m"
              else:
                  color = "\033[32m"
              str += '{0}{1}\t'.format(color, action)
#              if key in agent.q_values:
#                  str += "%0.2f\t" % agent.q_values[key]
#              else:
#                  str += '\t' 
        print str + "\033[1;37m"
        

if __name__ == '__main__':
    # TODO(snowden): Make it possible to specify agents
    # via command-line arguments.

    dealerAgent = DealerAgent()

    #playerAgents = [QLearningAgent()]
    playerAgents = [ReflexAgent()]
    #playerAgents = [StandingAgent()]

    print "Training..."
    game = Game(dealerAgent, playerAgents)
    game.executeGame(10000)

    playerAgents[0].epsilon = 0.0
    playerAgents[0].alpha = 0.0

    print "Testing..."
    game = Game(dealerAgent, playerAgents)
    game.executeGame(1000)
    print game.resultString()
    #printPolicy(playerAgents[0])
