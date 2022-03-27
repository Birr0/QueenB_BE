from search_engine.indexer import index#, timing, analyse
import db_init
from scraper.transcript_generator_ms_streams.get_transcript import MsStreams

from bson.objectid import ObjectId

from dotenv import load_dotenv

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import json


load_dotenv()

from os import listdir
from os.path import isfile, join


def create_documents(files, path, doc_type, lecturer, module):
    #files = [f for f in listdir("./notes") if isfile(join("./notes", f))]
    ids = []
    module = module.split('_')
    for file in files:
        page_no = 1
        for page in extract_pages(f'{path}/{file}'):
            print(file + 'Page is number ' + str(page_no))
            for element in page:
                if isinstance(element, LTTextContainer):
                    x = db_init.db.documents.insert_one({
                        'title': '{} - Page {}'.format(file, page_no),
                        #'filename': '{}'.format(file),
                        'type': doc_type,
                        'content': element.get_text().strip(),
                        'lecturer' : lecturer,
                        'module_code': module[0],
                        'module_name' : module[1],
                    })
                    ids.append(x.inserted_id)
            page_no += 1
    return ids

def compile_index():
    index.Index(db = db_init.db).delete_index()
    for document in db_init.db.documents.find({}):
        ID = document['_id']
        print(ID)
        print(f'Adding document {ID}')
        index.Index(db = db_init.db).index_document(document)

#compile_index()

# need to delete old documents ... Think about pipeline as well

#db_init.db.documents.drop()
#db_init.db.index.drop()

'''
modules = [f for f in listdir("./notes")]
for module in modules:
    resources = (listdir(f'./notes/{module}'))
    for resource in resources: # resources = 'assignments', 'exam_papers' or 'lecturer_name'
        if resource == 'assignments':
            #print(listdir(f'./notes/{module}/assignments'))
            create_documents(listdir(f'./notes/{module}/assignments'),f'./notes/{module}/assignments' ,'assignment', '' ,module)
        if resource == 'exam_papers':
            create_documents(listdir(f'./notes/{module}/exam paper'), f'./notes/{module}/exam paper','exam paper', '' ,module)

        else:
            docs = (listdir(f'./notes/{module}/{resource}'))
            for k in docs:
                if k == 'notes':
                    create_documents(listdir(f'./notes/{module}/{resource}/notes'),f'./notes/{module}/{resource}/notes', 'notes', resource, module)
                if k == 'slides':
                    create_documents(listdir(f'./notes/{module}/{resource}/slides'),f'./notes/{module}/{resource}/slides', 'slides', resource, module)
                if k == 'transcripts':
                    with open(f'./notes/{module}/{resource}/transcripts/transcripts.json') as f:
                        transcripts = json.load(f)
                        modules = module.split('_')
                        MsStreams().download_transcripts(db = db_init.db, gd_path="scraper/transcript_generator_ms_streams/geckodriver/geckodriver.exe", resource_urls=transcripts, data={'module_code': modules[0], 'module_name': modules[1], 'lecturer': resource})
                else:
                    pass
'''
docs = db_init.db.documents.find({'lecturer':'Dr Daniele Margarone', 'type':'video'})


for doc in docs:
    #doc = db_init.db.documents.find_one({'_id': id})
    
    print('adding {}'.format(doc['_id']))
    
    index.Index(db=db_init.db).index_document(doc)



#x = db_init.db.documents.find({'type':'exam paper'})
#compile_index()

'''
ARREDONDO = [
    "https://web.microsoftstream.com/video/aba660ed-d13d-4c82-93f3-09f013295ace",
    "https://web.microsoftstream.com/video/26502012-af5b-4119-bc6a-56307b5598d3",
    "https://web.microsoftstream.com/video/b23655bf-e3f1-4ba5-93fe-2492c2064413",
    "https://web.microsoftstream.com/video/21bfe229-e650-4763-8ef8-0f3ffe667740",
    "https://web.microsoftstream.com/video/43de9fc8-5c76-47ec-b8e4-a0e94c4c5ffe",
    "https://web.microsoftstream.com/video/6879af14-3dc4-4013-8b22-aff3cebc5576",
    "https://web.microsoftstream.com/video/822ee8b4-5b55-41a0-893f-fba8e82d0be1",
    #"https://eu.nv.instructuremedia.com/fetch/QkFoYkIxc0hhUU5FQ01jd2JDc0gwd0ExWWc9PS0tOGVmN2Y0MWQ0YmMzNzIwMjJjNzVlNDIwOThhNWYyNjhjMjA4MjkwOA.mp4"
    "https://web.microsoftstream.com/video/7c38dbbd-b386-4359-a7bf-256c621f940e",
    "https://web.microsoftstream.com/video/2ad7a6b1-5496-48dc-bd6e-d587394ce593"
]

GREGG = [
    "https://web.microsoftstream.com/video/a6196026-4e1d-496a-b5aa-0478af48f75d",
    "https://web.microsoftstream.com/video/8705ad31-31a8-48c9-a46f-4904099cce99",
    "https://web.microsoftstream.com/video/9077eaa3-156b-4515-9e44-c2d2cec09cf7",
    "https://web.microsoftstream.com/video/286542f5-7de2-410d-922e-7ab9f0847d9b",
    "https://web.microsoftstream.com/video/bd092712-e33d-4999-afcf-f5c0e92fedc3",
    "https://web.microsoftstream.com/video/bb8d078f-830b-42a9-86ac-1de31566a368",
    "https://web.microsoftstream.com/video/11425589-fc09-4127-b455-4e9955660b4e",
    "https://web.microsoftstream.com/video/2cc390db-72dd-496b-b49f-3fb1a190ef0d?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
    "https://web.microsoftstream.com/video/de073c71-4c8c-4c9c-bb7f-4040b833a3d9?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f"
    "https://web.microsoftstream.com/video/df83ecdf-35fd-45e5-bee4-c595c5b87c86?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
    #PHONONS
    "https://web.microsoftstream.com/video/848cd1be-b9f6-438e-9707-4f85246234ca?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f"
    "https://web.microsoftstream.com/video/e07b9cef-7f0c-4330-adcd-dc5f898c2b15?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
    "https://web.microsoftstream.com/video/7b588d4d-08aa-421e-afcc-de4016818fca?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
    "https://web.microsoftstream.com/video/76ee549d-e9c0-40d5-a174-ae1fb6ad2217?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
    "https://web.microsoftstream.com/video/71661e48-b5bf-4cd6-8bc1-3e02c9361a43?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
    "https://web.microsoftstream.com/video/4de18a28-809f-41e3-b8b4-74b59fa43f78?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
    "https://web.microsoftstream.com/video/f32fee61-64e0-4074-a28e-695589713a28?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
    "https://web.microsoftstream.com/video/a3c65f7b-272d-4be4-aab3-5a4b973c485c?list=user&userId=098edaf9-d5ca-418e-afc9-02c34597cd7f",
]
'''

'''
NUCLEAR

SIM_NUCLEAR = [
    "https://web.microsoftstream.com/video/f42e681b-65fc-413e-b46d-a1775740a272",
    "https://web.microsoftstream.com/video/3f038cb5-aba6-4e05-819d-4bff1c6c25ff",
    "https://web.microsoftstream.com/video/046dcb48-df34-424d-be0f-33e9add203db",
    "https://web.microsoftstream.com/video/c7979044-2d62-4970-bc56-d702b3bd4ed3",
    "https://web.microsoftstream.com/video/5f7ee02e-fde4-4689-aa8c-3c5e3be0417a",
    "https://web.microsoftstream.com/video/3574b9da-28b9-43c9-839a-787122985ba6",
    "https://web.microsoftstream.com/video/4c2722c6-1d99-4809-9ab2-829254c96d84",
    "https://web.microsoftstream.com/video/8dcaee00-d7a0-44ca-baed-a4d9d8b8e7bb",
    "https://web.microsoftstream.com/video/3eeb3191-5455-41d2-b098-ceeca068cadc",
    "https://web.microsoftstream.com/video/51fa01ca-7213-4833-8a45-64b4543954ec",
    "https://web.microsoftstream.com/video/0724619b-a568-4c63-8428-80bc28296622",
    "https://web.microsoftstream.com/video/11458eca-c4a8-49d2-a44c-c592b06c2e01",
    "https://web.microsoftstream.com/video/e0ba0483-3b32-4e7c-9fbd-4ad5aa17608c",
    "https://web.microsoftstream.com/video/b5b256ef-8913-4c10-bdca-3a847cf6976a",
    "https://web.microsoftstream.com/video/811300fa-23ed-4a19-b7fd-62f86e5d70fa",
    "https://web.microsoftstream.com/video/6eb32dd2-07c7-413d-aea3-f207113c145f",
    "https://web.microsoftstream.com/video/ffce5960-0bd5-4c35-a665-9abf3279f1f4",
    "https://web.microsoftstream.com/video/46248df4-af87-4e83-96a8-d92eba7f56d3",
    "https://web.microsoftstream.com/video/679a91fd-08b8-4cbd-9d35-bdbf1405c271",
]

MARGONNE_NUCLEAR = [
    "https://web.microsoftstream.com/video/2f4900fc-4f86-4cf4-a26d-f9f4b69ed59d",
    "https://web.microsoftstream.com/video/65a5a0ce-055f-402d-b1ed-129e4689ec37",
    "https://web.microsoftstream.com/video/22409e1d-1926-49cb-8fdf-0473a4ba26ea",
    "https://web.microsoftstream.com/video/62fae006-8f18-4e03-9d8c-04bc359d0ff4",
    "https://web.microsoftstream.com/video/8c7f1c0f-a680-4408-ad93-04b3a6797809",
    "https://web.microsoftstream.com/video/67b36b12-aa2b-482a-bceb-32dc6f03d546",
    "https://web.microsoftstream.com/video/8dbf2002-8ceb-442a-9171-44757abb22e8",
    "https://web.microsoftstream.com/video/51774d52-d698-4504-b226-92f98e3bf8e0",
    "https://web.microsoftstream.com/video/662ad4bb-b6c3-426b-8127-d7411efecda2"
]

'''

'''
PALMER_LECTURES = [
    "https://web.microsoftstream.com/video/cf01ab5e-88da-4edf-9160-e74455fcc4d1",
    "https://web.microsoftstream.com/video/8b9a08ba-2d59-405a-8ff2-25cce1be4c59",
    "https://web.microsoftstream.com/video/5103f779-e6da-4950-842f-92a1d81786d5",
    "https://web.microsoftstream.com/video/80eff17a-4290-40fd-92b1-20b0d4211162",
    "https://web.microsoftstream.com/video/2cc56611-8a99-4643-85ea-bd4689cacd82",
    "https://web.microsoftstream.com/video/caa11975-51a8-4fbd-8abe-9db1f3203fce",
    "https://web.microsoftstream.com/video/386caab1-63cd-44d7-8fc0-b69bdb018992?channelId=280af834-223c-4de9-906e-a4c8621031c8",
    "https://web.microsoftstream.com/video/1c16656a-8ce2-41f8-9e30-3dccc2b6c605?channelId=280af834-223c-4de9-906e-a4c8621031c8",
    "https://web.microsoftstream.com/video/4ad6551b-9e1c-4274-824d-29f024e6623f?channelId=280af834-223c-4de9-906e-a4c8621031c8",
    "https://web.microsoftstream.com/video/b7a181fa-10ac-44c0-8534-5c0a95b227bc?channelId=280af834-223c-4de9-906e-a4c8621031c8",
    "https://web.microsoftstream.com/video/d4d47b81-4d38-4b3a-bf67-cdf1222256f9?channelId=280af834-223c-4de9-906e-a4c8621031c8",
    "https://web.microsoftstream.com/video/a48b5eb0-3543-41f9-9343-173398aacb6d?channelId=280af834-223c-4de9-906e-a4c8621031c8",
    "https://web.microsoftstream.com/video/56d32834-385d-4246-9a69-8a9309b37617?channelId=280af834-223c-4de9-906e-a4c8621031c8",
]
SARRI_LECTURES = [
    "https://web.microsoftstream.com/video/26362b41-3ec2-4be7-948c-b200dc0c7447",
    "https://web.microsoftstream.com/video/1f1193ec-0776-4f4c-b32e-e1f7d979d1a6?list=studio",
    "https://web.microsoftstream.com/video/ea1b74a1-b005-4cc2-a69b-b17ebe9f39c0?list=studio",
    "https://web.microsoftstream.com/video/3b4d0169-797d-4ee4-afb5-6be16569e270?list=studio",
    "https://web.microsoftstream.com/video/c6b49ee1-22bf-46a4-8dfe-4206ba79cd57",
    "https://web.microsoftstream.com/video/af4dc801-8164-4ff5-9482-d9c785f6f4d7",
    "https://web.microsoftstream.com/video/252361cf-91e3-4c9c-a88f-e5e61b39fbc1"
    "https://web.microsoftstream.com/video/adaabf1f-9b81-40f4-b315-91f0318b9cb7",
    "https://web.microsoftstream.com/video/f9b7080b-a516-4066-aa27-1c17b55f63b3",
    "https://web.microsoftstream.com/video/c08ee839-5f11-494a-a603-ca1dbf3cd0a3",
    "https://web.microsoftstream.com/video/b91b1ef4-69e3-4fa1-ad41-9c6ac4fd3399",
]
'''


'''

'''


'''
STAT-MECH
#MsStreams().download_transcripts(gd_path = os.environ.get('GECKODRIVER_PATH') , db = db_init.db, resource_urls=FIELD_URLS)
SIM_URLS = [ # up 7/12/21 -
    "https://web.microsoftstream.com/video/60a76609-f61a-42d6-aa20-77431b931344",
    "https://web.microsoftstream.com/video/d0e45c75-34ed-48df-ba76-d12eaed372eb",
    "https://web.microsoftstream.com/video/b029fd8d-aa43-4c4e-82e6-f5750eb35f4b",
    "https://web.microsoftstream.com/video/60cda699-ca4e-4a2e-b707-6f19775d1510",
    "https://web.microsoftstream.com/video/b693b2a9-2345-4623-bbc1-ec4d1789c9cb",
    "https://web.microsoftstream.com/video/03136c5a-1978-43db-afe9-4c82c1ca5a9d",
    "https://web.microsoftstream.com/video/652a7016-a438-4454-b112-5ba6f96ff323",
    "https://web.microsoftstream.com/video/8f1a3b5e-9a3b-422c-a20a-48a0170721d9",
    "https://web.microsoftstream.com/video/a3fccbd7-9c50-4768-8c9f-29b67308c4cc",
    "https://web.microsoftstream.com/video/5f255c6d-318c-4b53-9e1e-cf675d5d05e0",
    "https://web.microsoftstream.com/video/e28f5d08-bce9-4db6-a3d1-d62de2df7184",
    "https://web.microsoftstream.com/video/26ddf93d-274f-441a-a6a8-a934b7e5cab9",
    "https://web.microsoftstream.com/video/85f70086-c0ae-4e1f-859b-8427b8e9b851",
    "https://web.microsoftstream.com/video/faa5f735-45c6-4f7e-9d99-98c17cc66b30",
    "https://web.microsoftstream.com/video/02d39959-a30c-4e3e-a871-5c33b3221a12",
    "https://web.microsoftstream.com/video/273ae93d-fb03-4bf2-b8f7-31e5a69f7feb",
    "https://web.microsoftstream.com/video/4793a582-17a9-44b6-a36a-6155dea9e400",
    "https://web.microsoftstream.com/video/3e6f33f6-a42b-4a90-9c9d-b1b67604e10f",
    "https://web.microsoftstream.com/video/1eb53641-109d-44bb-a062-31e65a2335a2"
]

#Complete
WHITE_URLS = [
    "https://web.microsoftstream.com/video/3afe311e-caa9-4e93-89af-40d0fd250101",
    "https://web.microsoftstream.com/video/d7d20891-71b3-4e35-9661-4194961c5bce",
    "https://web.microsoftstream.com/video/0ad73228-86bd-47cf-b778-cacbe6dc1ee1",
    "https://web.microsoftstream.com/video/cff896a6-03db-4e01-953a-c724a4ed4141",
    "https://web.microsoftstream.com/video/f7ff30ab-018d-441f-b086-3d4e9ca55813",
    "https://web.microsoftstream.com/video/82de7515-9d5a-4e7c-a07f-bd1693da94d4",
    "https://web.microsoftstream.com/video/1ae1ae42-dd4c-4dd7-bb42-6bfc4ebf74a6",
    "https://web.microsoftstream.com/video/c6e47217-e531-4c02-8ccd-b120f380c836",
    "https://web.microsoftstream.com/video/5cfdcb83-3864-4698-86b1-7a4f7694336e",
    "https://web.microsoftstream.com/video/a7823cf5-00e0-41e1-98d4-24ec56e29156",
    "https://web.microsoftstream.com/video/7c8a4a63-8992-4e76-b81d-a950f10691e8",
    "https://web.microsoftstream.com/video/67949e1f-065c-425c-8a4a-b8b6f083d158",
    "https://web.microsoftstream.com/video/96b90122-8129-4f19-83d2-f0b99e7bc1f2",
    "https://web.microsoftstream.com/video/8a27ae4f-b4a0-42f6-a071-7d804766ae16",
]

KAR_URLS = [
    "https://web.microsoftstream.com/video/874adb78-5630-48d8-a19f-4c8beb2cb0e3?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/738e8b7f-83b9-4e1c-b14a-c1eca28701f2?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/2e04c80a-c1fd-414a-b1b9-53227dfc6c97?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/2a68b681-b3a4-44c1-b080-b9bd9af9d1e3?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/82a566f5-7bc4-43c9-935f-f210e23075c8?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/642dd598-7ff6-4d5e-8b62-79c201bc5ca6?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/459ce2ba-f7bf-402b-a700-5e87e5fb477d?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/367f0107-ecb6-47a6-a559-83bc34265563?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/454ec24a-da9b-4d8d-b09f-3dc0d9c25d7c?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/e70dd7a8-77b8-4cdb-bbc2-9915aca99ce3?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/9e303848-735e-4abe-a976-f2b4d76cf3f1?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/fdcfce22-7d87-449a-81e5-5176e2d0dbf9?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/79039920-0ddb-4aa0-bef0-5e57d5e8e1d0?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594",
    "https://web.microsoftstream.com/video/7646cf64-2c3b-4ced-a652-73c3217a746a?list=user&userId=631b100e-6ab5-46a3-b2ba-2669f65f8594"
]

FIELD_URLS = [
    "https://web.microsoftstream.com/video/d2e18a79-62d7-4d63-bb98-49b8ef249f3d",
    "https://web.microsoftstream.com/video/a7b07692-741c-4f9a-bd21-5f8c70cef232",
    "https://web.microsoftstream.com/video/5ade2b76-04f5-4e75-9eac-d0f35bd5bf76",
    "https://web.microsoftstream.com/video/f8023d7e-2da9-4aa6-8312-98e11d629c22",
    "https://web.microsoftstream.com/video/a1954c00-f1c7-43ea-b2aa-d01d334f2a29",
    "https://web.microsoftstream.com/video/6d997b20-b9a6-41bc-a6bb-2a485883aa47",
    "https://web.microsoftstream.com/video/19e73ef4-0b29-46fc-9668-2c1463dcb44c",
    "https://web.microsoftstream.com/video/b62dc005-bc91-4580-a0d7-214acdb1692a",
    "https://web.microsoftstream.com/video/da5f32e1-e80d-4b86-a06e-f5c4252a6e6c",
    "https://web.microsoftstream.com/video/820d1d1a-b7af-4775-bc56-b086e20df980",
    "https://web.microsoftstream.com/video/d4c80531-d192-4e80-ad9b-d9138b35795e",
    "https://web.microsoftstream.com/video/eec8c83f-ff12-4360-97ed-b6381df135f2",
    "https://web.microsoftstream.com/video/ff876a72-c906-4bfb-914e-77a1adf68731",
    "https://web.microsoftstream.com/video/7597b4ff-e3fb-42dc-b703-e7027d74251b",
    "https://web.microsoftstream.com/video/2a047db6-0194-4816-b2d1-68dad4d356cd",
    "https://web.microsoftstream.com/video/4b331239-6dd0-4895-891b-979bcf689f97",
    "https://web.microsoftstream.com/video/adb69556-e275-4ebd-b76d-5d1c9e58d2d1"
]

GREENWOOD_URLS = [
    "https://web.microsoftstream.com/video/ef2fe882-99d0-4c8d-a134-9c69a30cff63",
    "https://web.microsoftstream.com/video/684061ab-e80d-43df-bd44-6ec5193fdc0d",
    "https://web.microsoftstream.com/video/e9a29419-50ca-47dc-a870-27581675095c",
    "https://web.microsoftstream.com/video/6268351b-6cb1-4753-8318-4172681fe1a8",
    "https://web.microsoftstream.com/video/75c59efe-d5a0-4c06-8b25-78c6f202632a",
    "https://web.microsoftstream.com/video/63a93ca0-a5e4-4e3d-8f19-a7d9bbd0536a",
    "https://web.microsoftstream.com/video/e1e9e593-7940-4529-ac63-df62f539f599",
    "https://web.microsoftstream.com/video/53eeb8b5-a43b-4684-8c81-e8f82830d1d0",
    "https://web.microsoftstream.com/video/a5ef71d9-262f-433a-a8bb-49c5ae564d0b",
    "https://web.microsoftstream.com/video/060c7e2f-4bed-4766-bcaa-61800f46c2cf",
    "https://web.microsoftstream.com/video/f839c1e5-77c5-4711-97ad-bbf66bd34c97",
    "https://web.microsoftstream.com/video/edc8d1ce-8931-4048-ae34-f2db0ae904ea",
    "https://web.microsoftstream.com/video/f4ad8611-fb32-4836-aa48-e8d426392660",
    "https://web.microsoftstream.com/video/f3860902-e363-4d54-a44d-d6588845ff52",
    "https://web.microsoftstream.com/video/8176c2cd-867e-467b-9196-44656e7121da",
    "https://web.microsoftstream.com/video/fd8d9ae0-d1cd-46ab-9822-efbf0c8220b2",
    "https://web.microsoftstream.com/video/cc5e10f0-05f1-4600-bca5-5bb79ebe8361",
    "https://web.microsoftstream.com/video/744dd9ee-6dc4-4b98-9f2a-0c79acf5d1ca",
    "https://web.microsoftstream.com/video/a0cfbdef-3319-433a-838f-8efe0f2ad967"
]


'''