import os
import sys
import pymongo
import json


class MongoDB(object):

    def __init__(self, host='localhost', maxPoolSize=50, port=28017):
        self.host = host
        self.port = port
        self.maxPoolsize = maxPoolSize
        # having issue with this way of creating client due to authentication
        self.client = pymongo.MongoClient(host=self.host, port=self.port,
                                  maxPoolSize=self.maxPoolsize)


class Operations(object):

    def __init__(self, instance=None):
        self.mongodb = instance

    def getAllDatabase(self):
        """
        Takes an Instance and return all Lists of Databases
        :return: List of all Databases found
        """
        return self.mongodb.client.list_database_names()

class Minsert(object):

    def __init__(self, _instance=None, dbName=None, collectionName=None):
        self.mongodb = _instance
        self.dbName = dbName
        self.collectionName = collectionName

    def insert_one(self, record):
        """
        :param record: Json
        :return: Bool
        """
        try:
            self.mongodb.client[self.dbName][self.collectionName].insert_one(record)
            return True
        except Exception as e:
            return False
        
    def insert_pandas_df(self, df=None):
        pass

if __name__ == "__main__":
    #myclient = pymongo.MongoClient("mongodb://rootuser:rootpass@127.0.0.1:28017")
    _helper = MongoDB(host="mongodb://rootuser:rootpass@127.0.0.1:28017")
    _ops = Operations(instance=_helper)
    _insert = Minsert(_instance=_helper, dbName="admin", collectionName="mynewcollection")
    with open("data.json") as f:
        file_data = json.load(f)
        print(file_data)
        if (_insert.insert_one(file_data)): 
            print("Insert was successful")
        else:
            print("Insert was not successful")
    print(_ops.getAllDatabase())
   
    #mydb = myclient["admin"]
    #print(myclient.list_database_names())