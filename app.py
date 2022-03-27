from ast import mod
from threading import Lock
from flask import Flask, render_template, send_from_directory, make_response, request
from flask.wrappers import Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import db_init
from search_engine.indexer.index import Index
from search_engine.indexer.analyse import analyze
from bson.objectid import ObjectId
from bson import json_util
import json
import time
from dotenv import load_dotenv
import re
from search_engine.ranker.rank import document_frequency
import sys

load_dotenv()


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.

app = Flask(__name__)#
CORS(app, origins=['http://localhost:3000'])
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='http://localhost:3000')


thread = None
thread_lock = Lock()


@socketio.event
def connect():
    emit('connection', {'data': 'Connected to server'})

@socketio.event
def quick_search(query, offset):
    #start = time.time()
 
    #OR search ...
    
    results = list(db_init.db.index.find({'token': {'$in': list(map(lambda x: re.compile('{}'.format(x)),analyze(query)))}})) # monitor this performance
    
    docs = set([])
    for result in results:
        docs.update(list(map(lambda doc: ObjectId(doc) ,result['documents'])))
    
    if len(docs) <= 5:
        emit('results', {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': list(docs)}})), default=json_util.default), 'number_results': len(docs), 'search_type': '0', 'offset': offset})
    else:
        emit('results', {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': list(docs)[5 * (int(offset)): (5 * int(offset)) + 5]}})), default=json_util.default), 'number_results': len(docs), 'search_type': '0', 'offset': offset}) # 0 is quick search
        
    #print('Time taken for response' + str(time.time() - start), flush=True)

@socketio.on('search')
def search(query, offset):

    #AND search
    #print(offset, flush=True)
    tokens = analyze(query)
    results = list(db_init.db.index.find({"token" : {"$in" : tokens}})) # handy to cache

    if results:
        results = set.intersection(*list(set(result['documents']) for result  in results))
        results = list(map(lambda result: ObjectId(result), results))
        if len(results) <= 5:
            emit('full_results', {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': results}})), default=json_util.default), 'number_results': len(results), 'search_type': '1', 'offset': offset}) # 1 is full_search
        else:
            emit('full_results', {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': results[5 * (int(offset)): (5 * int(offset)) + 5]}})), default=json_util.default), 'number_results': len(results), 'search_type': '1', 'offset': offset}) # add pagination here ...
    else:
        emit('full_results', {'data' : json.dumps([])})

    #ADD OR search ...

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

    resp = make_response(send_from_directory(directory='',path='./notes/{}_{}/{}/{}/{}'.format(doc['module_code'], doc['module_name'], doc['lecturer'], doc['type'], doc['title'].split(' - ')[0].rstrip()), as_attachment=False))
    resp.headers['Access-Control-Allow-Origin'] = '*' #'http://localhost:3000/'
    return resp

@app.route('/search/advanced')
def advanced_search():
    query = request.values.get("query")
    offset = request.values.get("offset")
    
    
    module_code = json.loads(request.values.get('module'))
    lecturer = json.loads(request.values.get('lecturer')) 
    _type = json.loads(request.values.get('type'))
    
    tokens = analyze(query)
    results = list(db_init.db.index.find({"token" : {"$in" : tokens}})) # handy to cache
     # change hardcode
    filters = []

    
    if module_code != []:
        filters.append({'module_code': {'$in': module_code}})
    
    if lecturer != []:
        filters.append({'lecturer': {'$in': lecturer}})
    
    if _type != []:
        filters.append({'type': {'$in': _type}})
    
    #d = list(db_init.db.documents.find({"$and": [*filters]}))
    
    if results:
        results = set.intersection(*list(set(result['documents']) for result  in results))
        results = list(map(lambda result: ObjectId(result), results))
        
        #resp = list(db_init.db.documents.find({"$and" : [*filters, {'_id': {'$in': results[20 * (int(offset)): (20 * int(offset)) + 20]}}]}))
            #print(resp, flush=True)
        #return {'data': json.dumps(resp, default=json_util.default), 'number_results': num_results, 'search_type': '1', 'offset': offset} # add pagination here ...

        resp = list(db_init.db.documents.find({"$and": [*filters, {'_id': {'$in': results}}]}))
            
        return {'data': json.dumps(resp, default=json_util.default), 'number_results': len(resp), 'search_type': '1', 'offset': offset} # 1 is full_search
        '''
        if len(results) <= 20:
            resp = list(db_init.db.documents.find({"$and": [*filters, {'_id': {'$in': results}}]}))
            
            return {'data': json.dumps(resp, default=json_util.default), 'number_results': len(resp), 'search_type': '1', 'offset': offset} # 1 is full_search
        else:
            #,  'lecturer': lecturer, 'module_code': module_code, 'type': _type
            #q = {'_id': {'$in': results[5 * (int(offset)): (5 * int(offset)) + 5]}}.update({'module_code':module_code, 'lecturer': lecturer, 'type': _type})
            num_results = len(list(db_init.db.documents.find({"$and" : [*filters, {'_id': {'$in': results}}]})))
            
            resp = list(db_init.db.documents.find({"$and" : [*filters, {'_id': {'$in': results[20 * (int(offset)): (20 * int(offset)) + 20]}}]}))
            #print(resp, flush=True)
            return {'data': json.dumps(resp, default=json_util.default), 'number_results': num_results, 'search_type': '1', 'offset': offset} # add pagination here ...
        '''
    else:
        return {'data' : []}

    #return {'data': json.dumps(list(db_init.db.documents.find({'_id': {'$in': list(results)[5 * (int(offset)): (5 * int(offset)) + 5]}})), default=json_util.default), 'number_results': len(results), 'search_type': '0', 'offset': 1} # 0 is quick search 
    
@app.route('/test')
def test_db():
   
   
    return #{'data': json.dumps(list(db_init.db.documents.find({"$and": [*filters]})), default=json_util.default)}


if __name__ == '__main__':
    socketio.run(app)
    #app.run()
