import unittest
from GameManager import *
from mock import MagicMock
from mock import patch


class GameManagerTest(unittest.TestCase):

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

        mockedPlayerState = PlayerState(self.player_ids[0], [], {}, [], self.player_ids[1], self.player_ids)
        game_state.get_player_state = MagicMock(return_value=mockedPlayerState)

        player_state = self.game_manager.get_player_state(self.game_id, self.player_ids[0])
        self.assertEqual(player_state, mockedPlayerState)

    @patch('GameStateCheckpointDao.GameStateCheckpointDao')
    @patch('GameState.GameState')
    def testPlayHand(self, mock_game_state, mock_checkpoint_dao):
        sequence_number = 0
        self.game_manager.games[self.game_id] = (mock_game_state, sequence_number)
        self.game_manager.checkpoint_dao = mock_checkpoint_dao

        # Mocks for Checkpoint
        mockedPlayerState = PlayerState(self.player_ids[0], '', {}, [], self.player_ids[1], self.player_ids)
        mock_game_state.get_player_state = MagicMock(return_value=mockedPlayerState)
        mock_game_state.get_index_for_player = MagicMock(return_value=0)

        self.game_manager.play_hand(self.game_id, self.player_ids[0], [])
        mock_game_state.play.assert_called_with(self.player_ids[0], [])

        mock_checkpoint_dao.checkpoint_game_state.assert_called_with(self.game_id, 0, [], '', self.player_ids[1], 0)

    def testPushStateToPlayer(self):
        # TODO Write when implemented
        pass

    def __initialize_game_state__(self):
        game_state = GameState()
        game_state.new_game(self.game_id, self.player_ids, self.player_ids[0])
        self.game_manager.__add_game__(game_state, 0)
        return game_state

if __name__ == '__main__':
    unittest.main()