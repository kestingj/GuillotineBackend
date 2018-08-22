class Card(dict):

    def __init__(self, rank, suit):
        super().__init__()
        self['rank'] = rank
        self['suit'] = suit

    def __eq__(self, other):
        return self['rank'] == other['rank'] and self['suit'] == other['suit']

    def __hash__(self):
        return self['rank'] + self['suit'] * 4

    def __repr__(self):
        return self.representation()

    def __str__(self):
        return self.representation()

    def representation(self):
        return "{Suit: " + str(self['suit']) + ", Rank: " + str(self['rank']) + "}"

    def serialize(self):
        return str(self['suit']) + ':' + str(self['rank'])


def deserialize(card_string):
    split = card_string.split(':')
    return Card(int(split[0]), int(split[1]))


def deserialize_card_list(card_list_string):
    split = card_list_string.split(',')
    card_set = set()
    for card_string in split:
        card_set.add(deserialize(card_string))

    return card_set


def serialize_card_set(card_set):
    card_list_string = ''
    for card in card_set:
        if card_list_string != '':
            card_list_string += ','
        card_list_string += card.serialize()

    return card_list_string

