from flask import Flask, jsonify, request
from GameManager import GameManager

app = Flask(__name__)
game_manager = GameManager()

@app.route('/games', methods=['POST'])
def startNewGame():
    player_ids = request.json['playerIds']
    starting_player = request.json['startingPlayer']
    game_manager.createNewGame(player_ids, starting_player)
    return jsonify({'gameCount' : len(game_manager.games)})

print "setup complete"

if __name__ == '__main__':
    app.run(debug=True, port=8080)
