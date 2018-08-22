
# A PlayerState includes all player-specific game state information that will be passed back to that player
class PlayerState(dict):
    def __init__(self, player_id, hand, players_to_cards_in_hand, previous_plays, turn, turn_order):
        super().__init__()
        self['playerId'] = player_id
        self['hand'] = list(hand)
        self['playersToCardsInHand'] = players_to_cards_in_hand
        self['previousPlays'] = previous_plays
        self['turn'] = turn
        self['turnOrder'] = turn_order
