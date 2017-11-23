import unittest
from GameState import *

class GameStateTest(unittest.TestCase):

    player_ids = ["Joseph", "Peter", "Nick", "Micha"]


    def setUp(self):
        self.game_state = GameState()
        self.game_state.new_game(self.player_ids, self.player_ids[0])

    def testHandsAreUnique(self):
        all_cards = set()

        for i in range(0, len(self.player_ids)):
            hand = self.game_state.get_player_state(self.player_ids[i])['hand']
            self.assertEqual(len(hand), 13)
            all_cards = all_cards.union(hand)

        self.assertEquals(len(all_cards), 52)

    def testPlayOneCard(self):
        total_plays = 8
        expected_previous_plays = []
        for i in range(0, total_plays):
            player_id = self.player_ids[i % len(self.player_ids)]
            play = self.play_hand_for_player(player_id)
            expected_previous_plays.append((player_id, play))
            self.assertHandPlayed(expected_previous_plays)

    def testPlayHandReturnsFalse_whenPlayerCantPlayHand(self):
        invalid = set([Card(15, 6)])
        self.assertRaises(ValueError, self.game_state.play, self.player_ids[0], invalid)

    def testInitThrows_whenPlayerToGoFirstNotInPlayerIds(self):
        self.assertRaises(ValueError, self.game_state.new_game, self.player_ids, "Alex")

    def testPlayHandReturnsFalse_whenItIsNotThatPlayersTurn(self):
        self.assertRaises(ValueError, self.game_state.play, "Micha", set())

    def testGetNextPlayer(self):
        self.assertEqual(self.player_ids[1], self.game_state.__get_next_player__(self.player_ids[0]))
        self.game_state.finished_players.append(self.player_ids[2])
        # since player 2 has finished the game, he should be skipped
        self.assertEqual(self.player_ids[3], self.game_state.__get_next_player__(self.player_ids[1]))
        self.assertEqual(self.player_ids[0], self.game_state.__get_next_player__(self.player_ids[3]))

    def testIsGameFinished(self):
        self.assertFalse(self.game_state.is_game_finished())
        for i in range(0, 3):
            self.game_state.finished_players.append(self.player_ids[i])

        self.assertTrue(self.game_state.is_game_finished())

    def testGetPlayerState(self):
        player_state = self.game_state.get_player_state(self.player_ids[0])
        self.assertEqual(player_state['playersToCardsInHand'][self.player_ids[0]], 13)

    def test_serialization_deserialization(self):
        self.play_hand_for_player(self.player_ids[0])
        serialized_game = self.game_state.serialize()
        deserialized_game = GameState()
        deserialized_game.deserialize(serialized_game, self.game_state.get_id())
        self.assertEqual(self.game_state, deserialized_game)


    def play_hand_for_player(self, player_id):
        player_hand = self.game_state.get_player_state(player_id)['hand'].copy()
        player_play = set([player_hand.pop()]) # Play one card
        self.game_state.play(player_id, player_play)
        return player_play

    def assertHandPlayed(self, expectedPreviousPlays):
        previous_plays = self.game_state.__get_previous_plays__()
        self.assertEquals(expectedPreviousPlays, previous_plays)

if __name__ == '__main__':
    unittest.main()
