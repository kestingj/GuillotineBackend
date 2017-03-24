import unittest
from GameState import *


class GameStateTest(unittest.TestCase):

    playerIds = ["Joseph", "Peter", "Nick", "Micha"]
    gameState = GameState(playerIds)

    def testHandsAreUnique(self):
        allCards = set()

        for i in range(0, len(self.playerIds)):
            playerState = self.gameState.getPlayerState(self.playerIds[i])
            self.assertEqual(len(playerState), 13)
            allCards = allCards.union(playerState)

        self.assertEquals(len(allCards), 52)

    def testPlayOneCard(self):
        totalPlays = 8
        expectedPreviousPlays = []
        for i in range(0, totalPlays):
            playerId = self.playerIds[i % len(self.playerIds)]
            play = self.playHandForPlayer(playerId)
            print play
            expectedPreviousPlays.append((playerId, play))
            print expectedPreviousPlays
            self.assertHandPlayed(playerId, expectedPreviousPlays)

    def testPlayHandReturnsFalse_whenPlayerCantPlayHand(self):
        invalid = set([Card(15, 6)])
        self.assertFalse(self.gameState.playHand(self.playerIds[0], invalid))

    def playHandForPlayer(self, playerId):
        playerHand = self.gameState.getPlayerState(playerId).copy()
        print "playerHand"
        print playerHand
        playerPlay = set([playerHand.pop()])
        self.gameState.playHand(playerId, playerPlay)
        return playerPlay

    def assertHandPlayed(self, playerId, expectedPreviousPlays):
        previousPlays = self.gameState.getPreviousPlays()
        print previousPlays
        self.assertEquals(expectedPreviousPlays, previousPlays)


if __name__ == '__main__':
    unittest.main()
