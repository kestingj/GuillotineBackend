import unittest
import random
from Card import *

class GameStateCheckpointDaoTest(unittest.TestCase):

    def testSerializeDeserializeCard(self):
        card = self.getRandCard()
        self.assertEqual(card, deserialize(card.serialize()))

    def testSerializeDeserializeCardList(self):
        cardSet = self.getRandCardSet()
        self.assertTrue(cardSet, deserialize_card_list(serialize_card_set(cardSet)))

    def getRandCard(self):
        return Card(random.randint(0, 4), random.randint(2, 14))

    def getRandCardSet(self):
        cardSet  = set()
        for i in range(10):
            cardSet.add(self.getRandCard())

        return cardSet


if __name__ == '__main__':
    unittest.main()