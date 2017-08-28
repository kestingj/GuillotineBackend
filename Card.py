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
