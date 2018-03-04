import boto3

class GameStateCheckpointDao:

    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('GameStateCheckpointTable-us-west-2')

    def checkpoint_game_state(self, game_id, serialized_game_state, sequence_number):
        item = {'gameId' : game_id,
                'serializedGameState' : serialized_game_state,
                'sequenceNumber' : sequence_number,
                'timestamp' : }

    def load_checkpoint(self, game_id):
        pass