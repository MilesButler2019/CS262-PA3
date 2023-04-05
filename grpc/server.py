from concurrent import futures
import grpc
import chat_pb2
import chat_pb2_grpc
import time
import threading
from collections import defaultdict
import datetime
import argparse 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://milesbutler:mu7PhtTsqAxvgFUV@cluster0.6ax79dz.mongodb.net/test"
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
except AttributeError:
    pass 
#Weird shit going on within my version
db = client['messages']
collection = db['test']

class Listener(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        #Accounts to store username:password for users
        self.accounts = {}
        #Inbocx to store messages
        self.all_inbox = {}
        #List to store logged in users
        self.user_sessions = []


    def getUsers(self,request,context):
        #Returns a stream of users
        for i in self.accounts.keys():
            creds = chat_pb2.Credentials()
            creds.username = i
            time.sleep(.1)
            yield creds

    def send_data_to_db(self,data,database,table):
        try:
            db = client[database]
            collection = db[table]
            collection.insert_one(data)
        except:
            return "Error with DB"
        
    def search_db(self,data,database,table):
        try:
            db = client[database]
            collection = db[table]
            result = collection.find_one(data)
            return result
        
        except:
            return "Error with DB"
        
    def update_db_row(self,filter,data,database,table):
        try:
            db = client[database]
            collection = db[table]

            update = {"$set": data}
            result = collection.update_one(filter, update)
            return result
        except:
            return "Error with DB"


    def CreateAccount(self, request, context):

        # Creates account and inbox for new user and logs them in
        res = self.search_db({"username":request.username},database='messages',table='auth')
        print(res)
        if res != None:
        # if request.username in self.accounts:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='user name already exists')
            return reply
        else:
            try:
                self.accounts[request.username] = request.password
                self.all_inbox[request.username] = defaultdict(list)
                for i in range(1):
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    self.all_inbox[request.username]["Server"] = []
                    default_message = chat_pb2.Message(content="Welcome say something nice",sent_time=formatted_datetime,src = "Server",dest=request.username)
                    self.all_inbox[request.username]["Server"].append(default_message)

                self.user_sessions.append(request.username)
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Account Created Sucsessfully')
                print(request.username,"has made an account")
                self.send_data_to_db({"username":request.username,"password":request.password,"loggedIn":True},database='messages',table='auth')
                try:
                    self.send_data_to_db({"sender_username":"Server","reciver_username" : request.username,"time" : formatted_datetime, "content" : "Welcome to the server!"},database='messages',table='message_table')
                    return reply
                except:
                    reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Error Creating Account, Try Again')
                    return reply
                
            except:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Error Creating Account, Try Again')
                return reply

    def LogIn(self, request, context):
        #  try and die login methd for checking account creditinals 
        try:
            res = self.search_db({"username":request.username,"password":request.password},database='messages',table='auth')
            if res is not None:
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Login Success')
                try:
                    res = self.update_db_row({"username":request.username,"password":request.password},data={"loggedIn":True},database='messages',table='auth')
                except:
                    reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Error setting user active')
                    return reply
                print(request.username,"is logged in")
                return reply

            else:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Incorrect username or password')
                return reply
        except:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Database Error')
            return reply
        #     if self.accounts[request.username] ==  request.password:
        #         self.user_sessions.append( request.username)
        #         reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Login Success')
        #         print(request.username,"is logged in")
        #         return reply
        #     else:
        #         reply =  chat_pb2.AccountStatus(AccountStatus=0,message='bad password')
        #         return reply
        # except:
        #     reply =  chat_pb2.AccountStatus(AccountStatus=0,message='incorrect username')
        #     return reply

    def LogOut(self, request, context):
        #This logs a user out
        try:
            self.update_db_row(filter={"username":request.username},data={"loggedIn":False},database="messages",table='auth')
            reply = chat_pb2.AccountStatus(AccountStatus=1,message="You are sucsessfully logged out")
            # print(self.user_sessions)
            print(request.username,'is logged out')
            # self.user_sessions.remove(request.username)
            return reply
        except:
            reply = chat_pb2.AccountStatus(AccountStatus=0,message="Error logging out")
            return reply


    def DeleteAccount(self,request,context):
        #Deletes a users account
        try:
            if request.username in self.accounts and request.username in self.user_sessions:
                del self.accounts[request.username]
                self.user_sessions.remove(request.username)
                reply =  chat_pb2.AccountStatus(AccountStatus=1,message='Account deleted successfully')
                return reply
            else:
                reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Account not Found')
                return reply
        except:
            reply =  chat_pb2.AccountStatus(AccountStatus=0,message='Error in your request')
            return reply


    
    
    def getInbox(self, request, context):
        #This returns a stram of messages
        if request.username in self.accounts:
            for i,v in self.all_inbox[request.username ].items():
                for mes in self.all_inbox[request.username ][i]:
                    time.sleep(.1)
                    yield mes
        else:
            reply = chat_pb2.Message(content="User not found",sent_time="today",dest = request.dest,src="server")
            return reply




    def CheckUserOnline(self,request, context):
        #This verifies is a user is online or exists
        if request.username in self.user_sessions:
            reply = chat_pb2.AccountStatus(AccountStatus=1, message="User online")
            return reply
        elif request.username not in self.accounts:
            reply = chat_pb2.AccountStatus(AccountStatus=0, message="User doesn't exist")
            return reply
        else:
            reply = chat_pb2.AccountStatus(AccountStatus=0, message="User Offline")
            return reply

    def ChatStream(self, request_iterator, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        # For every client a infinite loop starts (in gRPC's own managed thread)    

        while True:
            last_index = len(self.all_inbox[request_iterator.src][request_iterator.dest])

            # Check if there are any new messages
            while len(self.all_inbox[request_iterator.src][request_iterator.dest]) > last_index:
                n = self.all_inbox[request_iterator.src][request_iterator.dest][last_index]
                last_index += 1
                yield n
                

        
    def SendChat(self, request: chat_pb2.Message(), context):
        """
        This method is called when a clients sends a Message to the server.

        :param request:
        :param context:
        :return:
        """
        try:
            print("[{}] {}".format(request.src, request.content))
            self.chat_thread = request.src
            self.all_inbox[request.dest][request.src].append(request)
            return chat_pb2.MessageStatus(message_status=1,message="Message sent sucsessfully")
        except:
            return chat_pb2.MessageStatus(message_status=0,message="Error Sending Message")

   
    def CheckHealth(self, HealthCheckResponse, context):
        status = chat_pb2.HealthCheckResponse.SERVING
        return chat_pb2.HealthCheckResponse(status=status)
        
        
#method to run server
def serve(port):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  chat_pb2_grpc.add_ChatServiceServicer_to_server(
      Listener(), server)
  server.add_insecure_port('localhost:'+str(port))
  server.start()
  server.wait_for_termination()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat Server')
    parser.add_argument('--p', type=int, help='Enter a Port number')
    args = parser.parse_args()
    serve(args.p)