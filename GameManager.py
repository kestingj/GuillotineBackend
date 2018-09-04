from GameState import *
from GameStateCheckpointDao import *
import logging

          
# A GameManager manages all games for a single host. The server routes all calls to the game manager
class GameManager:

    def __init__(self):
        self.games = {}
        self.checkpoint_dao = GameStateCheckpointDao(False)

    def create_new_game(self, game_id, player_ids, player_to_go_first):
        game_state = GameState()
        game_state.new_game(game_id, player_ids, player_to_go_first)
        self.__add_game__(game_state, 0)

    def finish_game(self, game_id):
        pass
        # TODO

    def __add_game__(self, game_state, sequence_number):
        if game_state.get_id() in self.games:
            raise ValueError('Game with id: ' + game_state.get_id() + ' already exists')
        self.games[game_state.get_id()] = (game_state, sequence_number)
        logging.info('Added game with id: ' + str(game_state.get_id()))

    def __delete_game__(self, game_id):
        self.games.pop(game_id, None)
        logging.info('Deleted game with id: ' + str(game_id))

    def play_hand(self, game_id, player_id, hand):
        game_state = self.load_game_state(game_id)
        if game_state is None:
            raise ValueError('No game with id: ' + game_id + ' exists')
        game_state.play(player_id, hand)
        # TODO if this fails we may need to refresh the cache
        self.checkpoint_state(game_id, player_id)
        self.push_state_to_player(player_id, game_state.get_player_state(game_state.get_turn()))

    def game_id_exists(self, game_id):
        if game_id in self.games:
            return True
        else:
            logging.warning('No game with id: ' + str(game_id) + ' exists')
            return False

    def get_player_state(self, game_id, player_id):
        game_state = self.load_game_state(game_id)
        if game_state is None:
            return None
        return game_state.get_player_state(player_id)

    def checkpoint_state(self, game_id, player_id):
        game_state = self.games[game_id][0]
        player_state = game_state.get_player_state(player_id)

        updated_hand = player_state['hand']
        turn = player_state['turn']
        previous_plays = player_state['previousPlays']
        player_index = game_state.get_index_for_player(player_id)

        sequence_number = self.games[game_id][1]

        self.checkpoint_dao.checkpoint_game_state(
            game_id,
            player_index,
            previous_plays,
            updated_hand,
            turn,
            sequence_number)

        self.games[game_id] = (game_state, self.games[game_id][1] + 1)

    def push_state_to_player(self, player_id, player_state):
        pass
        # use push notifications to push state to player

    def load_game_state(self, game_id):
        if not self.game_id_exists(game_id):
            checkpoint = self.checkpoint_dao.load_checkpoint(game_id)
            if checkpoint is None:
                return None
            restored_game_state = GameState()
            restored_game_state.deserialize(checkpoint, game_id)
            self.games[game_id] = (restored_game_state, int(checkpoint['sequenceNumber']))
        return self.games[game_id][0]


