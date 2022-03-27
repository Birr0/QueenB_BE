from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from bs4 import BeautifulSoup
import time
import os


class MsStreams:
    def test(self, gd_path):
        print(gd_path)

    def download_transcripts(self, gd_path, db, resource_urls, data):
        print('Creating web driver.')
        driver = webdriver.Firefox(executable_path=gd_path)
        for i in range(len(resource_urls)): 
            
            document = {}
            try:
                time.sleep(2)
                driver.get(resource_urls[i])
                print('Valid URL recieved.')
                document['url'] = resource_urls[i]
                document['type'] = 'video'
            except:
                pass
            
            #WebDriverWait(driver)#.until(EC.presence_of_element_located((By.NAME, "loginfmt")))
            try:
                if i == 0:
                    time.sleep(2)
                    elem = driver.find_element_by_name("loginfmt")
                    elem.clear()
                    print(os.environ.get('MS_USERNAME'))
                    elem.send_keys(os.environ.get('MS_USERNAME'))
                    elem.send_keys(Keys.RETURN)
                    time.sleep(3)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "httpd_password")))
                    #add retry here, some reason aboce does not work if browser is not open...
                    pwd_field = driver.find_element_by_name("httpd_password")
                    pwd_field.clear()
                    pwd_field.send_keys(os.environ.get('MS_PASSWORD'))
                    pwd_field.send_keys(Keys.RETURN)
                    time.sleep(15)

            except:
                print('Login unsucessful')
                pass

            try:
                print('Getting transcript data ...')
                
                time.sleep(2)

                try:
                    content = driver.execute_script("try{return window.angular.element(window.document.querySelectorAll('.transcript-list')).scope().$ctrl.transcriptLines.map((t) => { return t; })} catch{return ''}")
                    document['content'] = ' '.join([clip['eventData']['text'] for clip in content])
                    document['video_data'] = content
                except:
                    print('Transcript is unavailable.')
                    pass

                document['lecturer'] = data['lecturer']
                document['module_code'] = data['module_code']
                document['module_name'] = data['module_name']

                try:
                    video_data = driver.find_element_by_class_name("video-meta-container")
                    soup = BeautifulSoup(video_data.get_attribute('innerHTML'), 'lxml')

                    title = soup.find(class_="title ng-binding").text
                    document['title'] = title
                except:
                    title = '{}-{}-{}'.format(data['lecturer'],data['module_code'],data['module_name'])
                #lecturer = soup.find(class_="c-hyperlink info-message-link ng-binding").text
                
                #date = soup.find(class_="info-message-content ng-binding ng-scope").text
                #document['date'] = date


                try:
                    description = soup.find(class_="item-description-content ng-binding ng-scope").text
                    document['description'] = description
                except:
                    
                    document['description'] = ''
                    print('Description not available.')

                print('Successfully recieved transcript data.')
            except:
                print('Unable to get transcript data.')
                raise
            db.documents.insert_one(document)
            
        driver.close()
'''
from pylatex import Document, NewPage, \
    Section, Subsection, Math, PageStyle, \
    LargeText, MediumText, LineBreak, Command, Foot, Head, Hyperref, Package

from pylatex.utils import bold, NoEscape, escape_latex
def hyperlink(url,text):
    text = escape_latex(text)
    return NoEscape(r'\href{' + url + '}{' + text + '}')

try:
    print('Generating LATEX document.')
    doc = Document()
    doc.packages.append(Package('hyperref'))
    doc.append(NoEscape(r'\hypersetup{colorlinks=false}'))
        
    doc.preamble.append(Command('title',title))
    doc.append(Command('author', author))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    if description:
        with doc.create(Section('Description')):
            doc.append(description)

    #doc.preamble.append(first_page)
    time_interval = input('Enter caption time interval (seconds):')

    try:
        time_interval = int(time_interval)
    except ValueError:
        print('Please use an integer interval.')
        raise ValueError
    
    print(len(ts))
    number_of_urls = round(ts[-1]['endSeconds']/time_interval)
    print(number_of_urls)
    captions_per_url = round(len(ts)/number_of_urls)
    print(captions_per_url)

    with doc.create(Section("Transcript")):
        for i in range(0, len(ts) - 1, captions_per_url):
            ref_url = URL + "?st=" + str(ts[i]['startSeconds'])
            text_block = " ".join(caption['eventData']['text'] for caption in ts[i: i + captions_per_url])
            doc.append(hyperlink(ref_url, text_block + " "))
    doc_title = title.strip()
    doc.generate_pdf(doc_title, clean_tex=False)

except:
    print('Unable to create document.')
    raise
'''


