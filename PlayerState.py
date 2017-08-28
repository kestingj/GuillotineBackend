
# A PlayerState includes all player-specific game state information that will be passed back to that player
class PlayerState(dict):
    def __init__(self, playerId, hand, playersToCardsInHand, previousPlays, turn):
        super().__init__()
        self['playerId'] = playerId
        self['hand'] = list(hand)
        self['playersToCardsInHand'] = playersToCardsInHand
        self['previousPlays'] = previousPlays
        self['turn'] = turn
