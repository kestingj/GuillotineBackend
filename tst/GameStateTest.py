import unittest
from GameState import *

class GameStateTest(unittest.TestCase):

    playerIds = ["Joseph", "Peter", "Nick", "Micha"]

    def setUp(self):
        self.gameState = GameState()
        self.gameState.new_game(self.playerIds, self.playerIds[0])

    def testHandsAreUnique(self):
        allCards = set()

        for i in range(0, len(self.playerIds)):
            hand = self.gameState.getPlayerState(self.playerIds[i])['hand']
            self.assertEqual(len(hand), 13)
            allCards = allCards.union(hand)

        self.assertEquals(len(allCards), 52)

    def testPlayOneCard(self):
        totalPlays = 8
        expectedPreviousPlays = []
        for i in range(0, totalPlays):
            playerId = self.playerIds[i % len(self.playerIds)]
            play = self.playHandForPlayer(playerId)
            expectedPreviousPlays.append((playerId, play))
            self.assertHandPlayed(expectedPreviousPlays)

    def testPlayHandReturnsFalse_whenPlayerCantPlayHand(self):
        invalid = set([Card(15, 6)])
        self.assertRaises(ValueError, self.gameState.play, self.playerIds[0], invalid)

    def testInitThrows_whenPlayerToGoFirstNotInPlayerIds(self):
        self.assertRaises(ValueError, self.gameState.new_game, self.playerIds, "Alex")

    def testPlayHandReturnsFalse_whenItIsNotThatPlayersTurn(self):
        self.assertRaises(ValueError, self.gameState.play, "Micha", set())

    def testGetNextPlayer(self):
        self.assertEqual(self.playerIds[1], self.gameState.getNextPlayer(self.playerIds[0]))
        self.gameState.finishedPlayers.append(self.playerIds[2])
        # since player 2 has finished the game, he should be skipped
        self.assertEqual(self.playerIds[3], self.gameState.getNextPlayer(self.playerIds[1]))
        self.assertEqual(self.playerIds[0], self.gameState.getNextPlayer(self.playerIds[3]))

    def testIsGameFinished(self):
        self.assertFalse(self.gameState.isGameFinished())
        for i in range(0, 3):
            self.gameState.finishedPlayers.append(self.playerIds[i])

        self.assertTrue(self.gameState.isGameFinished())

    def testGetPlayerState(self):
        player_state = self.gameState.getPlayerState(self.playerIds[0])
        self.assertEqual(player_state['playersToCardsInHand'][self.playerIds[0]], 13)

    def test_serialization_deserialization(self):
        self.playHandForPlayer(self.playerIds[0])
        serialized_game = self.gameState.serialize()
        deserialized_game = GameState()
        deserialized_game.deserialize(serialized_game, self.gameState.getId())
        self.assertEqual(self.gameState, deserialized_game)


    def playHandForPlayer(self, playerId):
        playerHand = self.gameState.getPlayerState(playerId)['hand'].copy()
        playerPlay = set([playerHand.pop()]) # Play one card
        self.gameState.play(playerId, playerPlay)
        return playerPlay

    def assertHandPlayed(self, expectedPreviousPlays):
        previousPlays = self.gameState.getPreviousPlays()
        self.assertEquals(expectedPreviousPlays, previousPlays)

if __name__ == '__main__':
    unittest.main()
