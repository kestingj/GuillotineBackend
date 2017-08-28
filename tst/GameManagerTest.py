import unittest
from GameManager import *
from mock import MagicMock
from mock import patch

class GameStateTest(unittest.TestCase):

    playerIds = ["Joseph", "Peter", "Nick", "Micha"]

    def setUp(self):
        self.gameManager = GameManager()

    def testCreateNewGame(self):
        gameId = self.gameManager.createNewGame(self.playerIds, self.playerIds[0])
        self.assertTrue(self.gameManager.gameIdExists(gameId))

    def testAddGame(self):
        gameState = GameState(self.playerIds, self.playerIds[0])
        self.gameManager.addGame(gameState)
        self.assertEqual(self.gameManager.games[gameState.gameId], gameState)

    def testDeleteGame(self):
        gameState = GameState(self.playerIds, self.playerIds[0])
        # Before game state has been added
        self.assertFalse(self.gameManager.deleteGame(gameState.gameId))

        self.gameManager.addGame(gameState)
        self.assertTrue(self.gameManager.deleteGame(gameState.gameId))
        self.assertFalse(self.gameManager.gameIdExists(gameState.gameId))

    def testGameIdExists(self):
        gameState = GameState(self.playerIds, self.playerIds[0])
        # Before game state has been added
        self.assertFalse(self.gameManager.gameIdExists(gameState.gameId))

        self.gameManager.addGame(gameState)

        self.assertTrue(self.gameManager.gameIdExists(gameState.gameId))

    def testGetPlayerState(self):
        playerId = self.playerIds[0]
        gameState = GameState(self.playerIds, playerId)
        # Before game state has been added
        self.assertEqual(self.gameManager.getPlayerState(gameState.gameId, playerId), None)

        mockedPlayerState = PlayerState(playerId, [], {}, [], self.playerIds[1])
        gameState.getPlayerState = MagicMock(return_value=mockedPlayerState)
        self.gameManager.addGame(gameState)

        playerState = self.gameManager.getPlayerState(gameState.gameId, playerId)
        self.assertEqual(playerState, mockedPlayerState)

    @patch.object(GameState, 'play')
    def testPlayHand(self, mockPlay):
        playerId = self.playerIds[0]
        gameState = GameState(self.playerIds, playerId)
        # Before game state has been added
        self.assertFalse(self.gameManager.playHand(gameState.gameId, playerId, []))

        self.gameManager.addGame(gameState)
        gameState.play = mockPlay

        self.assertTrue(self.gameManager.playHand(gameState.gameId, playerId, []))
        mockPlay.assert_called()

if __name__ == '__main__':
    unittest.main()