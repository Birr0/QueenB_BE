import math
import re

## not fast enough in realtime ...
def document_frequency(doc, token): # returns how frequently a token appears in the full text of a doc
    full_text = ' '.join([doc['title'], doc['lecturer'], doc['description'], doc['content']])
    print(full_text, flush=True)
    pattern = re.compile(r'\b{}\b'.format(token), re.I)
    return len(pattern.findall(full_text))
