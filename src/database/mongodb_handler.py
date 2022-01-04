import os
import sys
import pymongo
import json

from pymongo import mongo_client


class MongoDB(object):

    def __init__(self, host='localhost', maxPoolSize=50, port=28017):
        self.host = host
        self.port = port
        self.maxPoolsize = maxPoolSize
        # having issue with this way of creating client due to authentication
        self.client = pymongo.MongoClient(host=self.host, port=self.port,
                                  maxPoolSize=self.maxPoolsize)
        
class MongoDBHandler:
    mongodb_obj = None
    operations_obj = None
    minsert_objs = {}


    @staticmethod
    def init_mongodb():
        if MongoDBHandler.is_mongodb_connection_established() != True:
            MongoDBHandler.mongodb_obj = MongoDB(host="mongodb://rootuser:rootpass@127.0.0.1:28017")
            print("MongoDB connection established!")
            MongoDBHandler.init_operations()
            MongoDBHandler.init_minsert_objs()
        else:
            print("MongoDB connection already established!")

    @staticmethod
    def is_mongodb_connection_established():
        if MongoDBHandler.mongodb_obj != None: 
            return True
        return False

    @staticmethod
    def init_operations():
        MongoDBHandler.operations_obj = Operations(instance=MongoDBHandler.mongodb_obj) 

    @staticmethod
    def print_all_databases():
        if MongoDBHandler.operations_obj != None:
            print(MongoDBHandler.operations_obj.getAllDatabase())
        else:
            print("Operation class instance not initialized yet!")
    
    @staticmethod
    def init_minsert_objs():
        databases = []
        if MongoDBHandler.operations_obj != None:
            collections = []
            coll_dict = {}
            databases = MongoDBHandler.operations_obj.getAllDatabase()
            for database in databases:
                collections = MongoDBHandler.operations_obj.mongodb.client[database].list_collection_names()
                print("Collections of ", database, ": ", collections)
                for collection in collections:
                    # minsert_obj = Minsert(_instance=MongoDBHandler.mongodb_obj, dbName=database, collectionName=collection)
                    coll_dict[collection] = Minsert(_instance=MongoDBHandler.mongodb_obj, dbName=database, collectionName=collection)
                MongoDBHandler.minsert_objs[database] = coll_dict
            # print(MongoDBHandler.minsert_objs["smarthome"]["sensors_log"])

    @staticmethod
    def insert_one(input_doc, db_name, coll_name):
        if MongoDBHandler.minsert_objs[db_name][coll_name].insert_one(input_doc):
            return True
        else:
            return False

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