
from Card import Card
from random import shuffle
from PlayerState import PlayerState
import uuid

# A GameState tracks all state for a single game. This state includes:
# ID for the game
# Players in the game
# Hands for each player
# History of plays made so far in the game
# Players that have already finished the game
class GameState:
    def __init__(self):
        self.initialized = False

    def deserialize(self, game_json, game_id):
        if self.initialized:
            raise ValueError("Game already initialized")
        self.gameId = game_id
        self.playerIds = game_json['playerIds']
        self.previousPlays = self.deserialize_previous_plays(game_json['previousPlays'])
        self.playerHands = game_json['playerHands']
        self.turn = game_json['turn']
        self.finishedPlayers= game_json['finishedPlayers']
        self.initialized = True

    def deserialize_previous_plays(self, previous_plays_json):
        previous_plays = []
        for play in previous_plays_json:
            previous_plays.append((play['playerId'], play['play']))
        return previous_plays

    def new_game(self, player_ids, player_to_go_first):
        if self.initialized:
            raise ValueError("Game already initialized")
        if player_to_go_first not in player_ids:
            raise ValueError("Player to go first: " + player_to_go_first + " not found in playerIds: " + str(player_ids))
        hands = getRandomHands(len(player_ids))
        playerHands = {}
        for i in range(0, len(player_ids)):
            playerHands[player_ids[i]] = hands[i]
        self.playerHands = playerHands
        self.previousPlays = []  # Track the entire game's play history
        self.gameId = str(uuid.uuid4())
        self.playerIds = player_ids
        self.turn = player_to_go_first
        self.finishedPlayers = []
        self.initialized = True

    # Throws if playerId does not equal turn or if play is not a subset of playerId's current hand
    def play(self, playerId, play):
        if playerId != self.turn:
            raise ValueError("It is " + self.turn +"'s, not " + playerId + "'s, turn")
        existingHand = self.playerHands[playerId]
        if not (play.issubset(existingHand)):
            raise ValueError("play: " + str(play) + " is not a subset of existing hand " + str(existingHand) + " for player " + playerId)
        self.playerHands[playerId] = existingHand - play
        if len(self.playerHands[playerId]) == 0:
            self.finishedPlayers.append(playerId)
        self.previousPlays.append((playerId, play))
        self.turn = self.getNextPlayer(playerId)

    def getPlayerState(self, playerId):
        player_to_hand_size = {}
        for player_id in self.playerIds:
            player_to_hand_size[player_id] = len(self.playerHands[player_id])
        return PlayerState(playerId, self.playerHands[playerId], player_to_hand_size, self.getPreviousPlays(), self.getTurn())

    def getTurn(self):
        return self.turn

    def getPreviousPlays(self):
        return self.previousPlays

    def clearPreviousPlays(self):
        self.previousPlays = []

    def getId(self):
        return self.gameId

    def getPlayersIds(self):
        return self.playerIds

    def getFinishedPlayers(self):
        return self.finishedPlayers

    # Game is finished when all but one player has finished
    def isGameFinished(self):
        return len(self.finishedPlayers) == len(self.playerIds) - 1

    def getNextPlayer(self, currentPlayerId):

        index = self.playerIds.index(currentPlayerId)

        while(True):
            index += 1
            if index >= len(self.playerIds):
                index = 0
            if self.playerIds[index] not in self.finishedPlayers:
                break

        return self.playerIds[index]

    def serialize(self):
        json = {}
        json['playerHands'] = self.playerHands
        json['turn'] = self.turn
        json['previousPlays'] = self.jsonify_previous_plays()
        json['finishedPlayers'] = self.finishedPlayers
        json['playerIds'] = self.playerIds
        return json

    def jsonify_previous_plays(self):
        prev_plays_json = []
        for play in self.previousPlays:
            play_dict = {}
            play_dict['playerId'] = play[0]
            play_dict['play'] = play[1]
            prev_plays_json.append(play_dict)
        return prev_plays_json

    def __eq__(self, other):
        return self.gameId == other.gameId \
               and self.playerIds == other.playerIds \
               and self.playerHands == other.playerHands \
               and self.turn == other.turn \
               and self.finishedPlayers == other.finishedPlayers \
               and self.previousPlays == other.previousPlays

def getRandomHands(numberOfPlayers):
        cards = []
        for rank in range(2, 15):
            for suit in range(0, 4):
                cards.append(Card(rank, suit))
        shuffle(cards)
        hands = []
        for player in range(0, numberOfPlayers):
            hand = []
            for i in range(0, 13):
                hand.append(cards.pop())
            hands.append(set(hand))
        return hands
