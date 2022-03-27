import math
from pydoc import doc
from .analyse import analyze

class Index:
    def __init__(self, db):
        self.db = db
      
    def index_document(self, document):
        if not 'title' in document:
            document['title'] = 'Untitled'
        if not 'content' in document:
            document['content'] = 'No content'
        for token in analyze(' '.join([document['content'], document['title'], document['lecturer']])):
            if not self.db.index.find_one({'token' : token}):

                self.db.index.insert_one({'token': token , 'documents' : [str(document['_id'])]})
            else:
                
                self.db.index.update_one({'token': token}, {'$addToSet' : {'documents' : str(document['_id'])}})
        
    def delete_index(self):
        return self.db.index.drop()
        
    def document_frequency(self, token):
        return len(self.index[token])
    
    def inverse_document_frequency(self, token):
        return math.log(len(self.index)/self.document_frequency(token))
    
    def results(self, query):
        return self.db.index.find({'token': query}, {'_id': False}) #{'$regex': f".*{query}.*"}