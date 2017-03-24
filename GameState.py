
from Card import Card
from random import shuffle
import uuid


class GameState:
    def __init__(self, playerIds):
        hands = getRandomHands(len(playerIds))
        gameState = {}
        for i in xrange(0, len(playerIds)):
            gameState[playerIds[i]] = hands[i]
        self.playerCount = len(playerIds)
        self.gameState = gameState
        self.previousPlays = []  # Track the entire game's play history
        self.id = uuid.uuid4()
        self.playerIds = playerIds

    # True if player can play the hand, False otherwise
    def playHand(self, playerId, hand):
        existingHand = self.gameState[playerId]
        print "HAND"
        print hand
        print existingHand
        if not (hand.issubset(existingHand)):
            print "Returned False"
            return False
        self.gameState[playerId] = existingHand - hand
        self.previousPlays.append((playerId, hand))
        print "Returned True"
        return True

    def getPlayerState(self, playerId):
        return self.gameState[playerId]

    def getPreviousPlays(self):
        return self.previousPlays

    def clearPreviousPlays(self):
        self.previousPlays = []

    def getId(self):
        return self.id

    def getPlayersIds(self):
        return self.playerIds

    def getNextPlayer(self, currentPlayerId):
        index = self.playerIds.index(currentPlayerId) + 1
        if index >= self.playerIds.count:
            index = 0
        return self.playerIds[index]




def getRandomHands(numberOfPlayers):
        cards = []
        for rank in xrange(2, 15):
            for suit in xrange(0, 4):
                cards.append(Card(rank, suit))
        shuffle(cards)
        hands = []
        for player in xrange(0, numberOfPlayers):
            hand = []
            for i in xrange(0, 13):
                hand.append(cards.pop())
            hands.append(set(hand))
        return hands
