
from Card import Card
from random import shuffle
from PlayerState import PlayerState
import uuid

# A GameState tracks all state for a single game. This state includes:
# ID for the game
# Players in the game
# Hands for each player
# History of plays made so far in the game
# Players that have already finished the game
class GameState:
    def __init__(self, playerIds, playerToGoFirst):
        if playerToGoFirst not in playerIds:
            raise ValueError("Player to go first: " + playerToGoFirst + " not found in playerIds: " + str(playerIds))
        hands = getRandomHands(len(playerIds))
        playerHands = {}
        for i in xrange(0, len(playerIds)):
            playerHands[playerIds[i]] = hands[i]
        self.playerCount = len(playerIds)
        self.playerHands = playerHands
        self.previousPlays = []  # Track the entire game's play history
        self.gameId = uuid.uuid4()
        self.playerIds = playerIds
        self.turn = playerToGoFirst
        self.finishedPlayers = []

    # Throws if playerId does not equal turn or if play is not a subset of playerId's current hand
    def play(self, playerId, play):
        if playerId != self.turn:
            raise ValueError("It is " + self.turn +"'s, not " + playerId + "'s, turn")
        existingHand = self.playerHands[playerId]
        if not (play.issubset(existingHand)):
            raise ValueError("play: " + str(play) + " is not a subset of existing hand " + str(existingHand) + " for player " + playerId)
        self.playerHands[playerId] = existingHand - play
        if len(self.playerHands[playerId]) == 0:
            self.finishedPlayers.append(playerId)
        self.previousPlays.append((playerId, play))
        self.turn = self.getNextPlayer(playerId)

    def getPlayerState(self, playerId):
        return PlayerState(playerId, self.playerHands[playerId], self.getPlayersIds(), self.getPreviousPlays(), self.getTurn())

    def getTurn(self):
        return self.turn

    def getPreviousPlays(self):
        return self.previousPlays

    def clearPreviousPlays(self):
        self.previousPlays = []

    def getId(self):
        return self.gameId

    def getPlayersIds(self):
        return self.playerIds

    def getFinishedPlayers(self):
        return self.finishedPlayers

    # Game is finished when all but one player has finished
    def isGameFinished(self):
        return len(self.finishedPlayers) == len(self.playerIds) - 1

    def getNextPlayer(self, currentPlayerId):

        index = self.playerIds.index(currentPlayerId)

        while(True):
            index += 1
            if index >= len(self.playerIds):
                index = 0
            if self.playerIds[index] not in self.finishedPlayers:
                break

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
