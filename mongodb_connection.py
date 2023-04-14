import time

import pymongo

class MondoBDConnection():

    collection=None

    def get_group_name_collection(self):
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["shivamdb"]
        self.collection = db["group_name_data"]
        return  self.collection



        #return collection/

    def get_group_txt_export_collection(self):
        client = pymongo.MongoClient("mongodb://localhost:27017")

        db = client["shivamdb"]
        self.collection = db["group_txt_export"]
        return self.collection



    def insert_data_into_database(self,data):
        #dictionary = {"symbol": "NSE:NIFTY50-INDEX", "ltp": 300, "time": datetime.now()}
        self.collection.insert_one(data)


if __name__ == '__main__':


    #print(db.getLastInsertedDocument.find())

    # dictionary_list=\
    #     [{"symbol":"NSE:NIFTY50-INDEX","ltp":300,"time":start_time},
    #      {"symbol":"NSE:NIFTY50-INDEX","ltp":300},
    #      {"symbol":"NSE:NIFTY50-INDEX","ltp":300},
    #      {"symbol":"NSE:NIFTY50-INDEX","ltp":300}]
    from datetime import datetime

    #record=collection.find_one({"symbol": "NSE:NIFTY50-INDEX"},sort=[('time', pymongo.DESCENDING)])
    #record=db.getLastInsertedDocument.find({}).sort({"_id": -1}).limit(1);
    #print(record)