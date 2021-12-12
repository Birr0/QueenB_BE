#import os.path
#import requests
import json
from indexer import index, timing, analyse
from scraper.transcript_generator_ms_streams.get_transcript import MsStreams
from ..db_init import db_init


#if __name__ == '__main__':
    # this will only download the xml dump if you don't have a copy already;
    # just delete the file if you want a fresh copy
with open('test_data.json', 'r') as f:
    documents = json.load(f)

#_index = index_documents(documents)#, index.Index())
#for document in documents:
#    index.Index(db = db).index_document(''.join([document['title'], document['content']]))
#print(_index)
URLS = ["https://web.microsoftstream.com/video/cff896a6-03db-4e01-953a-c724a4ed4141", "https://web.microsoftstream.com/video/60a76609-f61a-42d6-aa20-77431b931344"]
MsStreams().download_transcripts(db = db_init.db, resource_urls=URLS)
print(f'Index contains {len(documents)} documents')