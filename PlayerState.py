class PlayerState:
    def __init__(self, playerId, hand, cardsInHands, previousPlays, turn):
        self.playerId = playerId
        self.hand = hand
        self.playerIds = playerIds
        self.previousPlays = previousPlays
        self.turn = turn

    def getPlayerId(self):
        return self.playerId

    def getHand(self):
        return self.hand

    def playerIds(self):
        return self.playerIds

    def getPreviousPlays(self):
        return self.previousPlays

    def getTurn(self):
        return self.turn
