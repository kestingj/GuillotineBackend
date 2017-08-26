
# A PlayerState includes all player-specific game state information that will be passed back to that player
class PlayerState:
    def __init__(self, playerId, hand, playersToCardsInHand, previousPlays, turn):
        self.playerId = playerId
        self.hand = hand
        self.playersToCardsInHand = playersToCardsInHand
        self.previousPlays = previousPlays
        self.turn = turn

    def getPlayerId(self):
        return self.playerId

    def getHand(self):
        return self.hand

    def getPlayersToCardsInHand(self):
        return self.playersToCardsInHand

    def getPreviousPlays(self):
        return self.previousPlays

    def getTurn(self):
        return self.turn
