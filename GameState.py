
from Card import Card
from Card import serialize_card_set
from Card import deserialize_card_list
from random import shuffle
from PlayerState import PlayerState

# A GameState tracks all state for a single game. This state includes:
# ID for the game
# Players in the game
# Hands for each player
# History of plays made so far in the game
# The player who has the next play
class GameState:
    def __init__(self):
        self.initialized = False

    # TODO make this a static method
    def deserialize(self, game_json, game_id):
        if self.initialized:
            raise ValueError("Game already initialized")
        self.game_id = game_id
        self.player_ids = game_json['playerIds']
        self.turn = game_json['turn']
        self.previous_plays = self.deserialize_previous_plays(game_json['previousPlays'])
        self.player_hands = {}
        for i in range(len(self.player_ids)):
            self.player_hands[self.player_ids[i]] = game_json['player' + str(i) + 'Hand']
        self.initialized = True

    def deserialize_previous_plays(self, previous_plays):
        current_player = self.player_ids[0]

        previous_plays = []
        for play in previous_plays:
            previous_plays.append((current_player, deserialize_card_list(play)))
        return previous_plays

    def new_game(self, game_id, player_ids, player_to_go_first):
        if self.initialized:
            raise ValueError("Game already initialized")
        if player_to_go_first not in player_ids:
            raise ValueError("Player to go first: " + player_to_go_first + " not found in playerIds: " + str(player_ids))
        hands = __get_random_hands__(len(player_ids))
        playerHands = {}
        for i in range(0, len(player_ids)):
            playerHands[player_ids[i]] = hands[i]
        self.player_hands = playerHands
        self.previous_plays = []  # Track the entire game's play history
        self.game_id = game_id
        self.player_ids = player_ids
        self.turn = player_to_go_first
        self.initialized = True

    # Throws if playerId does not equal turn or if play is not a subset of playerId's current hand
    def play(self, player_id, play):
        if player_id != self.turn:
            raise ValueError("It is " + self.turn +"'s, not " + player_id + "'s, turn")
        existing_hand = self.player_hands[player_id]
        if not (play.issubset(existing_hand)):
            raise ValueError("play: " + str(play) + " is not a subset of existing hand " + str(existing_hand) + " for player " + player_id)
        self.player_hands[player_id] = existing_hand - play
        self.previous_plays.append(play)
        next_turn = self.__get_next_player__(player_id)
        # Skip over finished players, appending empty plays as we do so
        while len(self.player_hands[next_turn]) == 0:
            self.previous_plays.append(set())
            next_turn = self.__get_next_player__(next_turn)
        self.turn = next_turn

    def get_player_state(self, playerId):
        player_to_hand_size = {}
        for player_id in self.player_ids:
            player_to_hand_size[player_id] = len(self.player_hands[player_id])
        return PlayerState(
            playerId,
            serialize_card_set(self.player_hands[playerId]),
            player_to_hand_size,
            self.__serialize_previous_plays__(),
            self.get_turn(),
            self.player_ids)

    def get_turn(self):
        return self.turn

    def get_index_for_player(self, player_id):
        return self.player_ids.index(player_id)

    def __get_previous_plays__(self):
        return self.previous_plays

    def get_id(self):
        return self.game_id

    def is_game_finished(self):
        finished_count = 0
        for player in self.player_ids:
            if len(self.player_hands[player]) == 0:
                finished_count += 1
        return finished_count == len(self.player_ids) - 1

    def __get_next_player__(self, currentPlayerId):
        index = self.player_ids.index(currentPlayerId)

        index += 1
        if index >= len(self.player_ids):
            index = 0

        return self.player_ids[index]

    def __serialize_previous_plays__(self):
        prev_plays_list = []
        for play in self.previous_plays:
            prev_plays_list.append(serialize_card_set(play))
        return prev_plays_list

    def __eq__(self, other):
        return self.game_id == other.game_id \
               and self.player_ids == other.player_ids \
               and self.player_hands == other.player_hands \
               and self.turn == other.turn \
               and self.previous_plays == other.previous_plays

def __get_random_hands__(number_of_players):
        cards = []
        for rank in range(2, 15):
            for suit in range(0, 4):
                cards.append(Card(rank, suit))
        shuffle(cards)
        hands = []
        for player in range(0, number_of_players):
            hand = []
            for i in range(0, 13):
                hand.append(cards.pop())
            hands.append(set(hand))
        return hands
