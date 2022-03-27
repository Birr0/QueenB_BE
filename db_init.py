from pymongo import MongoClient

host ="localhost" #"host.docker.internal" #
client = MongoClient(f'mongodb://{host}:27017/')

db = client.test
