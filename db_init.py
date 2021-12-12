from pymongo import MongoClient

host = "host.docker.internal" #"localhost"
client = MongoClient(f'mongodb://{host}:27017/')

db = client.test
