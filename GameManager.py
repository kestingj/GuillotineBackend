from GameState import *
import logging

          
# A GameManager manages all games for a single host. The server routes all calls to the game manager
class GameManager:

    def __init__(self):
        self.games = {}

    def create_new_game(self, game_id, player_ids, player_to_go_first):
        game_state = GameState()
        game_state.new_game(game_id, player_ids, player_to_go_first)
        self.__add_game__(game_state)

    def __add_game__(self, game_state):
        if game_state.get_id() in self.games:
            raise ValueError('Game with id: ' + game_state.get_id() + ' already exists')
        self.games[game_state.get_id()] = game_state
        logging.info('Added game with id: ' + str(game_state.get_id()))

    def __delete_game__(self, game_id):
        self.games.pop(game_id, None)
        logging.info('Deleted game with id: ' + str(game_id))

    def play_hand(self, game_id, player_id, hand):
        if not self.game_id_exists(game_id):
            raise ValueError('No game with id: ' + game_id + ' is currently being managed by this instance')
        game_state = self.games[game_id]
        game_state.play(player_id, hand)
        self.push_state_to_player(player_id, game_state.get_player_state(game_state.get_turn()))

    def game_id_exists(self, game_id):
        if game_id in self.games:
            return True
        else:
            logging.warning('No game with id: ' + str(game_id) + ' exists')
            return False

    def get_player_state(self, game_id, player_id):
        if not self.game_id_exists(game_id):
            # TODO: Deserialize from checkpoint
            return None
        game_state = self.games[game_id]
        return game_state.get_player_state(player_id)

    def checkpoint_state(self, game_id):
        game_state = self.games[game_id]
        serialized_game_state = game_state

    def push_state_to_player(self, player_id, player_state):
        pass
        # use push notifications to push state to player

    def ack_finished_game(self, game_id, player_id):
        acked_by_all_players = self.games[game_id].ack_completion(player_id)
        if acked_by_all_players:
            #TODO: Implement a cron job that scans through all Games and sends delete messages for all games that have received a completion ack from every player
            self.__delete_game__(game_id)
