from threading import Lock
from flask import Flask, send_from_directory, make_response, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import db_init
#from search_engine.indexer.index import Index
#from search_engine.indexer.analyse import analyze
from bson.objectid import ObjectId
from bson import json_util
import json
import time
from dotenv import load_dotenv
import re
#from search_engine.ranker.rank import document_frequency

from search_engine.es_test import es 


load_dotenv()


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.

app = Flask(__name__)#
CORS(app, origins=['http://localhost:3000'])
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins=['http://localhost:3000'])

thread = None
thread_lock = Lock()


@socketio.event
def connect():
    emit('connection', {'data': 'Connected to server'})

@socketio.event
def quick_search(query, offset):
    #start = time.time()
 
    #OR search ...
    
    '''results = list(db_init.db.index.find({'token': {'$in': list(map(lambda x: re.compile('{}'.format(x)), query))}})) # monitor this performance # analyze(query)
    
    docs = set([])
    for result in results:
        docs.update(list(map(lambda doc: ObjectId(doc) ,result['documents'])))
    '''
    body = {
        "_source": {
            "includes": [ "*" ],
            #"excludes": [ "transcript" ]
        },
        "query": {
            "match": {
            
            "content": {
                "query": query,
                "fuzziness": "AUTO"
            },
            }
        } 
    }

    return emit('results', {'data': json.loads(json_util.dumps(es.search(index="level_3", body = body))), 'number_results': 1, 'search_type': '1', 'offset': offset}) # 1 is full_search


    '''if len(docs) <= 5:
        emit('results', {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': list(docs)}})), default=json_util.default), 'number_results': len(docs), 'search_type': '0', 'offset': offset})
    else:
        emit('results', {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': list(docs)[5 * (int(offset)): (5 * int(offset)) + 5]}})), default=json_util.default), 'number_results': len(docs), 'search_type': '0', 'offset': offset}) # 0 is quick search'''
        
    #print('Time taken for response' + str(time.time() - start), flush=True)
#results = list(db_init.db.index.find({'token': {'$in': list(map(lambda x: re.compile('{}'.format(x)), query))}})) # monitor this performance
@socketio.on('search')
def search(query, offset):

    #AND search
    #print(offset, flush=True)
    '''tokens = query #analyze(query)
    results = list(db_init.db.index.find({"token" : {"$in" : tokens}}))''' # handy to cache
#
    body = {
        "_source": {
            "includes": [ "*" ],
            #"excludes": [ "transcript" ]
        },
        "query": {
            "match": {
            
            "content": {
                "query": query,
                "fuzziness": "AUTO"
            },
            }
        } 
    }
    
    return emit('full_results', {'data': json.loads(json_util.dumps(es.search(index="level_3", body = body))), 'number_results': 1, 'search_type': '1', 'offset': offset}) # 1 is full_search

    '''if results:
        results = set.intersection(*list(set(result['documents']) for result  in results))
        results = list(map(lambda result: ObjectId(result), results))
        if len(results) <= 5:
            emit('full_results', {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': results}})), default=json_util.default), 'number_results': len(results), 'search_type': '1', 'offset': offset}) # 1 is full_search
        else:
            emit('full_results', {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': results[5 * (int(offset)): (5 * int(offset)) + 5]}})), default=json_util.default), 'number_results': len(results), 'search_type': '1', 'offset': offset}) # add pagination here ...
    else:
        emit('full_results', {'data' : json.dumps([])})'''

    

@socketio.on('get_resource')
def get_resource(resource_id):
    result = db_init.db.documents.find_one({'_id': ObjectId(str(resource_id))})
 
    if result:
        if result['type'] == 'video':
            emit('resource_response', json.dumps(result, default=json_util.default))
        else:
            emit('resource_response', json.dumps({'message': 'No resource found'}))

# fix paths...

@app.route('/pdfNotes/<path:docId>')
def get_pdf_notes(docId):

    doc = db_init.db.documents.find_one({'_id': ObjectId(str(docId))})

    resp = make_response(send_from_directory(directory='',path='./notes/{}_{}/{}/{}/{}'.format(doc['module_code'], doc['module_name'], doc['lecturer'], doc['type'], doc['title'].split(".pdf")[0].strip() + ".pdf"), as_attachment=False))
    resp.headers['Access-Control-Allow-Origin'] = '*' #'http://localhost:3000/'
    return resp


@app.route('/search/advanced')
def advanced_search():
    query = request.values.get("query")
    offset = request.values.get("offset")
    
    module_codes = json.loads(request.values.get('module'))
    lecturers = json.loads(request.values.get('lecturer')) 
    _types = json.loads(request.values.get('type'))
    
    body = {
        "query": {
           "bool": { 
                "must": [
                    { "match": {
                        "content": {
                            "query": query,
                            "fuzziness": "AUTO"
                        },
                }},
                ],
                "should":[]
                
           }
        }
    }

    if module_codes:
        for code in module_codes:
            body["query"]["bool"]["must"].append({"match":{"module_code":code}})
    if lecturers:
        for lecturer in lecturers:
            body["query"]["bool"]["must"].append({"match":{"lecturer": lecturer}})
    if _types:
        for _type in _types:
            body["query"]["bool"]["should"].append({"match":{"type": _type}})


    return json.loads(json_util.dumps(es.search(index="level_3", body = body)))#json.dumps({'data': resp}) 
    #{'data' : resp} #resp
    
    #return {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': list(results)[5 * (int(offset)): (5 * int(offset)) + 5]}})), default=json_util.default), 'number_results': len(results), 'search_type': '0', 'offset': 1} # 0 is quick search 
    

if __name__ == '__main__':
    socketio.run(app)
    app.run()
