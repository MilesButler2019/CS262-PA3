import unittest
import chat_pb2
import chat_pb2_grpc
import grpc
import new_client
from unittest.mock import patch
from io import StringIO 
import sys
import signal
import uuid
import time

#Client Tests

test_account_1 = "jay"
test_account_2 = "def"




class TestCreateReg(unittest.TestCase):
    @patch('builtins.input', side_effect=["2",test_account_1,"test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn('Account Created Sucsessfully\n', str(sys.stdout.getvalue()))

class TestLoginBasic(unittest.TestCase):
    @patch('builtins.input', side_effect=["1",test_account_1,"test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn('Login Success\n', str(sys.stdout.getvalue()))

class TestLoginBasicWrongPassword(unittest.TestCase):
    @patch('builtins.input', side_effect=["1",test_account_1,"test1"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn('bad password\n', str(sys.stdout.getvalue()))

class TestLoginBasicWrongUserName(unittest.TestCase):
    @patch('builtins.input', side_effect=["1","blah","test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn('incorrect username\n', str(sys.stdout.getvalue()))     

class TestLogout(unittest.TestCase):
    @patch('builtins.input', side_effect=["1",test_account_1,"test",'logout'])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        try:
            new_client.main()
        except: 
            self.assertIn('You are sucsessfully logged out\n', str(sys.stdout.getvalue()))

class TestMakeDuplicate(unittest.TestCase):
    @patch('builtins.input', side_effect=["2",test_account_1,"test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        try:
            new_client.main()
        except: 
            self.assertIn('user name already exists\n', str(sys.stdout.getvalue()))



class TestRemoveAccountWrongUsername(unittest.TestCase):
    @patch('builtins.input', side_effect=["1",test_account_1,"test","del","y","blah","test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn('Account not Found\n', str(sys.stdout.getvalue()))

class TestRemoveAccountWrongPassword(unittest.TestCase):
    @patch('builtins.input', side_effect=["1",test_account_1,"test","del","y",test_account_1,"test1"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn('Account not Found\n', str(sys.stdout.getvalue()))

class TestRemoveFinallyAccount(unittest.TestCase):
    @patch('builtins.input', side_effect=["1",test_account_1,"test","del","y",test_account_1,"test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn('Account deleted successfully\n', str(sys.stdout.getvalue()))

class TestRemoveFinallyAccountLogin(unittest.TestCase):
    #Tests logging into delted account
    @patch('builtins.input', side_effect=["1",test_account_1,"test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn('incorrect username\n', str(sys.stdout.getvalue()))

class TestInboxServerMessage(unittest.TestCase):
    #Tests empty inbox
    @patch('builtins.input', side_effect=["2",test_account_2,"test",'inbox'])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn("Welcome say something nice", str(sys.stdout.getvalue()))



class TestInboxDummyUser(unittest.TestCase):
    #Creates a dummy user to send messages
    @patch('builtins.input', side_effect=["2",'bard',"test"])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            pass


class TestMessageNonExistUser(unittest.TestCase):
    #Tests message from user that doesnt exist
    @patch('builtins.input', side_effect=["1",test_account_2,"test",'msg','chat'])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn("User doesn't exist", str(sys.stdout.getvalue()))

class TestMessageBasic(unittest.TestCase):
    #This just sends a message to be tested in next testcase
    @patch('builtins.input', side_effect=["1",test_account_2,"test",'msg','bard','sup bro','exit'])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertEqual(1,1)
            # pass

class TestMessageBasicRecieveOnDemand(unittest.TestCase):
    #Test that message has NOT been recieved
    @patch('builtins.input', side_effect=["1","bard",'test',"sup bro",'inbox'])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertNotIn("sup bro", str(sys.stdout.getvalue()))

class TestMessageBasicRecieveOnDemand(unittest.TestCase):
    #Test that message has HAS been recieved
    @patch('builtins.input', side_effect=["1","bard",'test',"sup bro",'inbox'])
    def runTest(self, input_mock):
        #Wait 60 seconds to recieve messages
        time.sleep(60)
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn("sup bro", str(sys.stdout.getvalue()))

class TestListingUsers (unittest.TestCase):
    #Test that message has HAS been recieved
    @patch('builtins.input', side_effect=["1","bard","test",'ls'])
    def runTest(self, input_mock):
        #Stores Command line output
        sys.stdout = StringIO()
        #Need to use try expect since the programs erros out as it is epecting more user inputs but gets a iteration error
        try:
            new_client.main()
        except: 
            self.assertIn("bard def", str(sys.stdout.getvalue()))
    
if __name__ == '__main__':
    unittest.main()