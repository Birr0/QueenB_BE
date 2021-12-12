from search_engine.indexer import index, timing, analyse
import db_init
from scraper.transcript_generator_ms_streams.get_transcript import MsStreams

from bson.objectid import ObjectId

from dotenv import load_dotenv

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

load_dotenv()

from os import listdir
from os.path import isfile, join

def create_documents_from_notes():
    onlyfiles = [f for f in listdir("./notes") if isfile(join("./notes", f))]


    for file in onlyfiles:
        page_no = 1
        for page in extract_pages("./notes/astro_mooj/" + file):
            print(file + 'Page is number ' + str(page_no))
            for element in page:
                if isinstance(element, LTTextContainer):
                    db_init.db.documents.insert_one({
                        'title': '{} - Page {}'.format(file, page_no),
                        'filename': '{}'.format(file),
                        'type': 'pdf',
                        'content': element.get_text().strip(),
                        'page_number': page_no,
                        'lecturer' : '',
                        'date': '09/12/2021',
                        'description': ''
                    })
            page_no += 1


def compile_index():
    index.Index(db = db_init.db).delete_index()
    for document in db_init.db.documents.find({}):
        ID = document['_id']
        print(ID)
        print(f'Adding document {ID}')
        index.Index(db = db_init.db).index_document(document)


'''

#MsStreams().download_transcripts(gd_path = os.environ.get('GECKODRIVER_PATH') , db = db_init.db, resource_urls=FIELD_URLS)
SIM_URLS = [ # up 7/12/21
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

MOOJ_URLS = [
    "https://web.microsoftstream.com/video/9cd760bf-4e88-4925-8ce3-9a84b2581e3d",
    "https://web.microsoftstream.com/video/b3b416c7-bf2c-4ab0-8673-e30c708452ec",
    "https://web.microsoftstream.com/video/4f212b80-e839-4779-961a-52bb766996d6",
    "https://web.microsoftstream.com/video/43f286d9-8a5e-43a3-95b8-c40864b0df36",
    "https://web.microsoftstream.com/video/272c2067-678c-430c-8b4c-67351cda2187",
    "https://web.microsoftstream.com/video/ed3b80ad-4a39-4f46-94ef-f68756cafb7b",
    "https://web.microsoftstream.com/video/bf65a0a2-feda-4daf-9aac-3e2e514c2aa6",
    "https://web.microsoftstream.com/video/15963d44-7de9-4715-a806-dde957494c5c",
    "https://web.microsoftstream.com/video/3ee7cde1-4425-46f9-bd95-d3b84971f54d"
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

SCHWAMB_URLS = [
    "https://web.microsoftstream.com/video/547c26a4-5876-43f5-8a2a-0f7a08071e04",
    "https://web.microsoftstream.com/video/d9e991dd-4972-463e-810c-3d45e9b5547b",
    "https://web.microsoftstream.com/video/e348c5a3-2015-4bd8-a45f-782ec24024e4",
    "https://web.microsoftstream.com/video/b6f74408-3b2b-473a-a9c9-a798343285f7",
    "https://web.microsoftstream.com/video/e8d934df-045b-4471-9a9c-5a7e13108b39",
    "https://web.microsoftstream.com/video/d8d1972e-dfda-4f70-9ee5-13ee21801bc0",
    "https://web.microsoftstream.com/video/9d7a994c-2304-410f-b4cb-39d044a90251",
    "https://web.microsoftstream.com/video/98b377b3-d7ec-4eda-91c7-ac7521f73ee2",
    "https://web.microsoftstream.com/video/0ec3bfe5-bb59-4609-aabe-a341182b89f8",
    "https://web.microsoftstream.com/video/54b9526f-288e-489c-a555-a4a765e4adee",
    "https://web.microsoftstream.com/video/f6be1d43-f0e1-4145-b664-15ea656070fc",
    "https://web.microsoftstream.com/video/8f0e8d27-40f4-4841-918f-6cd454415315",
    "https://web.microsoftstream.com/video/b7f09914-412f-405d-9432-fa5f34a9bfa7",
    "https://web.microsoftstream.com/video/08f2d18c-1c9d-4326-b746-ed7b427e1e2a",
    "https://web.microsoftstream.com/video/b1c5f6c2-7096-4c1f-ad42-2c96fca35811",
    "https://web.microsoftstream.com/video/29bc1cdf-42a6-4587-ae58-4973a1d43ce0",
    "https://web.microsoftstream.com/video/56fb03e3-b89c-4a94-84c4-8e4e20c21f91",
    "https://web.microsoftstream.com/video/d713b6b8-c75a-4ff8-a58c-b3cb36865fbe",
    "https://web.microsoftstream.com/video/d61536ed-cbff-4262-bf69-30d9f5e973f7",
    "https://web.microsoftstream.com/video/dfee76f5-cdb8-47b3-9c10-da8664609d62",
    "https://web.microsoftstream.com/video/b4f2a511-df41-4c7e-8982-63fac96653a8",
    "https://web.microsoftstream.com/video/f3ff5cb0-5efd-43a4-a23c-2eecd4350064",
    "https://web.microsoftstream.com/video/6094a2e5-bbeb-4833-8da7-33de405fcd9c",
    "https://web.microsoftstream.com/video/f7064126-00dc-4605-928f-43ab3aa88206",
    "https://web.microsoftstream.com/video/3e699ad6-18cd-46c4-8b26-7ae3f17f8f87",
    "https://web.microsoftstream.com/video/6badc8af-1510-4f4b-8def-11522236319a",
    "https://web.microsoftstream.com/video/e83b491b-a923-4f33-ba37-8dc90ad1ddf9",
    "https://web.microsoftstream.com/video/33fe6341-84f0-4702-9987-cae4fcef1f62",
    "https://web.microsoftstream.com/video/ffb186cd-f904-4d44-96e7-4c2dc6c15730",
    
]
'''