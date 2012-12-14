#!/usr/bin/python

import argparse
import random
import sys

from actions import Actions
from deck import Deck
from hand import Hand
from human_agent import HumanAgent
from dealer_agent import DealerAgent
from game_state import GameState
from no_bust_agent import NoBustAgent
from q_learning_agent import QLearningAgent
from reflex_agent import ReflexAgent
from standing_agent import StandingAgent
from value_iteration_agent import ValueIterationAgent
from card import Card

class Game:
    def __init__(self, dealerAgent, playerAgents):
        self.dealerAgent = dealerAgent
        self.playerAgents = playerAgents

        # maps of Agent => int
        self.losses = {}
        self.wins = {}
        self.ties = {}
        self.balances = {}
        for playerAgent in playerAgents:
          self.losses[playerAgent] = self.wins[playerAgent] = \
              self.ties[playerAgent] = self.balances[playerAgent] = 0

    def executeGame(self, numRounds):
        for _ in range(numRounds):
            # print "Round {0}".format(i)
            self.executeRound()

    def executeRound(self):
        # A map of hands to the players who control them.
        handPlayerMap = {}
        inactiveHandPlayerMap = {}
        deck = Deck(1, 4, 13)

        # Deal cards to the dealer. The dealer has a bet of 0.
        dealerHand = Hand(0)
        dealerHand.addCard(deck.take())
        dealerHand.addCard(deck.take())
        for playerAgent in self.playerAgents:
            # TODO(snowden): Allow players to choose how much
            # they bet each time.
            playerHand = Hand(1)
            playerHand.addCard(deck.take())
            playerHand.addCard(deck.take())
            handPlayerMap[playerHand] = playerAgent

        # While there are still hands in play, ask the
        # agent controlling the hand for the next action.
        while handPlayerMap:
            # It isn't possible to modify the keys of the existing
            # map, so we have to create a new one each iteration.
            newHandPlayerMap = {}
            remainingHandPlayerMap = handPlayerMap
            for (hand, playerAgent) in handPlayerMap.items():
                currentHandPlayerMap = dict(newHandPlayerMap.items() +
                                            remainingHandPlayerMap.items())
                del remainingHandPlayerMap[hand]
                action = playerAgent.getNextAction(
                    GameState(currentHandPlayerMap,
                              dealerHand, deck), hand)
                if action == Actions.HIT:
                    hand.hit(deck)
                    if hand.isBust():
                        inactiveHandPlayerMap[hand] = playerAgent
                    else:
                        newHandPlayerMap[hand] = playerAgent
                elif action == Actions.STAND:
                    hand.stand(deck)
                    # If the action is to stand, remove the hand from
                    # the map of active hands and add it to the map
                    # of inactive hands.
                    inactiveHandPlayerMap[hand] = playerAgent
                elif action == Actions.SPLIT:
                    splitHands = hand.split(deck)
                    newHandPlayerMap[splitHands[0]] = playerAgent
                    newHandPlayerMap[splitHands[1]] = playerAgent
                elif action == Actions.DOUBLE_DOWN:
                    hand.doubleDown(deck)
                    # After doubling down, the player may take no
                    # further actions.
                    inactiveHandPlayerMap[hand] = playerAgent
                else:
                    raise ValueError("Not yet implemented.")
            handPlayerMap = newHandPlayerMap

        # All agents have either indicated that they want to
        # stand or else have busted, so it is the dealer's
        # turn to act.
        while True:
            # The dealer is not permitted to act on the cards
            # that players have been dealt and can only hit
            # or stand with each card received.
            dealerAction = self.dealerAgent.getNextAction(None, dealerHand)
            if dealerAction == Actions.STAND:
                break
            elif dealerAction == Actions.HIT:
                dealerHand.hit(deck)
                if dealerHand.isBust():
                    break

#       print
#       print "Dealer has: %s" % dealerHand.getValidCount()
#       print "Player has: %s" % map(Hand.getValidCount, inactiveHandPlayerMap.keys())

        # The dealer has finished executing its actions. Compare
        # the dealer's hands with those of the players to determine
        # winners and losers.
        endingState = GameState(handPlayerMap, dealerHand, deck)
        for (hand, playerAgent) in inactiveHandPlayerMap.items():
            result = self.determineWinner(hand, dealerHand)
#           print result
            if result < 0:
                playerAgent.lose(endingState, hand)
                self.losses[playerAgent] += 1
                self.balances[playerAgent] -= hand.getBet()
            elif result > 0:
                playerAgent.win(endingState, hand)
                self.wins[playerAgent] += 1
                self.balances[playerAgent] += hand.getBet() * 1.5 if hand.isBlackJack() else 1
            else: # result == 0
                playerAgent.tie(endingState, hand)
                self.ties[playerAgent] += 1
            # Return the cards in the hand to the deck.
            for card in hand.getCards():
                deck.give(card)
        # Return the dealer's cards to the deck.
        for card in dealerHand.getCards():
            deck.give(card)
        # The deck should have all of the cards back.
        deck.verifyFull()

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
        playerStrings = [
            "{0}: {1}-{2}-{3}. Ending balance: {4}".format(
                playerAgent, self.wins[playerAgent], self.losses[playerAgent],
                self.ties[playerAgent], self.balances[playerAgent]) for playerAgent in self.playerAgents]
        return '\n'.join(playerStrings)

# Print the name of the policy set and the header dealer cards
def printPolicyHeader(name):
    s = name + "\t"
    for i in range(2,12):
        s += "{0}\t".format(i)
    print s

def getColor(action):
    if action == 'S':
        return "\033[31m"
    elif action == 'D':
        return "\033[34m"
    else:
        return "\033[32m"
  
# Print the normal hand totals (no pairs/aces)
def printNoAcePairPolicy(agent):
    printPolicyHeader("sc")
    dummyHand = Hand(1)
    dummyHand.getPossibleActions = lambda: [Actions.HIT, Actions.STAND, Actions.DOUBLE_DOWN]

    for playerSoftCount in range(20,1,-1):
        printString = "{0}\t".format(playerSoftCount)
        for dealerSoftCard in range(2,12):
            # Construct features for this cell
            features = (playerSoftCount, False, dealerSoftCard)
            # print the action for that feature
            action = agent.getPolicy(features, dummyHand)[0]
            color = getColor(action)
            printString += '{0}{1}\t'.format(color, action)
#           key = (features, action)
#           if key in agent.q_values:
#               str += "%0.2f\t" % agent.q_values[key]
#           else:
#               str += '\t'
        print printString + "\033[1;37m"

def printAcePolicy(agent):
    printPolicyHeader("aces")
    for nonAceCard in range(10,1,-1):
        printString = "{0}\t".format(nonAceCard)
        for dealerSoftCard in range(2,12):
            dummyHand = Hand(1)
            dummyHand.addCard(Card(1, 0))
            dummyHand.addCard(Card(1, nonAceCard-1))
            # Construct features for this cell
            features = (nonAceCard+1, True, dealerSoftCard)
            # print the action for that features
            action = agent.getPolicy(features, dummyHand)[0]
            color = getColor(action)
            printString += '{0}{1}\t'.format(color, action)
#           key = (features, action)
#           if key in agent.q_values:
#               str += "%0.2f\t" % agent.q_values[key]
#           else:
#               str += '\t'
        print printString + "\033[1;37m"

def printPolicy(agent):
    printNoAcePairPolicy(agent)
    printAcePolicy(agent)
    print "\033[0m"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Play some games of Blackjack.")
    parser.add_argument("-t", "--trainingRounds", type=int, help="The number of training rounds to run.")
    parser.add_argument("-r", "--realRounds", type=int, help="The number of real rounds to run.")
    parser.add_argument("-s", "--randomSeed", type=int, help="The random seed to use.")
    parser.add_argument("-i", "--iterations", type=int, help="The number of iterations of value iteration to run.");
    parser.add_argument("-p", "--playerAgents", type=str, nargs="+", help="A list of player agents to use")

    args = parser.parse_args()
    trainingRounds = args.trainingRounds
    realRounds = args.realRounds
    randomSeed = args.randomSeed
    iterations = args.iterations
    if realRounds <= 0:
        print "Number of real rounds must be > 0 but was {0}".format(realRounds)
        sys.exit(1)

    if randomSeed:
        random.seed(randomSeed)

    playerAgentStrings = args.playerAgents

    playerAgents = []
    for playerAgentString in playerAgentStrings:
        if playerAgentString == "QLearningAgent":
            playerAgents.append(QLearningAgent())
        elif playerAgentString == "ReflexAgent":
            playerAgents.append(ReflexAgent())
        elif playerAgentString == "StandingAgent":
            playerAgents.append(StandingAgent())
        elif playerAgentString == "NoBustAgent":
            playerAgents.append(NoBustAgent())
        elif playerAgentString == "HumanAgent":
            playerAgents.append(HumanAgent())
        elif playerAgentString == "ValueIterationAgent":
            if not iterations:
                print "Number of iterations must be specified with ValueIterationAgent"
                sys.exit(1)
            playerAgents.append(ValueIterationAgent(iterations))
        else:
            print "Unrecognized agent {0}".format(playerAgentString)
            sys.exit(1)

    dealerAgent = DealerAgent()

    if trainingRounds > 0:
        trainingAgents = filter(lambda x: isinstance(x, QLearningAgent), playerAgents)
        print "Training ({0} rounds)...".format(trainingRounds)
        game = Game(dealerAgent, trainingAgents)
        game.executeGame(trainingRounds)

    for playerAgent in playerAgents:
        if isinstance(playerAgent, QLearningAgent):
            playerAgent.epsilon = 0.0
            playerAgent.alpha = 0.0
            playerAgent.no_policy_moves_made = 0

    print "Testing ({0} rounds)...".format(realRounds)
    game = Game(dealerAgent, playerAgents)
    game.executeGame(realRounds)
    print game.resultString()
    for (playerAgentString, playerAgent) in zip(playerAgentStrings, playerAgents):
        if isinstance(playerAgent, QLearningAgent):
            print "{0} policies:".format(playerAgentString)
            printPolicy(playerAgent)
            
            print "states seen: {0}".format(len(playerAgent.states_seen))
            values = playerAgent.states_seen.values()
            freq = {}
            for value in values:
                freq[value] = freq.get(value, 0) + 1
            s, ss = '', 0
            freq_items = freq.items()
            freq_items.sort()
            for (times_seen, num_states) in freq_items:
                s += "%3u:%u\t" % (times_seen, num_states)
                ss += 1
                if ss > 7:
                    print s
                    s, ss = '', 0
            if ss != 0:
                print s
            print "{0} random moves made".format(playerAgent.no_policy_moves_made)
        elif isinstance(playerAgent, ValueIterationAgent):
            playerAgent.printPolicies()
