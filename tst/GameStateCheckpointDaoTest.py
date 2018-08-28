import unittest
from GameStateCheckpointDao import GameStateCheckpointDao
from Card import *
import random


# To run this test a local instance of DDB must be running locally:
# cd ~/Downloads/dynamodb_local_latest/
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
class GameStateCheckpointDaoTest(unittest.TestCase):

    player_ids = ["Joseph", "Peter", "Nick", "Micha"]
    game_id = "gameId"

    def setUp(self):
        self.dao = GameStateCheckpointDao(True)

    def testNewGame(self):
        hands = self.getRandomHands()
        self.dao.new_game(self.game_id, self.player_ids, self.player_ids[0], hands)
        checkpoint = self.dao.load_checkpoint(self.game_id)
        self.assertEqual(checkpoint['gameId'], self.game_id)
        self.assertEqual(checkpoint['turn'], self.player_ids[0])
        self.assertEqual(checkpoint['sequenceNumber'], 0)
        self.assertEqual(checkpoint['playerIds'], self.player_ids)
        for player in self.player_ids:
            index = self.player_ids.index(player)
            self.assertEqual(checkpoint['player' + str(index) + 'Hand'], hands[player])

    def testCheckpointGame(self):
        pass

    def testLoadCheckpoint(self):
        pass

    def deleteGame(self):
        pass

    def getRandomHands(self):
        hands = {}
        for player in self.player_ids:
            hands[player] = serialize_card_set(set(Card(random.randint(0, 4), random.randint(2, 15))))

        return hands

if __name__ == '__main__':
    unittest.main()