

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict
# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://milesbutler:mu7PhtTsqAxvgFUV@cluster0.6ax79dz.mongodb.net/test"
# Set the Stable API version when creating a new client

client = MongoClient(uri, server_api=ServerApi('1'))
                          
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

#DataAPI key aY0HWMU2a4g2uQURg4CBVhsmY9S3kMfyahqIYbGHXZGlMbpSkKT9tlV1YKwrcbSl


# db = client['messages']

# collection = db['mycollection']

# document = {"name": "John", "age": 25, "city": "New York"}
# try:
# # Insert the document into the collection
#     collection.insert_one(document)
# except:
#     print("error")

# client.close()
def send_data_to_db(data,database,table):
        # try:
        db = client[database]
        collection = db[table]
        collection.insert_one(data)
        # except:
            # return "Error with DB"
    
def update_db_row(filter,data,database,table):
    # try:
    db = client[database]
    collection = db[table]

    update = {"$set": data}
    result = collection.update_one(filter, update)
    return result
    # except:
        # return "Error with DB"
    
def search_db(data,database,table):
        try:
            db = client[database]
            collection = db[table]
            result = collection.find_one(data)
            return result
        
        except:
            return "Error with DB"
        

res = update_db_row({"reciver_username":"test"},data={'read':True},database='messages',table='auth')
    
print(res)
# all_inbox["James"]["server"].append("hi")
# print(all_inbox["James"]["server"] =

# print(send_data_to_db({"sender_username":"James","reciver_username" : "James","time" : "Now", "content" : "Welcome to the server!"},database='messages',table='message_table'))