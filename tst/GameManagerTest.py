import unittest
from GameManager import *
from mock import MagicMock
from mock import patch

class GameStateTest(unittest.TestCase):

    player_ids = ["Joseph", "Peter", "Nick", "Micha"]
    game_id = "gameId"

    def setUp(self):
        self.game_manager = GameManager()

    def testCreateNewGame(self):
        self.game_manager.create_new_game(self.game_id, self.player_ids, self.player_ids[0])
        self.assertTrue(self.game_manager.game_id_exists(self.game_id))

    def testDeleteGame(self):
        self.__initialize_game_state__()
        self.game_manager.__delete_game__(self.game_id)
        self.assertFalse(self.game_manager.game_id_exists(self.game_id))

        # Assert that delete is idempotent
        self.game_manager.__delete_game__(self.game_id)

    def testGameIdExists(self):
        # Before game state has been added
        self.assertFalse(self.game_manager.game_id_exists(self.game_id))

        self.__initialize_game_state__()

        self.assertTrue(self.game_manager.game_id_exists(self.game_id))

    def testGetPlayerState(self):
        game_state = self.__initialize_game_state__()

        mockedPlayerState = PlayerState(self.player_ids[0], [], {}, [], self.player_ids[1])
        game_state.get_player_state = MagicMock(return_value=mockedPlayerState)

        player_state = self.game_manager.get_player_state(self.game_id, self.player_ids[0])
        self.assertEqual(player_state, mockedPlayerState)

    @patch('GameState.GameState')
    def testPlayHand(self, mock_game_state):

        self.game_manager.games[self.game_id] = mock_game_state


        self.game_manager.play_hand(self.game_id, self.player_ids[0], [])
        mock_game_state.play.assert_called()

    def __initialize_game_state__(self):
        game_state = GameState()
        game_state.new_game(self.game_id, self.player_ids, self.player_ids[0])
        self.game_manager.__add_game__(game_state)
        return game_state

if __name__ == '__main__':
    unittest.main()