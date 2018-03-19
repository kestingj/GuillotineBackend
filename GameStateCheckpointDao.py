import boto3

class GameStateCheckpointDao:

    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = dynamodb.Table('GameStateCheckpointTable-us-west-2')

    def checkpoint_game_state(self, game_id, serialized_game_state, old_sequence_number):
        item = {'gameId' : game_id,
                'serializedGameState' : serialized_game_state,
                'sequenceNumber' : old_sequence_number + 1,
                'timestamp' : 100} # TODO Actual timestamp
        # TODO Add entry if it does not already exist or update existing entry if the old_sequence_number matches
        # the sequence number of the current table entry

    def load_checkpoint(self, game_id):
        pass