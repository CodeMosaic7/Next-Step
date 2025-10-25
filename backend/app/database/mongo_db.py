# upgrading the database to mongo db
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)

db = client["mydatabase"]

collection = db["mycollection"]

if __name__ == "__main__":      
    print("Connected to MongoDB Atlas.")