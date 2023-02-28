#from search_engine.indexer import index#, timing, analyse
import db_init
#from scraper.transcript_generator_ms_streams.get_transcript import MsStreams

from bson.objectid import ObjectId

from dotenv import load_dotenv

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


load_dotenv()

from os import listdir
from os.path import isfile, join

#db_init.db.documents.drop()


speakers = list(db_init.client['birde']['speakers'].find())

audio_content = list(db_init.client['birde']['audio_content'].find({"speaker_ids":['7b23ae69-2a59-47d4-b12b-bd0e380c0259']}))

for i, audio in enumerate(audio_content):
    data={
        'title': audio["title"],
        'module_code': "PHY3001", 
        'module_name': "Quantum Mechanics & Special Relativity",
        'lecturer': "Prof Ian Williams",
        "transcript" : "",
        "segments": [], 
        "url": audio["url"], 
        "type":"video",
        "publish_date": audio["publish_date"]
        }

    if type(audio["transcript"]) == dict:
        data["content"] = audio["transcript"]['text']
        data["video_data"] = [{
                        "start": segment['start'],
                        "end": segment["end"],
                        "text": segment["text"]}
                        for segment in audio['transcript']['segments']
                        ]

    '''if "segments" in audio:
        for segment in audio["segments"]:
            data["segments"].append({
                "start": segment['start'],
                "end": segment["end"],
                "text": segment["text"]
            })
        data['transcript'] = " ".join(segment['text'] for segment in data["segments"])
    elif audio["transcript"] != "":'''
        #print("")#audio["transcript"])
        #data['transcript'] = " ".join([segment['text'] for segment in audio["transcript"]])
        #data['segments'] = [{'start' : segment['start'], 'end':  segment['end'], 'text': segment['text']} for segment in audio["transcript"]]
    #print(data)
    #db_init.db.documents.insert_one(
    #    data
    #)
        

def create_documents(files, path, doc_type, lecturer, module):
    #files = [f for f in listdir("./notes") if isfile(join("./notes", f))]
    ids = []
    module = module.split('_')
    for file in files:
        page_no = 1
        for page in extract_pages(f'{path}/{file}'):
            print(file + 'Page is number ' + str(page_no))
            
            page_content = ""
            
            for element in page:
                
                if isinstance(element, LTTextContainer):
                    ''''''
                    page_content += f" {element.get_text().strip()}"
                
                    #ids.append(x.inserted_id)

            x = db_init.db.documents.insert_one({
                    'title': '{} - Page {}'.format(file, page_no),
                    #'filename': '{}'.format(file),
                    'type': doc_type,
                    'content': page_content,
                    'lecturer' : lecturer,
                    'module_code': module[0],
                    'module_name' : module[1],
                })
            ids.append(x.inserted_id)
    
            page_no += 1
    return ids


#compile_index()

# need to delete old documents ... Think about pipeline as well

#db_init.db.documents.drop()
#db_init.db.index.drop()



'''modules = [f for f in listdir("./notes")]
for module in modules:
    resources = (listdir(f'./notes/{module}'))
    print(resources)
    for resource in resources: # resources = 'assignments', 'exam_papers' or 'lecturer_name'
        #if resource == 'assignments':
            #print(listdir(f'./notes/{module}/assignments'))
            #create_documents(listdir(f'./notes/{module}/assignments'),f'./notes/{module}/assignments' ,'assignment', '' ,module)
        if resource == 'exam paper':
            create_documents(listdir(f'./notes/{module}/exam paper'), f'./notes/{module}/exam paper','exam paper', '' ,module)
        
        else:
            docs = (listdir(f'./notes/{module}/{resource}'))
            for k in docs:
                if k == 'notes':
                    create_documents(listdir(f'./notes/{module}/{resource}/notes'),f'./notes/{module}/{resource}/notes', 'notes', resource, module)
                if k == 'slides':
                    create_documents(listdir(f'./notes/{module}/{resource}/slides'),f'./notes/{module}/{resource}/slides', 'slides', resource, module)
                #if k == 'transcripts':
                    #with open(f'./notes/{module}/{resource}/transcripts/transcripts.json') as f:
                        #transcripts = json.load(f)
                        #modules = module.split('_')
                        #MsStreams().download_transcripts(db = db_init.db, gd_path="scraper/transcript_generator_ms_streams/geckodriver/geckodriver.exe", resource_urls=transcripts, data={'module_code': modules[0], 'module_name': modules[1], 'lecturer': resource})
                else:
                    pass'''
        

def compile_index(index):
    index.Index(db = db_init.db).delete_index()
    for document in db_init.db.documents.find({}):
        ID = document['_id']
        print(ID)
        print(f'Adding document {ID}')
        index.Index(db = db_init.db).index_document(document)


'''docs = db_init.db.documents.find({'lecturer':'Prof Gianluca Sarri'})
for doc in docs:
    print(doc)'''
#for doc in docs:
    #doc = db_init.db.documents.find_one({'_id': id})
    
    #print('adding {}'.format(doc['_id']))
    
    #index.Index(db=db_init.db).index_document(doc)


#x = db_init.db.documents.find({'type':'exam paper'})

#for i in x:
#    print(i)

#
#compile_index()

