import unittest
from GameStateCheckpointDao import GameStateCheckpointDao
from Card import *
import random
import boto3
import botocore.exceptions


# To run this test a local instance of DDB must be running locally:
# cd ~/Downloads/dynamodb_local_latest/
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
class GameStateCheckpointDaoTest(unittest.TestCase):

    player_ids = ["Joseph", "Peter", "Nick", "Micha"]
    game_id = "gameId"

    def setUp(self):
        self.dao = GameStateCheckpointDao(True)
        self.create_table()

    def tearDown(self):
        self.delete_table()

    def test_new_game(self):
        hands = self.get_random_hands()
        self.dao.new_game(self.game_id, self.player_ids, self.player_ids[0], hands)
        self.assert_checkpoint(self.player_ids[0], '0', hands)

    def test_checkpoint_game(self):
        hands = self.get_random_hands()
        play = str(Card(0, 2))
        self.dao.new_game(self.game_id, self.player_ids, self.player_ids[0], hands)
        hands[self.player_ids[0]] = hands[self.player_ids[1]]

        self.dao.checkpoint_game_state(self.game_id, 0, play, hands[self.player_ids[1]], self.player_ids[1], 0)
        self.assert_checkpoint(self.player_ids[1], '1', hands, play)

    def test_checkpoint_game_throws_when_sequence_number_does_not_increase(self):
        hands = self.get_random_hands()
        play = str(Card(0, 2))
        self.dao.new_game(self.game_id, self.player_ids, self.player_ids[0], hands)
        hands[self.player_ids[0]] = hands[self.player_ids[1]]

        self.assertRaises(botocore.exceptions.ClientError, self.dao.checkpoint_game_state, self.game_id, 0, play, hands[self.player_ids[1]], self.player_ids[1], 1)

    def test_checkpoint_game_throws_when_game_does_not_exist(self):
        hands = self.get_random_hands()
        play = str(Card(0, 2))

        self.assertRaises(botocore.exceptions.ClientError, self.dao.checkpoint_game_state, self.game_id, 0, play,
                          hands[self.player_ids[1]], self.player_ids[1], 1)

    def test_delete_game(self):
        hands = self.get_random_hands()
        self.dao.new_game(self.game_id, self.player_ids, self.player_ids[0], hands)
        self.dao.delete_game(self.game_id)
        # Test that delete is idempotent
        self.dao.delete_game(self.game_id)
        self.assertIsNone(self.dao.load_checkpoint(self.game_id))

    def test_load_game_returns_none_when_game_does_not_exist(self):
        self.assertIsNone(self.dao.load_checkpoint('bogus'))

    def get_random_hands(self):
        hands = {}
        for player in self.player_ids:
            hand = set()
            hand.add(Card(random.randint(0, 4), random.randint(2, 15)))
            hands[player] = serialize_card_set(hand)

        return hands

    def create_table(self):
        dynamo_db = boto3.resource(
            'dynamodb',
            aws_access_key_id="anything",
            aws_secret_access_key="anything",
            region_name="us-west-2",
            endpoint_url="http://localhost:8000")
        attribute_definitions = [
            {
                'AttributeName': 'gameId',
                'AttributeType': 'S'
            },
        ]
        key_schema = [
            {
                'AttributeName': 'gameId',
                'KeyType': 'HASH'
            },
        ]
        provisioned_throughput = {
            'ReadCapacityUnits': 123,
            'WriteCapacityUnits': 123
        }
        dynamo_db.create_table(TableName='GameStateCheckpointTable-us-west-2',
                               AttributeDefinitions=attribute_definitions,
                               KeySchema=key_schema,
                               ProvisionedThroughput=provisioned_throughput)

    def delete_table(self):
        dynamo_db = boto3.client(
            'dynamodb',
            aws_access_key_id="anything",
            aws_secret_access_key="anything",
            region_name="us-west-2",
            endpoint_url="http://localhost:8000")
        dynamo_db.delete_table(TableName='GameStateCheckpointTable-us-west-2')

    def assert_checkpoint(self, turn, sequence_number, hands, previous_plays=None):
        checkpoint = self.dao.load_checkpoint(self.game_id)
        self.assertEqual(checkpoint['gameId'], self.game_id)
        self.assertEqual(checkpoint['turn'], turn)
        self.assertEqual(checkpoint['sequenceNumber'], sequence_number)
        self.assertEqual(checkpoint['playerIds'], self.player_ids)
        for player in self.player_ids:
            index = self.player_ids.index(player)
            self.assertEqual(checkpoint['player' + str(index) + 'Hand'], hands[player])
        if previous_plays is not None:
            self.assertEqual(checkpoint['previousPlays'], previous_plays)

if __name__ == '__main__':
    unittest.main()