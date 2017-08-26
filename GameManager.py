from GameState import *
import logging

# A GameManager manages all games for a single host. The server routes all calls to the game manager
class GameManager:

    def __init__(self):
        self.games = {}

    def createNewGame(self, playerIds, playerToGoFirst):
        gameState = GameState(playerIds, playerToGoFirst)
        self.addGame(gameState)
        return gameState.gameId

    def addGame(self, gameState):
        if gameState.getId() in self.games:
            logging.warning('Game with id: ' + gameState.getId() + ' already exists')
            return False
        self.games[gameState.getId()] = gameState
        logging.info('Added game with id: ' + str(gameState.getId()))
        return True

    def deleteGame(self, gameId):
        if self.gameIdExists(gameId):
            del self.games[gameId]
            logging.info('Deleted game with id: ' + str(gameId))
            return True
        else:
            return False

    def playHand(self, gameId, playerId, hand):
        if not self.gameIdExists(gameId):
            return False
        gameState = self.games[gameId]
        gameState.play(playerId, hand)
            # nextPlayerId = gameState.nextPlayerId(playerId)
            # playerState = gameState.getPlayerState(nextPlayerId)
            # self.pushStateToPlayer(playerId, playerState)
        return True

    def gameIdExists(self, gameId):
        if gameId in self.games:
            return True
        else:
            logging.warning('No game with id: ' + str(gameId) + ' exists')
            return False

    def getPlayerState(self, playerId, gameId):
        if not self.gameIdExists(gameId):
            return None
        gameState = self.games[gameId]
        return gameState.getPlayerState(playerId)

    def checkpointState(self):
        pass
        # Checkpoint game state to DDB

    def pushStateToPlayer(self, playerId, playerState):
        pass
        # use push notifications to push state to player
