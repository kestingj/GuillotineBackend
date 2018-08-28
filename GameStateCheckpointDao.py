import boto3
import time

class GameStateCheckpointDao:

    # TODO Dependency Injection
    def __init__(self, isTest):
        if (isTest):
            dynamo_db = boto3.resource(
                'dynamodb',
                aws_access_key_id="anything",
                aws_secret_access_key="anything",
                region_name="us-west-2",
                endpoint_url="http://localhost:8000")
        else:
            dynamo_db = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = dynamo_db.Table('GameStateCheckpointTable-us-west-2')

    # Pass in serialized player_hands
    def new_game(self, game_id, player_ids, starting_player, player_hands):
        item = {'gameId': game_id,
                'playerIds': player_ids,
                'turn': starting_player,
                'sequenceNumber': 0,
                'timestamp': time.time()}
        for i in range(len(player_ids)):
            player_id = player_ids[i]
            hand = player_hands[player_id]
            item['player' + str(i) + 'Hand'] = hand

        conditional_expression = 'attribute_not_exists(gameId)'

        self.table.put_item(Item=item, ConditionalExpression=conditional_expression)

    # Pass in serialized previous_plays and updated_hand
    def checkpoint_game_state(self, game_id, player_index, previous_plays, updated_hand, next_player, old_sequence_number):
        key = {'gameId': game_id}

        updates = {'turn': {'Value': next_player, 'Action': 'PUT'},
                   'player' + str(player_index) + 'Hand': {'Value': updated_hand, 'Action': 'PUT'},
                   'previousPlays': {'Value': previous_plays, 'Action': 'PUT'},
                   'sequenceNumber': {'Value': old_sequence_number + 1, 'Action': 'PUT'},
                   'timestamp': {'Value': time.time(), 'Action': 'PUT'}}

        expected = {'sequenceNumber': {'Value': old_sequence_number, 'ComparisonOperator': 'EQ'}}

        self.table.update_item(Key=key, AttributeUpdates=updates, Expected=expected)

    def load_checkpoint(self, game_id):
        return self.table.get_item(Key={'gameId': game_id}, ConsistentRead=True)['Item']
