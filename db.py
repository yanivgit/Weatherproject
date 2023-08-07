from pymongo import MongoClient

def connect_to_db():
  #connect to the data base
  db_client = MongoClient('localhost', 27017)
  #create new db
  data= db_client.details
  #create storage in db
  storage= data.storage
  return storage
