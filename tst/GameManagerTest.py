import unittest
from GameManager import *
from mock import MagicMock
from mock import patch

class GameStateTest(unittest.TestCase):

    playerIds = ["Joseph", "Peter", "Nick", "Micha"]
    game_id ="gameId"

    def setUp(self):
        self.gameManager = GameManager()

    def testCreateNewGame(self):
        gameId = self.gameManager.create_new_game(self.playerIds, self.playerIds[0])
        self.assertTrue(self.gameManager.game_id_exists(gameId))

    def testAddGame(self):
        gameState = GameState(self.playerIds, self.playerIds[0])
        self.gameManager.__add_game__(gameState)
        self.assertEqual(self.gameManager.games[gameState.game_id], gameState)

    def testDeleteGame(self):
        gameState = GameState(self.playerIds, self.playerIds[0])
        # Before game state has been added
        self.assertFalse(self.gameManager.__delete_game__(gameState.game_id))

        self.gameManager.__add_game__(gameState)
        self.assertTrue(self.gameManager.__delete_game__(gameState.game_id))
        self.assertFalse(self.gameManager.game_id_exists(gameState.game_id))

    def testGameIdExists(self):
        gameState = GameState(self.playerIds, self.playerIds[0])
        # Before game state has been added
        self.assertFalse(self.gameManager.game_id_exists(gameState.game_id))

        self.gameManager.__add_game__(gameState)

        self.assertTrue(self.gameManager.game_id_exists(gameState.game_id))

    def testGetPlayerState(self):
        playerId = self.playerIds[0]
        gameState = GameState(self.playerIds, playerId)
        # Before game state has been added
        self.assertEqual(self.gameManager.get_player_state(gameState.game_id, playerId), None)

        mockedPlayerState = PlayerState(playerId, [], {}, [], self.playerIds[1])
        gameState.get_player_state = MagicMock(return_value=mockedPlayerState)
        self.gameManager.__add_game__(gameState)

        playerState = self.gameManager.get_player_state(gameState.game_id, playerId)
        self.assertEqual(playerState, mockedPlayerState)

    @patch.object(GameState, 'play')
    def testPlayHand(self, mockPlay):
        playerId = self.playerIds[0]
        gameState = GameState(self.playerIds, playerId)
        # Before game state has been added
        self.assertFalse(self.gameManager.play_hand(gameState.game_id, playerId, []))

        self.gameManager.__add_game__(gameState)
        gameState.play = mockPlay

        self.assertTrue(self.gameManager.play_hand(gameState.game_id, playerId, []))
        mockPlay.assert_called()

if __name__ == '__main__':
    unittest.main()