from flask import Flask, jsonify, request
from GameManager import GameManager
from Card import Card

app = Flask(__name__)
game_manager = GameManager()

@app.route('/games', methods=['POST'])
def start_new_game():
    player_ids = request.get_json()['playerIds']
    starting_player = request.get_json()['startingPlayer']
    game_id = request.get_json()['gameId']
    game_manager.create_new_game(game_id, player_ids, starting_player)

@app.route('/games/<string:game_id>/<string:player_id>', methods=['GET'])
def get_player_state(game_id, player_id):
    player_state = game_manager.get_player_state(game_id, player_id)
    return jsonify(player_state)

# Returns the players hand after the play was made
@app.route('/games/<string:game_id>/<string:player_id>', methods=['PUT', 'DELETE'])
def play(game_id, player_id):
    if request.method == 'PUT':
        play_list = request.get_json()['play']
        play_set = set()
        for card in play_list:
            play_set.add(Card(card['rank'], card['suit']))
        game_manager.play_hand(game_id, player_id, play_set)
        return jsonify(game_manager.get_player_state(game_id, player_id)['hand'])
    elif request.method == 'DELETE':
        game_manager.ack_finished_game(game_id, player_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
