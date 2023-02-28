from elasticsearch import Elasticsearch
import os

'''

Go to elasticsearch in C:// and activate elasticsearch.bat to run server when running locally

'''
es = Elasticsearch(os.environ.get("ES")) 


es.options(ignore_status=[400,404]).indices.delete(index='level_3')

import sys

sys.path.append("..")

import db_init


docs = db_init.db.documents.find({})

for i, doc in enumerate(docs):
    doc['doc_id'] = str(doc["_id"])
    doc.pop('_id')
    
    resp = es.index(index="level_3", id=i+1, document=doc)
    print(resp['result'])

resp = es.get(index="level_3", id=1)
print(resp['_source'])

es.indices.refresh(index="level_3")

resp = es.get(index="level_3", id=1)
print(resp['_source'])

#resp = es.search(index="test-index", query={"match": {"transcript.text": "backpropagation"}})
#print("Got %d Hits:" % resp['hits']['total']['value'])

'''

Index all cuts so that jumps can be made to lecture video.

Plug into frontend / API


'''
