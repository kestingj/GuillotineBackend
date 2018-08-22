from flask import Flask, jsonify, request
from GameManager import GameManager
from Card import deserialize_card_list

app = Flask(__name__)
game_manager = GameManager()

@app.route('/games/<string:game_id>/<string:player_id>', methods=['GET'])
def get_player_state(game_id, player_id):
    player_state = game_manager.get_player_state(game_id, player_id)
    return jsonify(player_state)

# Returns the players hand after the play was made
@app.route('/games/<string:game_id>/<string:player_id>', methods=['PUT'])
def play(game_id, player_id):
    play_string = request.get_json()['play']
    play_set = deserialize_card_list(play_string)
    game_manager.play_hand(game_id, player_id, play_set)
    return jsonify(game_manager.get_player_state(game_id, player_id)['hand'])

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=20001)
