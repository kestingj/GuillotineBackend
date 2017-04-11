from GameState import *
import logging


class GameManager:

    def __init__(self):
        self.games = {}

    def addGame(self, gameState):
        if gameState.getId() in self.games:
            logging.warning('Game with id: ' + gameState.getId() + ' already exists')
            return false
        self.games[gameState.getId()] = gameState
        logging.info('Added game with id: ' + gameState.getId())
        return true

    def deleteGame(self, gameId):
        if not self.gameIdExists(gameId):
            return false
        if gameState.getId() in self.games:
            del self.games[gameId]
            logging.info('Deleted game with id: ' + gameState.getId())
            return true
        logging.warning('No game with id: ' + gameState.getId() + ' exists')
        return false

    def playHand(self, gameId, playerId, hand):
        if not self.gameIdExists(gameId):
            return false
        gameState = self.games[gameId]
        if gameState.playHand(playerId, hand):
            nextPlayerId = gameState.nextPlayerId(playerId)
            playerState = gameState.getPlayerState(nextPlayerId)
            previousPlays = gameState.getPreviousPlays()
            self.pushStateToPlayer(playerId, playerState, previousPlays)

    def gameIdExists(self, gameId):
        if gameState.getId() in self.games:
            return true
        else:
            logging.warning('No game with id: ' + gameState.getId() + ' exists')
            return false

    def getPlayerState(self, playerId, gameId):
        if not self.gameIdExists(gameId):
            return None
        gameState = self.games[gameId]
        return gameState.getPlayerState(playerId)


    def pushStateToPlayer(self, playerId, playerState, previousPlays):
        pass
        # use push notifications to push state to player
