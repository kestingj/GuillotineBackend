
from Card import Card
from random import shuffle
from PlayerState import PlayerState

# A GameState tracks all state for a single game. This state includes:
# ID for the game
# Players in the game
# Hands for each player
# History of plays made so far in the game
# Players that have already finished the game
# Players that have acked the completion of the game
class GameState:
    def __init__(self):
        self.initialized = False

    def deserialize(self, game_json, game_id):
        if self.initialized:
            raise ValueError("Game already initialized")
        self.game_id = game_id
        self.player_ids = game_json['playerIds']
        self.previous_plays = self.deserialize_previous_plays(game_json['previousPlays'])
        self.player_hands = game_json['playerHands']
        self.turn = game_json['turn']
        self.finished_players= game_json['finishedPlayers'] # Players that have played all their cards or have dropped from the game
        self.initialized = True
        self.players_recognizing_completion = game_json['ackedCompletion']

    def deserialize_previous_plays(self, previous_plays_json):
        previous_plays = []
        for play in previous_plays_json:
            previous_plays.append((play['playerId'], play['play']))
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
        self.finished_players = []
        self.players_recognizing_completion = []
        self.initialized = True

    # Throws if playerId does not equal turn or if play is not a subset of playerId's current hand
    def play(self, player_id, play):
        if player_id != self.turn:
            raise ValueError("It is " + self.turn +"'s, not " + player_id + "'s, turn")
        existing_hand = self.player_hands[player_id]
        if not (play.issubset(existing_hand)):
            raise ValueError("play: " + str(play) + " is not a subset of existing hand " + str(existing_hand) + " for player " + player_id)
        self.player_hands[player_id] = existing_hand - play
        if len(self.player_hands[player_id]) == 0:
            self.finished_players.append(player_id)
        self.previous_plays.append((player_id, play))
        self.turn = self.__get_next_player__(player_id)

    def get_player_state(self, playerId):
        player_to_hand_size = {}
        for player_id in self.player_ids:
            player_to_hand_size[player_id] = len(self.player_hands[player_id])
        return PlayerState(playerId, self.player_hands[playerId], player_to_hand_size, self.__get_previous_plays__(), self.get_turn())

    #Returns True if all players have acked completion. False otherwise
    def ack_completion(self, player_id):
        if player_id not in self.players_recognizing_completion:
            self.players_recognizing_completion.append(player_id)
        if len(self.players_recognizing_completion) == len(self.finished_players):
            return True
        return False

    def get_turn(self):
        return self.turn

    def __get_previous_plays__(self):
        return self.previous_plays

    def get_id(self):
        return self.game_id

    def is_game_finished(self):
        return len(self.finished_players) == len(self.player_ids)

    def __get_next_player__(self, currentPlayerId):
        index = self.player_ids.index(currentPlayerId)

        while(True):
            index += 1
            if index >= len(self.player_ids):
                index = 0
            if self.player_ids[index] not in self.finished_players:
                break

        return self.player_ids[index]

    def serialize(self):
        json = {}
        json['playerHands'] = self.player_hands
        json['turn'] = self.turn
        json['previousPlays'] = self.__jsonify_previous_plays__()
        json['finishedPlayers'] = self.finished_players
        json['playerIds'] = self.player_ids
        json['ackedCompletion'] = self.players_recognizing_completion
        return json

    def __jsonify_previous_plays__(self):
        prev_plays_json = []
        for play in self.previous_plays:
            play_dict = {}
            play_dict['playerId'] = play[0]
            play_dict['play'] = play[1]
            prev_plays_json.append(play_dict)
        return prev_plays_json

    def __eq__(self, other):
        return self.game_id == other.game_id \
               and self.player_ids == other.player_ids \
               and self.player_hands == other.player_hands \
               and self.turn == other.turn \
               and self.finished_players == other.finished_players \
               and self.previous_plays == other.previous_plays \
               and self.players_recognizing_completion == other.players_recognizing_completion

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
