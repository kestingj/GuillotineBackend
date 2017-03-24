class PlayerState:
    def __init__(self, playerId, hand, otherPlayerIds, previousPlays, turn):
        self.playerId = playerId
        self.hand = hand
        self.otherPlayerIds = otherPlayerIds
        self.previousPlays = previousPlays
        self.turn = turn

    def getPlayerId(self):
        return self.playerId

    def getHand(self):
        return self.hand

    def getOtherPlayerIds(self):
        return self.otherPlayerIds

    def getPreviousPlays(self):
        return self.previousPlays

    def getTurn(self):
        return self.turn
