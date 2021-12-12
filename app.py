from threading import Lock
from flask import Flask, render_template, send_from_directory, make_response
from flask.wrappers import Response
from flask_socketio import SocketIO, emit
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
load_dotenv()


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.

app = Flask(__name__)
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

@app.route('/pdfNotes/<path:filename>')
def get_pdf_notes(filename):
    resp = make_response(send_from_directory('./notes/', filename, as_attachment=False))
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return resp


if __name__ == '__main__':
    #socketio.run(app)
    app.run()
