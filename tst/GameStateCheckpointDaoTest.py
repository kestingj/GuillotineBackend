import unittest

# To run this test a local instance of DDB must be running locally:
# cd ~/Downloads/dynamodb_local_latest/
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
class GameStateCheckpointDaoTest(unittest.TestCase):

    def testNewGame(self):
        pass

    def testCheckpointGame(self):
        pass

    def testLoadCheckpoint(self):
        pass

    def deleteGame(self):
        pass

if __name__ == '__main__':
    unittest.main()