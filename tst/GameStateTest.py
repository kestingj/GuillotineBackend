import unittest
from GameState import *

class GameStateTest(unittest.TestCase):

    player_ids = ["Joseph", "Peter", "Nick", "Micha"]
    game_id = "gameId"

    def setUp(self):
        self.game_state = GameState()
        self.game_state.new_game(self.game_id, self.player_ids, self.player_ids[0])

    def testHandsAreUnique(self):
        all_cards = set()

        for i in range(0, len(self.player_ids)):
            hand = deserialize_card_list(self.game_state.get_player_state(self.player_ids[i])['hand'])
            self.assertEqual(len(hand), 13)
            all_cards = all_cards.union(hand)

        self.assertEqual(len(all_cards), 52)

    def testPlayOneCard(self):
        total_plays = 8
        expected_previous_plays = []
        for i in range(0, total_plays):
            player_id = self.player_ids[i % len(self.player_ids)]
            play = self.play_hand_for_player(player_id)
            expected_previous_plays.append(play)
            self.assertHandPlayed(expected_previous_plays)

    def testPlayHandReturnsFalse_whenPlayerCantPlayHand(self):
        invalid = set([Card(15, 6)])
        self.assertRaises(ValueError, self.game_state.play, self.player_ids[0], invalid)

    def testInitThrows_whenPlayerToGoFirstNotInPlayerIds(self):
        self.assertRaises(ValueError, self.game_state.new_game, self.game_id, self.player_ids, "Alex")

    def testPlayHandThrows_whenItIsNotThatPlayersTurn(self):
        self.assertRaises(ValueError, self.game_state.play, "Micha", set())

    def testNextPlayer(self):
        self.assertEqual(self.player_ids[0], self.game_state.get_player_state(self.player_ids[0])['turn'])
        self.play_hand_for_player(self.player_ids[0])
        self.assertEqual(self.player_ids[1], self.game_state.get_player_state(self.player_ids[1])['turn'])
        self.finish_player(self.player_ids[2])
        # since player 2 has finished the game, he should be skipped
        self.assertEqual(self.player_ids[3], self.game_state.get_player_state(self.player_ids[3])['turn'])
        self.play_hand_for_player(self.player_ids[3])
        self.assertEqual(self.player_ids[0], self.game_state.get_player_state(self.player_ids[0])['turn'])

    def testIsGameFinished(self):
        self.assertFalse(self.game_state.is_game_finished())
        for i in range(len(self.player_ids) - 1):
            self.finish_player(self.player_ids[i])

        self.assertTrue(self.game_state.is_game_finished())

    def testGetPlayerState(self):
        for i in range(len(self.player_ids)):
            player_id = self.player_ids[i]
            player_state = self.game_state.get_player_state(player_id)
            for j in range(len(self.player_ids)):
                self.assertEqual(player_state['playersToCardsInHand'][self.player_ids[j]], 13)

            self.assertEqual(player_state['playerId'], player_id)
            self.assertEqual(player_state['turn'], self.player_ids[0])
            self.assertEqual(player_state['previousPlays'], [])
            self.assertEqual(player_state['hand'], serialize_card_set(self.game_state.player_hands[player_id]))
            self.assertEqual(player_state['turnOrder'], self.player_ids)

    def testFinishedPlayersAddEmptyPlayToPreviousPlays(self):
        self.finish_player(self.player_ids[2])
        base_line = self.game_state.get_player_state(self.player_ids[0])['previousPlays']
        self.play_hand_for_player(self.player_ids[3])
        self.play_hand_for_player(self.player_ids[0])
        self.play_hand_for_player(self.player_ids[1])

        new_previous_plays = self.game_state.get_player_state(self.player_ids[0])['previousPlays']

        self.assertEqual(len(base_line) + 4, len(new_previous_plays))
        self.assertEqual(new_previous_plays[len(new_previous_plays) - 1], '')

    def testInitializeFromCheckpoint(self):
        # Play one round
        for i in range(len(self.player_ids)):
            self.play_hand_for_player(self.player_ids[i])

         # Serialize the game state
        game_state_json = {}
        game_state_json['playerIds'] = self.player_ids
        game_state_json['turn'] = self.game_state.get_turn()
        game_state_json['previousPlays'] = self.game_state.get_player_state(self.player_ids[0])['previousPlays']
        for i in range(len(self.player_ids)):
            game_state_json['player' + str(i) + 'Hand'] = self.game_state.get_player_state(self.player_ids[i])['hand']

        new_game_state = GameState()
        new_game_state.deserialize(game_state_json, self.game_id)

        self.assertEqual(new_game_state, self.game_state)

    def testGetIndexForPlayer(self):
        for i in range(len(self.player_ids)):
            self.assertEqual(self.game_state.get_index_for_player(self.player_ids[i]), i)

    def play_hand_for_player(self, player_id):
        player_hand = deserialize_card_list(self.game_state.get_player_state(player_id)['hand'])
        player_play = set()
        player_play.add(player_hand.pop())  # Play one card
        self.game_state.play(player_id, player_play)
        return player_play

    def assertHandPlayed(self, expectedPreviousPlays):
        previous_plays = self.game_state.__get_previous_plays__()
        self.assertEqual(expectedPreviousPlays, previous_plays)

    def finish_player(self, player_id):
        player_state = self.game_state.get_player_state(self.game_state.get_turn())
        while len(deserialize_card_list(self.game_state.get_player_state(player_id)['hand'])) > 0:
            if player_state['playerId'] == player_id:
                play = set()
                play.add(deserialize_card_list(player_state['hand']).pop())
                self.game_state.play(player_id, play)
            else:
                self.game_state.play(player_state['playerId'], set())
            player_state = self.game_state.get_player_state(self.game_state.get_turn())

if __name__ == '__main__':
    unittest.main()
